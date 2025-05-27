from model.object_enum import ObjectEnum
from entity_process.core.events.base_extractor import BaseExtractor


class LabelExtractor(BaseExtractor):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.LABEL
        self.object_class = self.db_service.Base.classes.mdl_label
        self.has_course_relation = True
