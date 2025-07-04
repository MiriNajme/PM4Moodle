from logic.model.object_enum import ObjectEnum
from logic.utils.date_utils import format_date
from logic.utils.object_utils import convert_value_type
from logic.entity_process.core.transformers.base import Base


class GradeHistory(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.GRADES_HISTORY
        self.object_class = self.db_service.Base.classes.mdl_grade_grades_history
        self.sort_by = [("timemodified", "asc")]

    def get_attributes(self, row, columns):
        return [
            {
                "name": col["name"],
                "value": convert_value_type(row[col["name"]]),
                "time": format_date(row["timemodified"]),
            }
            for col in columns
        ]
