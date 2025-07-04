from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.transformers.base import Base


class MatchQuestionSubQuestion(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.MATCH_QUESTION_SUB_QUESTION
        self.object_class = self.db_service.Base.classes.mdl_qtype_match_subquestions
        self.has_relationships = False
