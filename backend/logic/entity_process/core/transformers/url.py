from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.transformers.base import Base


class Url(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.URL
        self.object_class = self.db_service.Base.classes.mdl_url
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True
