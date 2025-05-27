from model.object_enum import ObjectEnum
from entity_process.core.objects.base_transformer import BaseTransformer


class TagInstanceTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.TAG_INSTANCE
        self.object_class = self.db_service.Base.classes.mdl_tag_instance
        self.sort_by = [("timecreated", "asc")]

        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log
