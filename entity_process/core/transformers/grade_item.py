from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key, convert_value_type, check_key_existence
from utils.date_utils import format_date
from entity_process.core.transformers.base import Base


class GradeItem(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.GRADE_ITEM
        self.object_class = self.db_service.Base.classes.mdl_grade_items
        self.sort_by = [("timemodified", "asc")]

        self.GradeItemsHistory = self.db_service.Base.classes.mdl_grade_items_history

    def process_records(self, records):
        list_of_objects = []

        columns = self.get_columns()
        if not columns:
            return

        for row in records:
            history_rows = self.get_grade_item_update_history(row)
            attributes = self.get_attributes(row, columns, history_rows)

            row_obj = {
                "id": get_object_key(self.object_type, row["id"]),
                "type": self.object_type.value.name,
                "attributes": attributes,
            }

            list_of_objects.append(row_obj)

        self.ocel_event_log["objects"].extend(list_of_objects)

    def get_attributes(self, row, columns, history_rows):
        attributes = []

        for col in columns:
            attributes.append(
                {
                    "name": col["name"],
                    "value": convert_value_type(row[col["name"]]),
                    "time": format_date(row["timecreated"]),
                }
            )

        for history_row in history_rows:
            attributes.append(
                {
                    "name": history_row["name"],
                    "value": convert_value_type(history_row["value"]),
                    "time": format_date(history_row["time"]),
                }
            )

        attributes = sorted(attributes, key=lambda x: x["name"])
        return attributes

    def get_grade_item_update_history(self, grade_item):
        update_filter_conditions = [
            self.GradeItemsHistory.oldid == grade_item["id"],
        ]
        update_rows = self.db_service.query_object(
            self.GradeItemsHistory,
            update_filter_conditions,
            sort_by=[("timemodified", "asc")],
        )

        if not update_rows:
            return []

        result = []
        for row in update_rows:
            for key in row.keys():
                if not check_key_existence(
                    key, self.related_object_columns["grade_item"]
                ):
                    continue

                result.append(
                    {"name": key, "value": row[key], "time": row["timemodified"]}
                )

        return result
