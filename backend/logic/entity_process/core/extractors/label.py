from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.extractors.base import Base


class Label(Base):

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

    def extractBy(self, events: list = None):
        if not events:
            self.extract()
            return

        if "create_label" in events or "import_label" in events:
            self.add_create_import_events()

        if "delete_label" in events:
            self.add_delete_events()

        if "update_label" in events:
            self.add_update_events()
