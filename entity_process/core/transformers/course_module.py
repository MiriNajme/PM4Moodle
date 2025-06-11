from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key, relation_formatter
from entity_process.core.transformers.base import Base


class CourseModule(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.COURSE_MODULE
        self.object_class = self.db_service.Base.classes.mdl_course_modules
        self.has_relationships = True

        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log

    def get_relationship(self, row):
        relationships = []
        tag_instances = self.fetch_course_module_tag_instances(row["id"])

        if tag_instances:
            for tag_instance in tag_instances:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.TAG_INSTANCE, tag_instance["id"]
                        ),
                        "qualifier": "Course module has tag instance",
                        "from": tag_instance["from"],
                        "to": tag_instance["to"],
                    }
                )

        return relationships

    def fetch_course_module_tag_instances(self, course_module_id):
        added_tags = self.fetch_from_log_event(
            course_module_id, objecttable="tag_instance", action="added"
        )
        removed_tags = self.fetch_from_log_event(
            course_module_id, objecttable="tag_instance", action="removed"
        )
        instances = relation_formatter(added_tags, removed_tags, "objectid")
        return instances if instances else None

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
