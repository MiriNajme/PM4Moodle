from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.transformers.base import Base
from logic.utils.date_utils import format_date
from logic.utils.object_utils import convert_value_type


class Quiz(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.QUIZ
        self.object_class = self.db_service.Base.classes.mdl_quiz
        self.sort_by = [("timecreated", "asc")]
        self.has_relationships = True

    def get_attributes(self, row, columns):
        attributes = []

        for col in columns:
            attributes.append(
                {
                    "name": col["name"],
                    "value": convert_value_type(row[col["name"]]),
                    "time": format_date(row["timecreated"]),
                }
            )

        return attributes
