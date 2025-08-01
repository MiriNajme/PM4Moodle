import json

from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.utils.extractor_utils import (
    build_attributes,
    get_formatted_event_id,
    get_formatted_relationship,
    get_module_event_type_name,
)
from logic.utils.date_utils import format_date
from logic.entity_process.core.extractors.base import Base


class Choice(Base):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.CHOICE
        self.object_class = self.db_service.Base.classes.mdl_choice
        self.has_view_events = True
        self.has_course_relation = True

    def extract(self, courses: list = None):
        super().extract(courses)
        self.add_create_choice_answer_events()
        self.add_delete_choice_answer_events()

    def extractBy(self, courses: list = None, events: list = None):
        if not events:
            self.extract(courses)
            return

        self.selected_courses = courses

        self.module_id = self.db_service.fetch_module_id(
            self.object_type.value.module_name
        )

        if "create_choice" in events or "import_choice" in events:
            self.add_create_import_events()

        if "delete_choice" in events:
            self.add_delete_events()

        if "update_choice" in events:
            self.add_update_events()

        if "view_choice" in events:
            self.add_view_events()

        if "make_a_choice" in events:
            self.add_create_choice_answer_events()

        if "remove_a_choice" in events:
            self.add_delete_choice_answer_events()

    def add_create_choice_answer_events(self):
        events = self.fetch_choice_answer_events("created")
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_create_choice_answer_event_object(event)
                )

    def add_delete_choice_answer_events(self):
        events = self.fetch_choice_answer_events("deleted")
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_deleted_choice_answer_event_object(event)
                )

    def get_module_event_object(self, event, event_type_enum: EventType):
        result = super().get_module_event_object(event, event_type_enum)
        instance = json.loads(event["other"])

        if instance:
            choice_id = instance["instanceid"]
            choice_options = self.fetch_choice_options_by_choice_id(choice_id)
            for option in choice_options:
                result["relationships"].append(
                    get_formatted_relationship(
                        ObjectEnum.OPTION,
                        option["id"],
                        "Choice option",
                    )
                )

        return result

    def get_module_import_event_object(self, row):
        result = super().get_module_import_event_object(row)
        choice_options = self.fetch_choice_options_by_choice_id(row["instance"])

        for option in choice_options:
            result["relationships"].append(
                get_formatted_relationship(
                    ObjectEnum.OPTION,
                    option["id"],
                    "Imported option",
                )
            )

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
        choice = self.fetch_module_by_id(id)

        # region RELATIONSHIPS
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

        if choice:
            course_relation = self.get_course_relation(EventType.VIEWED, id)
            if course_relation:
                relationships.append(course_relation)

            choice_options = self.fetch_choice_options_by_choice_id(choice["id"])
            for option in choice_options:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.OPTION,
                        option["id"],
                        "Choice option",
                    )
                )

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

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

            choice = self.fetch_module_by_id(item_id)
            if choice:
                course_relationships = self.get_course_relation(
                    EventType.DELETED, choice["course"]
                )
                if course_relationships:
                    relationships.append(course_relationships)

            choice_options = self.fetch_choice_options_by_choice_id(item_id)
            for option in choice_options:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.OPTION,
                        option["id"],
                        "Deletes option",
                    )
                )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_create_choice_answer_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.MAKE_A_CHOICE, self.object_type, event["id"]
            ),
            "type": EventType.MAKE_A_CHOICE.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = []
        instance = json.loads(event["other"])
        if instance:
            relationships = [
                get_formatted_relationship(
                    self.object_type,
                    instance[f"{self.object_type.value.name}id"],
                    f"{EventType.MAKE_A_CHOICE.value.qualifier} {self.object_type.value.name}",
                ),
                get_formatted_relationship(
                    ObjectEnum.OPTION,
                    instance["optionid"],
                    "Selected option",
                ),
            ]

            choice = self.fetch_module_by_id(instance["choiceid"])
            if choice:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.COURSE,
                        choice["course"],
                        "Pertains to course",
                    ),
                )

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Made a choice by user",
            )
        )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_deleted_choice_answer_event_object(self, event):
        attributes = []
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.REMOVE_A_CHOICE, self.object_type, event["id"]
            ),
            "type": EventType.REMOVE_A_CHOICE.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = []
        instance = json.loads(event["other"])
        if instance:
            relationships = [
                get_formatted_relationship(
                    self.object_type,
                    instance[f"{self.object_type.value.name}id"],
                    f"{EventType.REMOVE_A_CHOICE.value.qualifier} {self.object_type.value.name}",
                ),
                get_formatted_relationship(
                    ObjectEnum.OPTION,
                    instance["optionid"],
                    "Removes selection",
                ),
            ]

            choice = self.fetch_module_by_id(instance["choiceid"])
            if choice:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.COURSE,
                        choice["course"],
                        "Pertains to course",
                    ),
                )

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Deleted by",
            ),
        )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def fetch_choice_answer_events(self, action_type):
        filter_conditions = [
            self.Log.action == action_type,
            self.Log.objecttable == "choice_answers",
        ]

        if self.selected_courses:
            filter_conditions.append(self.Log.courseid.in_(self.selected_courses))

        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_module_by_id(self, module_id):
        choices = self.db_service.query_object(
            self.object_class,
            [self.object_class.id == module_id],
            sort_by=[("timemodified", "asc")],
        )
        return choices[0] if choices else None

    def fetch_choice_options_by_choice_id(self, choice_id):
        option_table = self.db_service.Base.classes.mdl_choice_options
        filter_conditions = [option_table.choiceid == choice_id]
        rows = self.db_service.query_object(option_table, filter_conditions)
        return rows if rows else []
