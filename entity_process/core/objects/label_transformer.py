from model.object_enum import ObjectEnum
from entity_process.core.objects.base_transformer import BaseTransformer


class LabelTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.LABEL
        self.object_class = self.db_service.Base.classes.mdl_label
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True
