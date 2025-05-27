from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key
from utils.date_utils import format_date
from entity_process.core.objects.base_transformer import BaseTransformer


class FolderTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.FOLDER
        self.object_class = self.db_service.Base.classes.mdl_folder
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True

        self.CourseModule = self.db_service.Base.classes.mdl_course_modules
        self.Calendar_Event = self.db_service.Base.classes.mdl_event
        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log
