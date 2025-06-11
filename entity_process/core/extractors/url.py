from model.object_enum import ObjectEnum
from entity_process.core.extractors.base import Base


class Url(Base):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.URL
        self.object_class = self.db_service.Base.classes.mdl_url
        self.has_view_events = True
