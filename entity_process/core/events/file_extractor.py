from model.event_types import EventType
from model.object_enum import ObjectEnum
from entity_process.core.events.base_extractor import BaseExtractor


class FileExtractor(BaseExtractor):

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

    def get_viewed_event_object(self, event, ids):
        result = super().get_viewed_event_object(event, ids)

        course_relationships = self.get_course_relation(
            EventType.VIEWED, event["objectid"]
        )
        if course_relationships:
            result["relationships"].append(course_relationships)

        return result
