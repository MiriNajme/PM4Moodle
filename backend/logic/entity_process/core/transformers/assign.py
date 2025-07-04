from logic.model.object_enum import ObjectEnum
from logic.utils.date_utils import format_date
from logic.utils.object_utils import get_object_key
from logic.entity_process.core.transformers.base import Base
from sqlalchemy import not_, or_


class Assign(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.ASSIGN
        self.object_class = self.db_service.Base.classes.mdl_assign
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True

        self.Files = self.db_service.Base.classes.mdl_files
        self.GradeItems = self.db_service.Base.classes.mdl_grade_items
        self.Context = self.db_service.Base.classes.mdl_context

    def get_relationship(self, row):
        relationships = []
        # region RELATED TO COURSE MODULE
        course_modules = self.db_service.fetch_course_modules_by_ids(
            row["id"], self.object_type.value.module_id
        )

        if course_modules:
            for course_module in course_modules:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.COURSE_MODULE, course_module["id"]
                        ),
                        "qualifier": "assign is course module",
                        "from": format_date(course_module["added"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )

                context = self.fetch_assignment_context_id(course_module["id"])
                if context:
                    files = self.db_service.fetch_assignment_files_by_context_id(
                        context["id"]
                    )
                    if files:
                        for file in files:
                            relationships.append(
                                {
                                    "objectId": get_object_key(
                                        ObjectEnum.FILES, file["id"]
                                    ),
                                    "qualifier": "Contains " + file["filearea"],
                                    "from": format_date(file["timecreated"]),
                                    "to": "9999-12-31T23:59:59.999Z",
                                }
                            )
        # endregion RELATED TO COURSE MODULE

        # region CALENDAR
        calendar_events = self.db_service.fetch_related_calendar_events(
            self.object_type.value.module_name, row["id"]
        )

        if calendar_events:
            for calendar_event in calendar_events:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.CALENDAR, calendar_event["id"]
                        ),
                        "qualifier": "assign has calendar event",
                        "from": format_date(calendar_event["timestart"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )
        # endregion CALENDAR

        # region GRADE ITEM
        grade_items = self.fetch_assign_grade_item(row["id"])
        if grade_items:
            for grade_item in grade_items:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.GRADE_ITEM, grade_item["id"]
                        ),
                        "qualifier": "assign is grade item",
                        "from": format_date(grade_item["timecreated"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )
        # endregion GRADE ITEM

        # region SUBMISSION FILES
        submission_files = self.fetch_submission_files(row["id"])
        if submission_files:
            for file in submission_files:
                relationships.append(
                    {
                        "objectId": get_object_key(ObjectEnum.FILES, file["id"]),
                        "qualifier": "Contains submission file",
                        "from": format_date(file["timecreated"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )
        # endregion SUBMISSION FILES

        return relationships

    def fetch_assign_grade_item(self, assign_id):
        grade_items = self.db_service.query_object(
            self.GradeItems,
            filters=[
                self.GradeItems.iteminstance == assign_id,
                self.GradeItems.itemmodule == "assign",
            ],
        )
        return grade_items if grade_items else None

    def fetch_submission_files(self, assign_id):
        assign_submission = self.db_service.Base.classes.mdl_assign_submission
        filter_conditions = [assign_submission.assignment == assign_id]
        submission_row = self.db_service.query_object(
            assign_submission, filter_conditions
        )
        if submission_row:
            filter_conditions = [
                self.Files.itemid == submission_row[0]["id"],
                self.Files.component == "assignsubmission_file",
                self.Files.filearea == "submission_files",
                not_(
                    or_(
                        self.Files.filename.like("."),
                        self.Files.filename.like(""),
                    )
                ),
            ]
            rows = self.db_service.query_object(
                self.Files, filter_conditions, sort_by=[("timecreated", "asc")]
            )
            return rows if rows else None

        return None

    def fetch_assignment_context_id(self, instance_id):
        filter_conditions = [
            self.Context.instanceid == instance_id,
            self.Context.contextlevel == 70,
        ]
        rows = self.db_service.query_object(self.Context, filter_conditions)
        return rows[0] if rows else None
