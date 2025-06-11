from model.object_enum import ObjectEnum
from entity_process.core.extractors.base import Base


class Page(Base):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.PAGE
        self.object_class = self.db_service.Base.classes.mdl_page
        self.has_view_events = True
