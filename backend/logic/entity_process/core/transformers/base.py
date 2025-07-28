from abc import ABC
from logic.model.object_enum import ObjectEnum
from logic.utils.object_utils import get_object_key
from logic.utils.date_utils import format_date


class Base(ABC):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        self.db_service = db_service
        self.related_object_columns = related_object_columns
        self.ocel_event_log = ocel_event_log
        self.object_type: ObjectEnum = None
        self.object_class = None
        self.sort_by = None
        self.has_relationships = None
        self.module_id = 0

    def transform(self):
        self.module_id = self.db_service.fetch_module_id(
            self.object_type.value.module_name
        )
        records = self.db_service.query_object(self.object_class, sort_by=self.sort_by)

        if not records:
            return

        self.process_records(records)

    def process_records(self, records):
        list_of_objects = []

        columns = self.get_columns()
        if not columns:
            return

        for row in records:
            attributes = self.get_attributes(row, columns)

            row_obj = {
                "id": get_object_key(self.object_type, row["id"]),
                "type": self.object_type.value.name,
                "attributes": attributes,
            }

            if self.has_relationships:
                relationships = self.get_relationship(row)

                if relationships:
                    row_obj["relationships"] = relationships

            list_of_objects.append(row_obj)

        self.ocel_event_log["objects"].extend(list_of_objects)

    def get_attributes(self, row, columns):
        return [
            {
                "name": col["name"],
                "time": "1970-01-01T00:00:00Z",
                "value": row.get(col["name"], None),
            }
            for col in columns
        ]

    def get_columns(self):
        columns = self.related_object_columns.get(self.object_type.value.name)

        if not columns:
            print(
                f"[WARN] Skipping '{self.object_type.value.name}' processor due to missing metadata."
            )
            return None

        return columns

    def get_relationship(self, row):
        return []