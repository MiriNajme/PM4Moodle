from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key, compare_history_logs
from utils.date_utils import format_date
from entity_process.core.objects.base_transformer import BaseTransformer


class TagTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.TAG
        self.object_class = self.db_service.Base.classes.mdl_tag
        self.has_relationships = True

        self.Tag_instance = self.db_service.Base.classes.mdl_tag_instance
        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log

    def get_attributes(self, row, columns):
        attributes = super().get_attributes(row, columns)

        for history_row in self.get_tag_update_history(row["id"]):
            attributes.append(
                {
                    "name": history_row["name"],
                    "value": history_row["value"],
                    "time": history_row["time"],
                }
            )

        attributes = sorted(attributes, key=lambda x: x["name"])
        return attributes

    def get_relationship(self, row):
        relationships = []
        tag_instances = self.fetch_tag_instances_tags(row["id"])

        if tag_instances:
            for tag_instance in tag_instances:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.TAG_INSTANCE, tag_instance["id"]
                        ),
                        "qualifier": "An instance of tag",
                        "from": format_date(tag_instance["timecreated"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )

        return relationships

    def fetch_tag_instances_tags(self, tag_id):
        instances = self.db_service.query_object(
            self.Tag_instance, filters=[self.Tag_instance.tagid == tag_id]
        )
        return instances if instances else None

    def get_tag_update_history(self, tag_id):
        filter_conditions = [
            (
                self.Log.eventname.like("%tag_created%")
                | self.Log.eventname.like("%tag_updated%")
            ),
            self.Log.objectid == tag_id,
        ]
        rows = self.db_service.query_object(
            self.Log,
            filter_conditions,
            sort_by=[("objectid", "asc"), ("timecreated", "asc")],
        )

        return compare_history_logs(rows)
