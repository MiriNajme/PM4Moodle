import json
from logic.entity_process.core.extractors.base import Base
from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.utils.extractor_utils import (
    build_attributes,
    get_formatted_event_id,
    get_formatted_relationship,
    get_module_event_type_name,
)
from logic.utils.date_utils import format_date

from sqlalchemy import not_, or_


class Assign(Base):
    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.ASSIGN
        self.object_class = self.db_service.Base.classes.mdl_assign
        self.has_view_events = True
        self.has_course_relation = True
        
        self.GradeItemsHistory = self.db_service.Base.classes.mdl_grade_items_history
        self.Context = self.db_service.Base.classes.mdl_context
        self.Files = self.db_service.Base.classes.mdl_files
        self.Assign_submission = self.db_service.Base.classes.mdl_assign_submission
        
    def extract(self):
        super().extract()

        self.add_submit_assignment_events()
        self.add_grade_assignment_events()

    def extractBy(self, events: list = None):
        if not events:
            self.extract()
            return

        if "create_assign" in events or "import_assign" in events:
            self.add_create_import_events()

        if "delete_assign" in events:
            self.add_delete_events()

        if "update_assign" in events:
            self.add_update_events()

        if "view_assign" in events:
            self.add_view_events()

        if (
            "submit_group_assign" in events
            or "submit_individual_assign" in events
            or "resubmit_group_assign" in events
            or "resubmit_individual_assign" in events
        ):
            self.add_submit_assignment_events()
    
        if "set_grade" in events or "update_grade" in events:
            self.add_grade_assignment_events()

    def add_create_import_events(self):
        assigns = self.fetch_assigns()
        for assign in assigns:
            course_module = self.fetch_course_module_by_instance(
                assign["id"], ObjectEnum.ASSIGN.value.module_id
            )
            event = self.fetch_assign_event_by_ids(
                course_module["id"], EventType.CREATED.value.name
            )
            if event:
                self.ocel_event_log["events"].append(
                    self.get_assign_create_event_object(event, assign)
                )
            else:
                self.ocel_event_log["events"].append(
                    self.get_module_import_event_object(course_module)
                )

    def add_submit_assignment_events(self):
        processed_ids = []
        events = self.fetch_submitted_assignment_events()
        if events:
            for event in events:
                object_id = event["objectid"]
                converted = None

                if object_id not in processed_ids:
                    processed_ids.append(object_id)
                    converted = self.get_submit_assignment_event_object(event)
                else:
                    converted = self.get_resubmit_assignment_event_object(event)

                if converted:
                    self.ocel_event_log["events"].append(converted)

    def add_grade_assignment_events(self):
        object_ids = []
        events = self.fetch_grade_assignment_events()
        if events:
            for event in events:
                if event["objectid"] in object_ids:
                    event_type = EventType.UPDATED
                else:
                    object_ids.append(event["objectid"])
                    event_type = EventType.SET

                self.ocel_event_log["events"].append(
                    self.get_grade_assignment_event_object(event, event_type)
                )

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

        # region RELATIONSHIPS
        relationships = []
        instance = self.fetch_course_module_by_id(event["objectid"])

        if instance:
            instance_id = instance["instance"]
            if event_type_enum == EventType.UPDATED:
                delete_time = self.deleted_items.get(instance_id)
                if delete_time is not None and event["timecreated"] > delete_time:
                    return None

            relationships.append(
                get_formatted_relationship(
                    self.object_type,
                    instance_id,
                    f"{event_type_enum.value.qualifier} {self.object_type.value.name}",
                )
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

        if event_type_enum == EventType.CREATED:
            files = self.fetch_assignment_files_by_context_id(event["contextid"])
            if files:
                for file in files:
                    relationships.append(
                        get_formatted_relationship(
                            ObjectEnum.FILES,
                            file["id"],
                            "Contains file",
                        )
                    )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_assign_create_event_object(self, event, assign):
        event_type = get_module_event_type_name(self.object_type, EventType.CREATED)
        attributes = build_attributes(event, self.related_event_columns["log"])

        result = {
            "id": get_formatted_event_id(
                EventType.CREATED, self.object_type, event["id"]
            ),
            "type": event_type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.ASSIGN,
                assign["id"],
                f"{EventType.CREATED.value.qualifier} {self.object_type.value.name}",
            )
        ]

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.COURSE,
                assign["course"],
                "Created in course",
            )
        )

        calendar_events = self.fetch_related_calendar_events(
            ObjectEnum.ASSIGN.value.module_name, assign["id"]
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

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Created by user",
            )
        )

        files = self.fetch_assignment_files_by_context_id(event["contextid"])
        if files:
            for file in files:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.FILES,
                        file["id"],
                        "Contains file",
                    )
                )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

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

        user_row = self.fetch_import_assign_user_log(row["instance"])
        if user_row:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.USER, user_row["loggeduser"], "Imported by user"
                )
            )

        context = self.fetch_assignment_context_id(row["id"])
        if context:
            files = self.fetch_assignment_files_by_context_id(context["id"])
            if files:
                for file in files:
                    relationships.append(
                        get_formatted_relationship(
                            ObjectEnum.FILES, file["id"], "Contains file"
                        )
                    )

        if relationships:
            result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_viewed_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        relationships = []
        id_ = event["objectid"]
        qualifier = "Viewed by user"
        result = {
            "id": get_formatted_event_id(
                EventType.VIEWED, self.object_type, event["id"]
            ),
            "type": get_module_event_type_name(self.object_type, EventType.VIEWED),
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships.append(
            get_formatted_relationship(
                self.object_type,
                id_,
                f"Viewed {self.object_type.value.name}",
            )
        )

        relationships.append(
            get_formatted_relationship(ObjectEnum.USER, event["userid"], qualifier)
        )

        if self.has_course_relation:
            course_relationship = self.get_course_relation(EventType.VIEWED, id_)
            if course_relationship:
                relationships.append(course_relationship)

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_submit_assignment_event_object(self, event):
        submission = self.fetch_submission(event["objectid"])
        if submission is None:
            return None

        assign = self.fetch_assign_by_submission(submission["assignment"])
        if assign is None:
            return None

        if assign["teamsubmission"] == 1 and submission["groupid"] == 0:
            return None

        event_type = (
            "submit_individual_assign"
            if assign["teamsubmission"] == 0
            else "submit_group_assign"
        )
        type_abbr = "sub_ind" if assign["teamsubmission"] == 0 else "sub_grp"
        user_qualifier = (
            "Submitted by"
            if assign["teamsubmission"] == 0
            else "Submitted by on behalf of the group"
        )
        assign_qualifier = "Submits assignment"
        file_qualifier = "Submitted file"
        group_qualifier = "Submitted by group"
        course_qualifier = "Submited assignment in course"

        if submission["status"] == "draft":
            return None
        
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": f'evt_assign_{type_abbr}_{event["id"]}',
            "type": event_type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.ASSIGN,
                assign["id"],
                assign_qualifier,
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                user_qualifier,
            ),
            get_formatted_relationship(
                ObjectEnum.COURSE,
                assign["course"],
                course_qualifier,
            ),
        ]

        files = self.fetch_assignment_files(event["objectid"])
        if files:
            for file in files:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.FILES,
                        file["id"],
                        file_qualifier,
                    )
                )

        if assign["teamsubmission"] == 1:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.GROUP,
                    submission["groupid"],
                    group_qualifier,
                )
            )

            group_members = self.fetch_group_members_by_id(submission["groupid"])
            if group_members:
                for member in group_members:
                    status_row = self.fetch_submission_by_user_id(
                        event["objectid"], member["userid"]
                    )
                    if status_row:
                        if status_row["status"] == "submitted":
                            member_qualifier = "Submitted by system"

                        relationships.append(
                            get_formatted_relationship(
                                ObjectEnum.USER,
                                member["userid"],
                                member_qualifier,
                            )
                        )

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_resubmit_assignment_event_object(self, event):
        submission = self.fetch_submission(event["objectid"])
        if submission is None:
            return None

        assign = self.fetch_assign_by_submission(submission["assignment"])
        if assign is None:
            return None

        if assign["teamsubmission"] == 1 and submission["groupid"] == 0:
            return None

        event_type = (
            "resubmit_individual_assign"
            if assign["teamsubmission"] == 0
            else "resubmit_group_assign"
        )
        type_abbr = "resub_ind_" if assign["teamsubmission"] == 0 else "resub_grp_"
        user_qualifier = (
            "Resubmitted by"
            if assign["teamsubmission"] == 0
            else "Resubmitted by on behalf of the group"
        )
        assign_qualifier = "Resubmits assignment"
        file_qualifier = "Resubmitted file"
        group_qualifier = "Resubmitted by group"
        course_qualifier = "Reubmitted assignment in course"

        if submission["status"] == "draft":
            return None
        
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": f'evt_assign_{type_abbr}_{event["id"]}',
            "type": event_type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.ASSIGN,
                assign["id"],
                assign_qualifier,
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                user_qualifier,
            ),
            get_formatted_relationship(
                ObjectEnum.COURSE,
                assign["course"],
                course_qualifier,
            ),
        ]

        files = self.fetch_assignment_files(event["objectid"])
        if files:
            for file in files:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.FILES,
                        file["id"],
                        file_qualifier,
                    )
                )

        if assign["teamsubmission"] == 1:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.GROUP,
                    submission["groupid"],
                    group_qualifier,
                ),
            )

            group_members = self.fetch_group_members_by_id(submission["groupid"])
            if group_members:
                for member in group_members:
                    status_row = self.fetch_submission_by_user_id(
                        event["objectid"], member["userid"]
                    )
                    if status_row:
                        if status_row["status"] == "submitted":
                            member_qualifier = "Resubmitted by system"

                        relationships.append(
                            get_formatted_relationship(
                                ObjectEnum.USER,
                                member["userid"],
                                member_qualifier,
                            )
                        )

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def get_grade_assignment_event_object(self, event, event_type: EventType):
        event_qualifier = "evt_set"
        if event_type == EventType.UPDATED:
            event_qualifier = "evt_upd"

        attributes = build_attributes(event, self.related_event_columns["log"])

        result = {
            "id": f'{event_qualifier}_grade_{event["id"]}',
            "type": f"{event_type.value.name}_grade",
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Graded by user",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["relateduserid"],
                "Received by user",
            ),
        ]

        assign_grade = self.fetch_assign_grade_by_id(event["objectid"])
        if assign_grade:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.ASSIGN,
                    assign_grade["assignment"],
                    "Pertains to assignment",
                ),
            )

            assign = self.fetch_module_by_id(assign_grade["assignment"])
            if assign:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.COURSE,
                        assign["course"],
                        "Graded in course",
                    )
                )

            grade = self.fetch_grade_grades_by(
                assign_grade["assignment"],
                event["timecreated"],
                event["relateduserid"],
                event["userid"],
            )
            if grade:
                final_grade = float(grade.get("finalgrade"))
                if final_grade is not None:
                    result["attributes"].append({"name": "grade", "value": final_grade})

        feedback_files = self.fetch_feedback_file_by_grade(event["objectid"])
        if feedback_files:
            for feedback_file in feedback_files:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.FILES,
                        feedback_file["id"],
                        "Contains feedback file",
                    )
                )

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def fetch_assign_event_by_ids(self, course_module_id, action_type):
        filter_conditions = [
            self.Log.action == action_type,
            self.Log.objectid == course_module_id,
            self.Log.objecttable == "course_modules",
        ]
        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events[0] if events else None

    def fetch_import_assign_user_log(self, assign_id):
        filter_conditions = [
            self.GradeItemsHistory.source == "restore",
            self.GradeItemsHistory.action == 1,
            self.GradeItemsHistory.itemmodule == "assign",
            self.GradeItemsHistory.iteminstance == assign_id,
        ]

        rows = self.db_service.query_object(self.GradeItemsHistory, filter_conditions)
        return rows[0] if rows else None

    def fetch_submitted_assignment_events(self):
        filter_conditions = [
            self.Log.action == "uploaded",
            self.Log.eventname == "\\assignsubmission_file\\event\\assessable_uploaded",
            self.Log.objecttable == "assign_submission",
        ]
        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_submission_by_user_id(self, object_id, user_id):
        assign_submission = self.db_service.Base.classes.mdl_assign_submission
        filter_conditions = [
            assign_submission.id == object_id,
            assign_submission.userid == user_id,
        ]
        rows = self.db_service.query_object(assign_submission, filter_conditions)
        return rows[0] if rows else None

    def fetch_submission(self, object_id):
        filter_conditions = [
            self.Assign_submission.id == object_id,
            not_(self.Assign_submission.status.like("new")),
        ]
        rows = self.db_service.query_object(self.Assign_submission, filter_conditions)
        return rows[0] if rows else None

    def fetch_assign_by_submission(self, assignment):
        filter_conditions = [self.object_class.id == assignment]
        assigns = self.db_service.query_object(self.object_class, filter_conditions)
        return assigns[0] if assigns else None

    def fetch_assignment_files(self, object_id):
        filter_conditions = [
            self.Files.itemid == object_id,
            self.Files.component == "assignsubmission_file",
            self.Files.filearea == "submission_files",
            not_((self.Files.filename.like(".")) | (self.Files.filename.like(""))),
        ]
        rows = self.db_service.query_object(self.Files, filter_conditions)
        return rows if rows else None

    def fetch_assignment_files_by_context_id(self, context_id):
        filter_conditions = [
            self.Files.contextid == context_id,
            self.Files.component == "mod_assign",
            not_((self.Files.filename.like(".")) | (self.Files.filename.like(""))),
        ]
        rows = self.db_service.query_object(self.Files, filter_conditions)
        return rows if rows else None

    def fetch_assignment_context_id(self, instance_id):
        filter_conditions = [
            self.Context.instanceid == instance_id,
            self.Context.contextlevel == 70,
        ]
        rows = self.db_service.query_object(self.Context, filter_conditions)
        return rows[0] if rows else None

    def fetch_group_members_by_id(self, group_id):
        group_members = self.db_service.Base.classes.mdl_groups_members

        filter_conditions = [group_members.groupid == group_id]
        rows = self.db_service.query_object(group_members, filter_conditions)
        return rows if rows else None

    def fetch_course_module_by_id(self, course_module_id):
        course_modules = self.db_service.query_object(
            self.CourseModule, [self.CourseModule.id == course_module_id]
        )
        return course_modules[0] if course_modules else None

    def fetch_course_module_by_instance(self, instance, module_id):
        filter_conditions = [
            self.CourseModule.instance == instance,
            self.CourseModule.module == module_id,
        ]
        course_modules = self.db_service.query_object(
            self.CourseModule, filter_conditions
        )
        return course_modules[0] if course_modules else None

    def fetch_grade_assignment_events(self):
        filter_conditions = [
            self.Log.action == "graded",
            self.Log.target == "submission",
            self.Log.objecttable == "assign_grades",
        ]
        rows = self.db_service.query_object(
            self.Log,
            filter_conditions,
            sort_by=[("timecreated", "asc"), ("objectid", "asc")],
        )
        return rows if rows else None

    def fetch_assign_submission_fil_by_id(self, object_id):
        assign_sub_file = self.db_service.Base.classes.mdl_assignsubmission_file
        filter_conditions = [assign_sub_file.id == object_id]
        rows = self.db_service.query_object(assign_sub_file, filter_conditions)
        return rows[0] if rows else None

    def fetch_assign_submission_by_id(self, object_id):
        assign_sub = self.db_service.Base.classes.mdl_assign_submission
        filter_conditions = [assign_sub.id == object_id]
        rows = self.db_service.query_object(assign_sub, filter_conditions)
        return rows[0] if rows else None

    def fetch_assign_grade_by_id(self, object_id):
        table = self.db_service.Base.classes.mdl_assign_grades
        filter_conditions = [table.id == object_id]
        rows = self.db_service.query_object(table, filter_conditions)
        return rows[0] if rows else None

    def fetch_grade_grades_by(
        self, assignment_id, time_created, related_user_id, user_id
    ):
        grade_items = self.db_service.Base.classes.mdl_grade_items
        filter_conditions = [grade_items.iteminstance == assignment_id]
        grade_rows = self.db_service.query_object(grade_items, filter_conditions)
        if grade_rows is None or len(grade_rows) == 0:
            return None

        grade_grades_history = self.db_service.Base.classes.mdl_grade_grades_history
        filter_conditions = [
            grade_grades_history.itemid == grade_rows[0]["id"],
            grade_grades_history.userid == related_user_id,
            grade_grades_history.timemodified >= (time_created - 5),
            grade_grades_history.timemodified < (time_created + 5),
            (
                grade_grades_history.loggeduser == user_id
                or grade_grades_history.usermodified == user_id
            ),
        ]
        rows = self.db_service.query_object(grade_grades_history, filter_conditions)
        return rows[0] if rows else None

    def fetch_feedback_file_by_grade(self, assign_grade_id):
        filter_conditions = [
            self.Files.itemid == assign_grade_id,
            self.Files.component == "assignfeedback_file",
            self.Files.filearea == "feedback_files",
            not_(
                or_(
                    self.Files.filename.like("."),
                    self.Files.filename.like(""),
                )
            ),
        ]
        rows = self.db_service.query_object(self.Files, filter_conditions)
        return rows if rows else None

    def fetch_assigns(self):
        assigns = self.db_service.query_object(
            self.object_class, sort_by=[("timemodified", "asc")]
        )
        return assigns if assigns else None

    def fetch_module_by_id(self, module_id):
        filter_conditions = [self.object_class.id == module_id]
        rows = self.db_service.query_object(
            self.object_class, filter_conditions, sort_by=[("timemodified", "asc")]
        )
        return rows[0] if rows else None
