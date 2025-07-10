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
        self.view_filter_conditions = [
            self.CourseModule.completionview == 1,
            self.CourseModule.completion == 2,
            self.CourseModule.module == 5,
        ]

    def extract(self):
        super().extract()
        self.add_create_choice_answer_events()
        self.add_delete_choice_answer_events()

    def extractBy(self, events: list = None):
        if not events:
            self.extract()
            return

        if "create_choice" in events or "import_choice" in events:
            self.add_create_import_events()

        if "delete_choice" in events:
            self.add_delete_events()

        if "update_choice" in events:
            self.add_update_events()

        if "view_choice" in events:
            self.add_view_events()

        if (
            "complete_choice_manually" in events
            or "complete_choice_automatic" in events
        ):
            self.add_complete_events()

        if "created_answer" in events:
            self.add_create_choice_answer_events()

        if "deleted_answer" in events:
            self.add_delete_choice_answer_events()

    def add_complete_events(self):
        # manually completed
        super().add_complete_events()

        # automatically completed
        filter_conditions = []

        events = self.fetch_completed_events(2, filter_conditions)
        if events:
            for event in events:
                converted = self.get_completed_automatically_choice_event_object(event)
                if converted:
                    self.ocel_event_log["events"].append(converted)

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
        choice = self.fetch_module_by_id(id)
        is_just_completed_by_view = False
        if choice is not None and choice["completionsubmit"] == 0:
            is_just_completed_by_view = True

        if id in ids and ids[id] is False and is_just_completed_by_view:
            ids[id] = True

            result["types"] = [
                get_module_event_type_name(self.object_type, EventType.VIEWED),
                f"{get_module_event_type_name(self.object_type, EventType.COMPLETED)}_automatic",
            ]

            qualifier = "Viewed and completed by user"
            rule_filters = [
                {"name": "must_be_viewed", "value": 1},
                {"name": "make_a_choice", "value": 0},
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

        choice = self.fetch_module_by_id(event["choiceid"])
        if choice:
            course_relationships = self.get_course_relation(
                EventType.COMPLETED, choice["course"]
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
                        ObjectEnum.COMPLETION_RULE, rule["id"], "with completion_rule"
                    )
                )

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_completed_automatically_choice_event_object(self, event):
        choice = self.fetch_module_by_id(event["choiceid"])
        course_module = self.fetch_course_module_by_id(event["coursemoduleid"])
        if choice is None or (
            choice["completionsubmit"] == 0 and course_module["completionview"] == 1
        ):
            return None

        attributes = build_attributes(
            event, self.related_event_columns["course_module_completion"]
        )
        result = {
            "id": get_formatted_event_id(
                EventType.COMPLETED, self.object_type, event["id"]
            ),
            "type": f"{get_module_event_type_name(self.object_type, EventType.COMPLETED)}_automatic",
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
            get_formatted_relationship(
                ObjectEnum.COURSE,
                choice["course"],
                "Completed in course",
            ),
        ]

        rule_filters = [
            {"name": "make_a_choice", "value": choice["completionsubmit"]},
            {"name": "must_be_viewed", "value": course_module["completionview"]},
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

    def get_create_choice_answer_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.CREATED_ANSWER, self.object_type, event["id"]
            ),
            "type": EventType.CREATED_ANSWER.value.type,
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
                    f"{EventType.CREATED_ANSWER.value.qualifier} {self.object_type.value.name}",
                ),
                get_formatted_relationship(
                    ObjectEnum.USER,
                    event["userid"],
                    "Completed by user",
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
                "Selected by",
            ),
        )
        relationships.append(
            get_formatted_relationship(
                ObjectEnum.USER,
                event["relateduserid"],
                "Selected for",
            ),
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
                EventType.DELETED_ANSWER, self.object_type, event["id"]
            ),
            "type": EventType.DELETED_ANSWER.value.type,
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
                    f"{EventType.DELETED_ANSWER.value.qualifier} {self.object_type.value.name}",
                ),
                get_formatted_relationship(
                    ObjectEnum.OPTION,
                    instance["optionid"],
                    "Deselected option",
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
        relationships.append(
            get_formatted_relationship(
                ObjectEnum.USER,
                event["relateduserid"],
                "Deleted for",
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
