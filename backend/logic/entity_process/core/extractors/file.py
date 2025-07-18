from logic.model.event_types import EventType
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

    def extractBy(self, events: list = None):
        if not events:
            self.extract()
            return

        if "create_file" in events or "import_file" in events:
            self.add_create_import_events()

        if "delete_file" in events:
            self.add_delete_events()

        if "update_file" in events:
            self.add_update_events()

        if "view_file" in events:
            self.add_view_events()

    def get_viewed_event_object(self, event):
        result = super().get_viewed_event_object(event)

        course_relationships = self.get_course_relation(
            EventType.VIEWED, event["objectid"]
        )
        if course_relationships:
            result["relationships"].append(course_relationships)

        return result
