from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.transformers.base import Base


class Assign(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.ASSIGN
        self.object_class = self.db_service.Base.classes.mdl_assign
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True

        self.Context = self.db_service.Base.classes.mdl_context
