import json
from abc import ABC
from sqlalchemy import func
from logic.model.object_enum import ObjectEnum
from logic.model.event_types import EventType
from logic.utils.object_utils import get_object_key, relation_formatter
from logic.utils.date_utils import format_date
from logic.utils.extractor_utils import (
    build_attributes,
    get_course_relationship_qualifier,
    get_formatted_event_id,
    get_formatted_relationship,
    get_module_event_type_name,
)


class Base(ABC):
    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        self.db_service = db_service
        self.related_object_columns = related_object_columns
        self.related_event_columns = related_event_columns
        self.ocel_event_log = ocel_event_log
        self.object_type: ObjectEnum = None
        self.object_class = None
        self.has_view_events = False
        self.has_course_relation = False
        self.deleted_items = {}
        self.module_id = 0
        self.CourseModule = self.db_service.Base.classes.mdl_course_modules
        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log
        self.TaskAdhoc = self.db_service.Base.classes.mdl_task_adhoc

    # region Main extraction process
    def extract(self):
        self.module_id = self.db_service.fetch_module_id(
            self.object_type.value.module_name
        )

        self.add_create_import_events()
        self.add_delete_events()
        self.add_update_events()

        if self.has_view_events:
            self.add_view_events()

    def extractBy(self, events: list = None):
        pass

    def add_create_import_events(self):
        list_of_objects = []
        events_map = None
        course_modules = self.fetch_all_course_modules_by_module(self.module_id)
        events = self.fetch_module_events(EventType.CREATED.value.name)

        if events:
            events_map = {event["objectid"]: event for event in events}

        if events_map and course_modules:
            for row in course_modules:
                if row["id"] in events_map:
                    list_of_objects.append(
                        self.get_module_event_object(
                            events_map.get(row["id"]), EventType.CREATED
                        )
                    )
                else:
                    list_of_objects.append(self.get_module_import_event_object(row))

        self.ocel_event_log["events"].extend(list_of_objects)

    def add_update_events(self):
        list_of_objects = []
        events = self.fetch_module_events(EventType.UPDATED.value.name)
        if events:
            for event in events:
                formated_event_object = self.get_module_event_object(
                    event, EventType.UPDATED
                )
                if formated_event_object is not None:
                    list_of_objects.append(formated_event_object)

        self.deleted_items = None
        self.ocel_event_log["events"].extend(list_of_objects)

    def add_view_events(self):
        list_of_objects = []
        events = self.fetch_viewed_events(EventType.VIEWED.value.name)
        if events:
            list_of_objects.extend(self.process_viewed_events(events))

        self.deleted_items = None
        self.ocel_event_log["events"].extend(list_of_objects)

    def add_delete_events(self):
        list_of_objects = []
        events = self.fetch_deleted_events()
        if events:
            for event in events:
                list_of_objects.append(self.get_deleted_module_event_object(event))

        self.ocel_event_log["events"].extend(list_of_objects)

    # endregion Main extraction process

    # region Event object construction
    def get_module_event_object(self, event, event_type_enum: EventType):
        event_type = get_module_event_type_name(self.object_type, event_type_enum)
        attributes = build_attributes(event, self.related_event_columns["log"])

        result = {
            "id": get_formatted_event_id(
                event_type_enum, self.object_type, event["id"]
            ),
            "type": event_type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        relationships = self.module_relationships(event, event_type_enum)
        if relationships:
            result["relationships"] = relationships
        return result

    def get_module_import_event_object(self, row):
        result = {
            "id": get_formatted_event_id(
                EventType.IMPORTED, self.object_type, row["id"]
            ),
            "type": f"import_{self.object_type.value.name}",
            "time": format_date(row["added"]),
            "attributes": [],
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                self.object_type,
                row["instance"],
                f"{EventType.IMPORTED.value.qualifier} {self.object_type.value.name}",
            )
        ]

        if self.has_course_relation:
            course_relationship = self.get_course_relation(
                EventType.IMPORTED, row["instance"]
            )
            if course_relationship:
                relationships.append(course_relationship)

        relationships.append(
            get_formatted_relationship(ObjectEnum.USER, "unknown", "Imported by user")
        )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def process_viewed_events(self, events):
        result = []

        for event in events:
            result.append(self.get_viewed_event_object(event))

        return result

    def get_viewed_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        relationships = []
        id = event["objectid"]
        qualifier = "Viewed by user"
        result = {
            "id": get_formatted_event_id(
                EventType.VIEWED, self.object_type, event["id"]
            ),
            "type": get_module_event_type_name(self.object_type, EventType.VIEWED),
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        relationships.append(
            get_formatted_relationship(
                self.object_type,
                id,
                f"Viewed {self.object_type.value.name}",
            )
        )

        relationships.append(
            get_formatted_relationship(ObjectEnum.USER, event["userid"], qualifier)
        )
        result["relationships"] = relationships
        return result

    def get_deleted_module_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["task_adhoc"])

        result = {
            "id": get_formatted_event_id(
                EventType.DELETED, self.object_type, event["id"]
            ),
            "type": get_module_event_type_name(self.object_type, EventType.DELETED),
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = []
        instance = json.loads(event["customdata"])
        if instance:
            item_id = instance["cms"][0]["instance"]
            self.deleted_items[item_id] = event["timecreated"]
            relationships.append(
                get_formatted_relationship(
                    self.object_type,
                    item_id,
                    f"{EventType.DELETED.value.qualifier} {self.object_type.value.name}",
                )
            )
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.USER, instance["userid"], "Deleted by user"
                )
            )

            if self.has_course_relation:
                course_relationships = self.get_course_relation(
                    EventType.DELETED,
                    item_id,
                )
                if course_relationships:
                    relationships.append(course_relationships)

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    # endregion Event object construction

    # region Data fetching helpers
    def fetch_all_course_modules_by_module(self, module_id):
        filter_conditions = [self.CourseModule.module == module_id]
        course_modules = self.db_service.query_object(
            self.CourseModule, filter_conditions
        )
        return course_modules if course_modules else None

    def fetch_module_events(self, action_type):
        filter_conditions = [
            self.Log.action == action_type,
            self.Log.objecttable == "course_modules",
            func.JSON_EXTRACT(self.Log.other, "$.modulename")
            == self.object_type.value.module_name,
        ]
        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_viewed_events(self, action_type):
        filter_conditions = [
            self.Log.action == action_type,
            self.Log.objecttable == self.object_type.value.module_name,
            self.Log.target == "course_module",
        ]
        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_deleted_events(self):
        module = f'%"module":"{self.module_id}"%'
        filter_conditions = [
            self.TaskAdhoc.classname.like("%course_delete_modules%"),
            self.TaskAdhoc.customdata.like(module),
        ]
        events = self.db_service.query_object(
            self.TaskAdhoc, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_module_by_id(self, module_id):
        filter_conditions = [self.object_class.id == module_id]
        rows = self.db_service.query_object(self.object_class, filter_conditions)
        return rows[0] if rows else None

    def fetch_from_log_event(
        self,
        event_id,
        action="created",
        objecttable=None,
        sort_by=[("timecreated", "asc")],
        itemtype="course_modules",
    ):
        filter_conditions = [
            self.Log.other.like(f'%"itemtype":"{itemtype}"%'),
            (
                self.Log.other.like('%"itemid":"' + str(event_id) + '"%')
                | self.Log.other.like('%"itemid":' + str(event_id) + "%")
            ),
            self.Log.action == action,
            self.Log.objecttable == objecttable,
        ]
        result = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=sort_by
        )
        return result

    # endregion Data fetching helpers

    def get_course_relation(self, event_type_enum: EventType, id):
        course_rel = self.fetch_module_by_id(id)
        if course_rel:
            return {
                "objectId": get_object_key(ObjectEnum.COURSE, course_rel["course"]),
                "qualifier": get_course_relationship_qualifier(event_type_enum),
            }

        return None

    def module_relationships(self, event, event_type_enum: EventType):
        relationships = []
        qualifier = f"{event_type_enum.value.qualifier} {self.object_type.value.name}"
        instance = json.loads(event["other"])

        if instance:
            instance_id = instance["instanceid"]
            if event_type_enum == EventType.UPDATED:
                delete_time = self.deleted_items.get(instance_id)
                if delete_time is not None and event["timecreated"] > delete_time:
                    return None

            relationships.append(
                get_formatted_relationship(self.object_type, instance_id, qualifier)
            )

            if self.has_course_relation:
                course_relation = self.get_course_relation(event_type_enum, instance_id)
                if course_relation:
                    relationships.append(course_relation)

        qualifier = (
            "Created by user"
            if event_type_enum == EventType.CREATED
            else "Updated by user"
        )
        relationships.append(
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                qualifier,
            ),
        )

        return relationships
