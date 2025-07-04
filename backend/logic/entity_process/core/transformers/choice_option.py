from logic.model.object_enum import ObjectEnum
from logic.utils.date_utils import format_date
from logic.entity_process.core.transformers.base import Base


class ChoiceOption(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.OPTION
        self.object_class = self.db_service.Base.classes.mdl_choice_options
        self.sort_by = [("timemodified", "asc")]

    def get_attributes(self, row, columns):
        return [
            {
                "name": col["name"],
                "value": row[col["name"]],
                "time": format_date(row["timemodified"]),
            }
            for col in columns
        ]
