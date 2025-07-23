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

        self.GradeItems = self.db_service.Base.classes.mdl_grade_items
        self.Context = self.db_service.Base.classes.mdl_context

    def get_relationship(self, row):
        relationships = []
        # region RELATED TO COURSE MODULE
        course_modules = self.db_service.fetch_course_modules_by_ids(
            row["id"], self.module_id
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
        # endregion RELATED TO COURSE MODULE

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
