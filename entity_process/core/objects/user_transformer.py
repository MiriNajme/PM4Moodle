from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key
from entity_process.core.objects.base_transformer import BaseTransformer


class UserTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.USER
        self.object_class = self.db_service.Base.classes.mdl_user

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
            list_of_objects.append(row_obj)

        unknown_user = {
            "id": get_object_key(self.object_type, "unknown"),
            "type": self.object_type.value.name,
            "attributes": [
                {"name": "id", "value": get_object_key(self.object_type, "unknown")},
                {"name": "username", "value": "unknown"},
                {"name": "firstname", "value": "Unknown"},
            ],
        }

        list_of_objects.append(unknown_user)
        self.ocel_event_log["objects"].extend(list_of_objects)
