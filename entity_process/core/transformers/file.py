from model.object_enum import ObjectEnum
from entity_process.core.transformers.base import Base


class File(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.FILE
        self.object_class = self.db_service.Base.classes.mdl_resource
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True
