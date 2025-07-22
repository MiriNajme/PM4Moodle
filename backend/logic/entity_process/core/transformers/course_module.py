from logic.model.object_enum import ObjectEnum
from logic.utils.object_utils import get_object_key, relation_formatter
from logic.entity_process.core.transformers.base import Base


class CourseModule(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.COURSE_MODULE
        self.object_class = self.db_service.Base.classes.mdl_course_modules
        self.has_relationships = True

        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log

    def get_relationship(self, row):
        relationships = []
        return relationships

    def fetch_from_log_event(
        self,
        event_id,
        action="created",
        objecttable=None,
        sort_by=[("timecreated", "asc")],
    ):
        filter_conditions = [
            self.Log.other.like('%"itemtype":"course_modules"%'),
            (
                self.Log.other.like('%"itemid":"' + str(event_id) + '"%')
                | self.Log.other.like('%"itemid":' + str(event_id) + "%")
            ),
            self.Log.action == action,
            self.Log.objecttable == objecttable,
        ]
        result = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=sort_by
        )
        return result
