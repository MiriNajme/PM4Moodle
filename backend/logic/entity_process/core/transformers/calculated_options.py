from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.transformers.base import Base


class CalculatedOptions(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.CALCULATED_OPTION
        self.object_class = self.db_service.Base.classes.mdl_question_calculated_options
        self.has_relationships = False
