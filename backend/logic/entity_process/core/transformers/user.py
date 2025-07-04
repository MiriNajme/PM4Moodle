from logic.model.object_enum import ObjectEnum
from logic.utils.object_utils import get_object_key
from logic.entity_process.core.transformers.base import Base


class User(Base):
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
                {
                    "name": "id",
                    "time": "1970-01-01T00:00:00Z",
                    "value": get_object_key(self.object_type, "unknown")
                },
                {
                    "name": "username", 
                    "time": "1970-01-01T00:00:00Z",
                    "value": "unknown"
                },
                {
                    "name": "firstname",
                    "time": "1970-01-01T00:00:00Z",
                    "value": "Unknown"
                },
            ],
        }

        list_of_objects.append(unknown_user)
        system_user = {
            "id": get_object_key(self.object_type, "system"),
            "type": self.object_type.value.name,
            "attributes": [
                {
                    "name": "id", 
                    "time": "1970-01-01T00:00:00Z",
                    "value": get_object_key(self.object_type, "system")
},
                {
                    "name": "username",
                    "time": "1970-01-01T00:00:00Z",
                    "value": "system"
},
                {
                    "name": "firstname",
                    "time": "1970-01-01T00:00:00Z",
                    "value": "system"
                },
            ],
        }

        list_of_objects.append(system_user)
        self.ocel_event_log["objects"].extend(list_of_objects)
