from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.extractors.base import Base


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
        self.has_course_relation = True

    def extractBy(self, courses: list = None, events: list = None):
        if not events:
            self.extract(courses)
            return

        self.selected_courses = courses
        
        self.module_id = self.db_service.fetch_module_id(
            self.object_type.value.module_name
        )

        if "create_url" in events or "import_url" in events:
            self.add_create_import_events()

        if "delete_url" in events:
            self.add_delete_events()

        if "update_url" in events:
            self.add_update_events()

        if "view_url" in events:
            self.add_view_events()
