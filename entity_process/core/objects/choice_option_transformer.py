from model.object_enum import ObjectEnum
from utils.date_utils import format_date
from entity_process.core.objects.base_transformer import BaseTransformer


class ChoiceOptionTransformer(BaseTransformer):
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
