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
        self.view_filter_conditions = None

        self.CourseModule = self.db_service.Base.classes.mdl_course_modules
        self.Calendar_Event = self.db_service.Base.classes.mdl_event
        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log
        self.TaskAdhoc = self.db_service.Base.classes.mdl_task_adhoc

    # region Main extraction process
    def extract(self):
        self.add_create_import_events()
        self.add_delete_events()
        self.add_update_events()

        if self.has_view_events:
            self.add_view_events()

        self.add_complete_events()

    def extractBy(self, events: list = None):
        if not events:
            self.extract()
            return

    def add_create_import_events(self):
        list_of_objects = []
        events_map = None
        course_modules = self.fetch_all_course_modules_by_module(
            self.object_type.value.module_id
        )
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

    def add_complete_events(self):
        list_of_objects = []
        events = self.fetch_completed_events()
        if events:
            for event in events:
                list_of_objects.append(self.get_completed_module_event_object(event))

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

        calendar_events = self.fetch_related_calendar_events(
            self.object_type.value.module_name, row["instance"]
        )
        if calendar_events:
            for calendar_event in calendar_events:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.CALENDAR,
                        calendar_event["id"],
                        "potentially creates calendar event",
                    )
                )

        tag_instances = self.fetch_course_module_tag_instances(row["id"])
        if tag_instances:
            for tag_instance in tag_instances:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.TAG_INSTANCE,
                        tag_instance["id"],
                        "potentially creates tag instance",
                    )
                )

        relationships.append(
            get_formatted_relationship(ObjectEnum.USER, "unknown", "Imported by user")
        )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def process_viewed_events(self, events):
        result = []
        ids = {}
        course_modules = self.fetch_course_modules_by_completion_setting(
            2, self.object_type.value.module_id, self.view_filter_conditions
        )
        if course_modules:
            ids = {course_module["instance"]: False for course_module in course_modules}

        for event in events:
            result.append(self.get_viewed_event_object(event, ids))

        return result

    def get_viewed_event_object(self, event, ids):
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
        # if the module's completion has been set 2 when the first view event raised
        # then we should create both view and complete events
        if id in ids and not ids[id]:
            ids[id] = True

            result["types"] = [
                get_module_event_type_name(self.object_type, EventType.VIEWED),
                f"{get_module_event_type_name(
                    self.object_type, EventType.COMPLETED
                )}_automatic",
            ]

            qualifier = "Viewed and completed by user"
            rule_filters = [
                {"name": "must_be_viewed", "value": 1},
                {"name": "must_be_submitted", "value": 0},
                {"name": "must_be_graded", "value": None},
                {"name": "must_be_passed", "value": 0},
            ]
            rules = self.get_rule_by_filters(rule_filters)
            if rules:
                for rule in rules:
                    relationships.append(
                        get_formatted_relationship(
                            ObjectEnum.COMPLETION_RULE,
                            rule["id"],
                            "Completed according to",
                        )
                    )

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

            calendar_events = self.fetch_related_calendar_events(
                self.object_type.value.module_name, item_id
            )
            if calendar_events:
                for calendar_event in calendar_events:
                    relationships.append(
                        get_formatted_relationship(
                            ObjectEnum.CALENDAR,
                            calendar_event["id"],
                            "Deactivates calendar event",
                        )
                    )

        course_modules = self.db_service.fetch_course_modules_by_ids(
            item_id, self.object_type.value.module_id
        )
        if course_modules:
            for course_module in course_modules:
                tag_instances = self.fetch_course_module_tag_instances(
                    course_module["id"]
                )
                if tag_instances:
                    for tag_instance in tag_instances:
                        relationships.append(
                            get_formatted_relationship(
                                ObjectEnum.TAG_INSTANCE,
                                tag_instance["id"],
                                "Deactivates tag instance",
                            )
                        )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_completed_module_event_object(self, event):
        attributes = build_attributes(
            event, self.related_event_columns["course_module_completion"]
        )
        result = {
            "id": get_formatted_event_id(
                EventType.COMPLETED, self.object_type, event["id"]
            ),
            "type": f"{get_module_event_type_name(self.object_type, EventType.COMPLETED)}_manually",
            "time": format_date(event["timemodified"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                self.object_type,
                event[f"{self.object_type.value.name}id"],
                f"{EventType.COMPLETED.value.qualifier} {self.object_type.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Completed by user",
            ),
        ]

        if self.has_course_relation:
            course_relationships = self.get_course_relation(
                EventType.COMPLETED,
                event[f"{self.object_type.value.name}id"],
            )
            if course_relationships:
                relationships.append(course_relationships)

        rule_filters = [
            {"name": "is_manual", "value": 1},
        ]
        rules = self.get_rule_by_filters(rule_filters)

        if rules:
            for rule in rules:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.COMPLETION_RULE, rule["id"], "Completed according to"
                    )
                )

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
        module = f'%"module":"{self.object_type.value.module_id}"%'
        filter_conditions = [
            self.TaskAdhoc.classname.like("%course_delete_modules%"),
            self.TaskAdhoc.customdata.like(module),
        ]
        events = self.db_service.query_object(
            self.TaskAdhoc, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_completed_events(self, completion=1, extra_condition=None):
        events = []
        course_modules = self.fetch_course_modules_by_completion_setting(
            completion, self.object_type.value.module_id, extra_condition
        )

        if course_modules:
            course_module_ids = [
                course_module["id"] for course_module in course_modules
            ]
            course_module_instance_map = {
                course_module["id"]: course_module["instance"]
                for course_module in course_modules
            }

            event_filter_conditions = [
                self.CourseModuleCompletion.completionstate == completion,
                self.CourseModuleCompletion.coursemoduleid.in_(course_module_ids),
            ]
            events = self.db_service.query_object(
                self.CourseModuleCompletion,
                event_filter_conditions,
                sort_by=[("timemodified", "asc")],
            )

            for event in events:
                event[f"{self.object_type.value.name}id"] = (
                    course_module_instance_map.get(event["coursemoduleid"])
                )

        return events if events else None

    def fetch_module_by_id(self, module_id):
        filter_conditions = [self.object_class.id == module_id]
        rows = self.db_service.query_object(self.object_class, filter_conditions)
        return rows[0] if rows else None

    def fetch_related_calendar_events(self, module_name, instance_id):
        filter_conditions = [
            self.Calendar_Event.modulename == module_name,
            self.Calendar_Event.instance == instance_id,
        ]
        events = self.db_service.query_object(self.Calendar_Event, filter_conditions)
        return events if events else None

    def fetch_course_modules_by_completion_setting(
        self, completion, module, extra_condition=None
    ):
        filter_conditions = [
            self.CourseModule.completion == completion,
            self.CourseModule.module == module,
        ]

        if extra_condition:
            filter_conditions.extend(extra_condition)

        course_modules = self.db_service.query_object(
            self.CourseModule, filter_conditions
        )
        return course_modules if course_modules else None

    def fetch_course_module_tag_instances(self, course_module_id):
        added_tags = self.fetch_from_log_event(
            course_module_id, objecttable="tag_instance", action="added"
        )
        removed_tags = self.fetch_from_log_event(
            course_module_id, objecttable="tag_instance", action="removed"
        )
        instances = relation_formatter(added_tags, removed_tags, "objectid")
        return instances if instances else None

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

    def get_rule_by_filters(self, filters):
        return [
            rule
            for rule in self.get_rules()
            if all(
                any(
                    attr["name"] == f["name"] and attr["value"] == f["value"]
                    for attr in rule["attributes"]
                )
                for f in filters
            )
        ]

    def get_rules(self):
        return [
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 1),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 1),
                    },
                    {"name": "is_manual", "value": 1},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 2),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 2),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 3),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 3),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 4),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 4),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 5),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 5),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 6),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 6),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 7),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 7),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 8),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 8),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 9),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 9),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 10),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 10),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 11),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 11),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 12),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 12),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 1},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 13),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 13),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 1},
                ],
            },
        ]

    # endregion Data fetching helpers

    def get_course_relation(self, event_type_enum: EventType, id):
        course_rel = self.fetch_module_by_id(id)
        if course_rel:
            return {
                "objectId": get_object_key(ObjectEnum.COURSE, course_rel["course"]),
                "qualifier": get_course_relationship_qualifier(event_type_enum),
            }

        return None

    # --- Relationships logic moved to protected/private methods ---
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

            calendar_events = self.fetch_related_calendar_events(
                self.object_type.value.module_name, instance_id
            )
            if calendar_events:
                for calendar_event in calendar_events:
                    relationships.append(
                        get_formatted_relationship(
                            ObjectEnum.CALENDAR,
                            calendar_event["id"],
                            "potentially creates calendar event",
                        )
                    )

        tag_instances = self.fetch_course_module_tag_instances(event["objectid"])
        if tag_instances:
            for tag_instance in tag_instances:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.TAG_INSTANCE,
                        tag_instance["id"],
                        "potentially creates tag instance",
                    )
                )

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
