from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.extractors.base import Base


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

    def extractBy(self, events: list = None):
        if not events:
            self.extract()
            return

        self.module_id = self.db_service.fetch_module_id(
            self.object_type.value.module_name
        )

        if "create_page" in events or "import_page" in events:
            self.add_create_import_events()

        if "delete_page" in events:
            self.add_delete_events()

        if "update_page" in events:
            self.add_update_events()

        if "view_page" in events:
            self.add_view_events()
