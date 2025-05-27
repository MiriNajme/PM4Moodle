from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key
from utils.date_utils import format_date
from entity_process.core.objects.base_transformer import BaseTransformer


class SectionTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.SECTION
        self.object_class = self.db_service.Base.classes.mdl_course_sections
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True
        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log
        self.TaskAdhoc = self.db_service.Base.classes.mdl_task_adhoc
        self.CourseModule = self.db_service.Base.classes.mdl_course_modules

    def get_relationship(self, row):
        relationships = []
        if row["sequence"]:
            course_modules = self.fetch_section_course_modules(row["id"])
            if course_modules:
                for course_module in course_modules:
                    to = "9999-12-31T23:59:59.999Z"

                    if course_module["deletioninprogress"] == 1:
                        course_module_delete_row = self.fetch_course_module_delete_log(
                            course_module["id"]
                        )
                        if course_module_delete_row:
                            to = format_date(course_module_delete_row["timecreated"], 1)

                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.COURSE_MODULE, course_module["id"]
                            ),
                            "qualifier": "Section contains course module",
                            "from": format_date(course_module["added"]),
                            "to": to,
                        }
                    )

        return relationships

    def fetch_section_course_modules(self, section_id):
        course_modules = self.db_service.query_object(
            self.CourseModule, filters=[self.CourseModule.section == section_id]
        )
        return course_modules if course_modules else None

    def fetch_course_module_delete_log(self, course_module_id):
        filter_conditions = [
            self.TaskAdhoc.classname.like("%course_delete_modules%"),
            self.TaskAdhoc.customdata.like('%"id":"' + str(course_module_id) + '"%'),
        ]
        rows = self.db_service.query_object(
            self.TaskAdhoc, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return rows[0] if rows else None
