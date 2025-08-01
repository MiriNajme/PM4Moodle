from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.extractors.base import Base


class File(Base):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.FILE
        self.object_class = self.db_service.Base.classes.mdl_resource
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

        if "create_file" in events or "import_file" in events:
            self.add_create_import_events()

        if "delete_file" in events:
            self.add_delete_events()

        if "update_file" in events:
            self.add_update_events()

        if "view_file" in events:
            self.add_view_events()
