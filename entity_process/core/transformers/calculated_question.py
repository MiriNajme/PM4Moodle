from model.object_enum import ObjectEnum
from entity_process.core.transformers.base import Base


class CalculatedQuestion(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.CALCULATED_QUESTION
        self.object_class = self.db_service.Base.classes.mdl_question_calculated
        self.has_relationships = False
