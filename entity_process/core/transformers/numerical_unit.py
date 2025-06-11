from model.object_enum import ObjectEnum
from entity_process.core.transformers.base import Base
from utils.object_utils import convert_value_type


class NumericalUnit(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.NUMERICAL_UNIT
        self.object_class = self.db_service.Base.classes.mdl_question_numerical_units
        self.has_relationships = False

    def get_attributes(self, row, columns):
        attributes = []

        for col in columns:
            attributes.append(
                {
                    "name": col["name"],
                    "value": convert_value_type(row[col["name"]]),
                }
            )

        return attributes
