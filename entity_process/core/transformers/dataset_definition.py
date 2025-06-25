from model.object_enum import ObjectEnum
from entity_process.core.transformers.base import Base
from utils.object_utils import convert_value_type


class DatasetDefinition(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.DATASET_DEFINITION
        self.object_class = self.db_service.Base.classes.mdl_question_dataset_definitions
        self.has_relationships = False

    def get_attributes(self, row, columns):
        attributes = []

        for col in columns:
            attributes.append(
                {
                    "name": col["name"],
                    "value": convert_value_type(row[col["name"]]),
                    "time": "1970-01-01T00:00:00Z",
                }
            )

        return attributes
