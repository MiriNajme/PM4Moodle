import json
from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.extractors.base import Base
from logic.utils.date_utils import format_date
from logic.utils.object_utils import convert_value_type, get_object_key
from logic.utils.extractor_utils import (
    build_attributes,
    get_formatted_event_id,
    get_formatted_relationship,
    get_module_event_type_name,
)


class Quiz(Base):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.QUIZ
        self.object_class = self.db_service.Base.classes.mdl_quiz
        self.has_view_events = True
        self.has_course_relation = True

    def extract(self, courses: list = None):
        super().extract(courses)
        self.get_question_events(EventType.CREATE_QUESTION)
        self.get_question_events(EventType.DELETE_QUESTION)
        self.get_question_slot_events(EventType.ADD_QUESTION_TO_QUIZ)
        self.get_question_slot_events(EventType.DELETE_QUESTION_FROM_QUIZ)
        self.get_attempt_quiz_events()
        self.get_set_grade_quiz_events()

    def extractBy(self, courses: list = None, events: list = None):
        if not events:
            self.extract(courses)
            return

        self.selected_courses = courses
        self.module_id = self.db_service.fetch_module_id(
            self.object_type.value.module_name
        )
        if "create_quiz" in events or "import_quiz" in events:
            self.add_create_import_events()

        if "delete_quiz" in events:
            self.add_delete_events()

        if "update_quiz" in events:
            self.add_update_events()

        if "view_quiz" in events:
            self.add_view_events()

        if "create_question" in events:
            self.get_question_events(EventType.CREATE_QUESTION)

        if "delete_question" in events:
            self.get_question_events(EventType.DELETE_QUESTION)

        if "add_question_to_quiz" in events:
            self.get_question_slot_events(EventType.ADD_QUESTION_TO_QUIZ)

        if "delete_question_from_quiz" in events:
            self.get_question_slot_events(EventType.DELETE_QUESTION_FROM_QUIZ)

        if "attempt_quiz" in events or "reattempt_quiz" in events:
            self.get_attempt_quiz_events()

        if "set_grade_quiz" in events:
            self.get_set_grade_quiz_events()

    def get_question_events(self, event_type: EventType):
        if event_type == EventType.CREATE_QUESTION:
            action = "created"
        else:
            action = "deleted"

        filter_conditions = [
            self.Log.action == action,
            self.Log.target == "question",
            self.Log.objecttable == "question",
        ]

        events = self.fetch_question_events(filter_conditions)

        if events:
            for event in events:
                formated_event_object = self.get_question_event_object(
                    event, event_type
                )
                if formated_event_object is not None:
                    self.ocel_event_log["events"].append(formated_event_object)

    def get_question_slot_events(self, event_type: EventType):
        if event_type == EventType.ADD_QUESTION_TO_QUIZ:
            action = "created"
        else:
            action = "deleted"

        filter_conditions = [
            self.Log.action == action,
            self.Log.target == "slot",
            self.Log.objecttable == "quiz_slots",
        ]

        events = self.fetch_question_events(filter_conditions)

        if events:
            for event in events:
                formated_event_object = self.get_question_slot_event_object(
                    event, event_type
                )
                if formated_event_object is not None:
                    self.ocel_event_log["events"].append(formated_event_object)

    def get_attempt_quiz_events(self):
        events = self.fetch_attempt_quiz_events()

        if events:
            for event in events:
                formated_event_object = self.get_attempt_quiz_event_object(event)
                if formated_event_object is not None:
                    self.ocel_event_log["events"].append(formated_event_object)

    def get_set_grade_quiz_events(self):
        events = self.fetch_set_grade_quiz_events()

        if events:
            for event in events:
                formated_event_object = self.get_set_grade_quiz_event_object(event)
                if formated_event_object is not None:
                    self.ocel_event_log["events"].append(formated_event_object)

    def get_question_event_object(self, event, event_type_enum: EventType):
        event_type = event_type_enum.value.type
        attributes = build_attributes(event, self.related_event_columns["log"])

        result = {
            "id": get_formatted_event_id(
                event_type_enum, self.object_type, event["id"]
            ),
            "type": event_type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        if event_type_enum is EventType.CREATE_QUESTION:
            user_qualifier = "Added by user"
            question_qualifier = "Creates question"
        elif event_type_enum is EventType.DELETE_QUESTION:
            user_qualifier = "Deleted by user"
            question_qualifier = "Deletes question"
        else:
            user_qualifier = ""
            question_qualifier = ""

        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                user_qualifier,
            ),
            get_formatted_relationship(
                ObjectEnum.QUESTION,
                event["objectid"],
                question_qualifier,
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        self.set_quiz_relationship(event, event_type_enum, relationships)

        hints = self.fetch_question_hints(event["objectid"])
        for hint in hints:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.QUESTION_HINT,
                    hint["id"],
                    "Creates hint",
                )
            )

        if event_type_enum is EventType.CREATE_QUESTION:
            answers = self.fetch_question_answers(event["objectid"])
            for answer in answers:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.QUESTION_ANSWER,
                        answer["id"],
                        "Creates answer",
                    )
                )

        if relationships:
            result["relationships"] = relationships
        return result

    def get_question_slot_event_object(self, event, event_type_enum: EventType):
        event_type = event_type_enum.value.type
        attributes = build_attributes(event, self.related_event_columns["log"])

        result = {
            "id": get_formatted_event_id(
                event_type_enum, self.object_type, event["id"]
            ),
            "type": event_type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        if event_type_enum is EventType.ADD_QUESTION_TO_QUIZ:
            user_qualifier = "Added by user"
            quiz_qualifier = "Added to the quiz"
        elif event_type_enum is EventType.DELETE_QUESTION_FROM_QUIZ:
            user_qualifier = "Deleted by user"
            quiz_qualifier = "Deleted from the quiz"
        else:
            user_qualifier = ""
            quiz_qualifier = ""

        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER, event["userid"], user_qualifier
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        instance = json.loads(event["other"])
        if instance:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.QUIZ, instance["quizid"], quiz_qualifier
                )
            ),

        if event_type_enum == EventType.ADD_QUESTION_TO_QUIZ:
            question_refrence = self.fetch_question_refrence(
                event["objectid"], "itemid"
            )
            if question_refrence is not None:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.QUESTION_BANK_ENTRY,
                        question_refrence["questionbankentryid"],
                        "Adds question bank entry to quiz",
                    )
                ),

        if relationships:
            result["relationships"] = relationships
        return result

    def get_attempt_quiz_event_object(self, event):
        if event["attempt"] == 1:
            event_type_enum = EventType.QUIZ_ATTEMPT
            user_qualifier = "Attempted by user"
        else:
            event_type_enum = EventType.QUIZ_REATTEMPT
            user_qualifier = "Reattempted by user"

        event_type = event_type_enum.value.type
        attributes = [
            {"name": col["name"], "value": convert_value_type(event[col["name"]])}
            for col in self.related_event_columns["quiz_attempt"]
        ]

        result = {
            "id": get_formatted_event_id(
                event_type_enum, self.object_type, event["id"]
            ),
            "type": event_type,
            "time": format_date(event["timestart"]),
            "attributes": attributes,
        }

        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER, event["userid"], user_qualifier
            ),
            get_formatted_relationship(
                ObjectEnum.QUIZ, event["quiz"], event_type_enum.value.qualifier
            ),
        ]

        quiz = self.fetch_quiz_by_id(event["quiz"])
        if quiz is not None:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.COURSE, quiz["course"], "Related to course"
                )
            )

        if relationships:
            result["relationships"] = relationships
        return result

    def get_set_grade_quiz_event_object(self, event):
        user_qualifier = "Graded user"

        event_type = get_module_event_type_name(
            ObjectEnum.QUIZ, EventType.QUIZ_SET_GRADE
        )

        attributes = [
            {"name": col["name"], "value": convert_value_type(event[col["name"]])}
            for col in self.related_event_columns["quiz_grades"]
        ]

        result = {
            "id": get_formatted_event_id(
                EventType.QUIZ_SET_GRADE, self.object_type, event["id"]
            ),
            "type": event_type,
            "time": format_date(event["timemodified"]),
            "attributes": attributes,
        }

        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER, event["userid"], user_qualifier
            ),
            get_formatted_relationship(ObjectEnum.USER, "system", "Graded by system"),
            get_formatted_relationship(
                ObjectEnum.QUIZ, event["quiz"], EventType.QUIZ_SET_GRADE.value.qualifier
            ),
        ]

        quiz = self.fetch_quiz_by_id(event["quiz"])
        if quiz is not None:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.COURSE, quiz["course"], "Related to course"
                )
            )

        if relationships:
            result["relationships"] = relationships
        return result

    def set_quiz_relationship(self, event, event_type, relationships):
        if event_type is EventType.CREATE_QUESTION:
            bank_entry_qualifier = "Creates bank entry"
            quiz_qualifier = "Created in the quiz question bank"
        elif event_type is EventType.DELETE_QUESTION:
            bank_entry_qualifier = "Deletes bank entry"
            quiz_qualifier = "Deleted from the quiz question bank"
        else:
            bank_entry_qualifier = ""
            quiz_qualifier = ""

        course_modules = self.fetch_course_module_by_id(event["contextinstanceid"])

        if course_modules is not None:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.QUIZ,
                    course_modules["instance"],
                    quiz_qualifier,
                )
            )

        question_version = self.fetch_question_version(event["objectid"])

        if question_version is None:
            return relationships

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.QUESTION_BANK_ENTRY,
                question_version["questionbankentryid"],
                bank_entry_qualifier,
            )
        )

        if course_modules is None:
            question_refrence = self.fetch_question_refrence(
                question_version["questionbankentryid"], "questionbankentryid"
            )

            if question_refrence is not None:
                context = self.fetch_context(question_refrence["usingcontextid"])

                if context is None:
                    return relationships

                course_modules = self.fetch_course_module_by_id(context["instanceid"])

                if course_modules is not None:
                    relationships.append(
                        get_formatted_relationship(
                            ObjectEnum.QUIZ,
                            course_modules["instance"],
                            quiz_qualifier,
                        )
                    )

        return relationships

    def fetch_question_events(self, filter_conditions):
        if self.selected_courses:
            filter_conditions.append(self.Log.courseid.in_(self.selected_courses))

        rows = self.db_service.query_object(
            self.Log,
            filter_conditions,
            sort_by=[("timecreated", "asc"), ("objectid", "asc")],
        )
        return rows if rows else None

    def fetch_question_version(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_versions
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows[0] if rows else None

    def fetch_question_refrence(self, id, column_name):
        TABLE = self.db_service.Base.classes.mdl_question_references
        filter_conditions = [getattr(TABLE, column_name) == id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows[0] if rows else None

    def fetch_context(self, using_context_id):
        TABLE = self.db_service.Base.classes.mdl_question_references
        filter_conditions = [TABLE.id == using_context_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows[0] if rows else None

    def fetch_attempt_quiz_events(self):
        TABLE = self.db_service.Base.classes.mdl_quiz_attempts
        quiz_ids = self.fetch_quiz_ids_by_course_ids()
        filter_conditions = None

        if quiz_ids:
            filter_conditions = [TABLE.quiz.in_(quiz_ids)]

        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_set_grade_quiz_events(self):
        TABLE = self.db_service.Base.classes.mdl_quiz_grades
        quiz_ids = self.fetch_quiz_ids_by_course_ids()
        filter_conditions = None

        if quiz_ids:
            filter_conditions = [TABLE.quiz.in_(quiz_ids)]

        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_question_answers(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_answers
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else []

    def fetch_question_hints(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_hints
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else []

    def fetch_quiz_by_id(self, quiz_id):
        TABLE = self.db_service.Base.classes.mdl_quiz
        filter_conditions = [TABLE.id == quiz_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows[0] if rows else None

    def fetch_quiz_ids_by_course_ids(self):
        TABLE = self.db_service.Base.classes.mdl_quiz
        filter_conditions = None

        if self.selected_courses:
            filter_conditions = [TABLE.course.in_(self.selected_courses)]

        rows = self.db_service.query_object(TABLE, filter_conditions)

        return [row["id"] for row in rows] if rows else []
