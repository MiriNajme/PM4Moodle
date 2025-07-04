from logic.model.object_enum import ObjectEnum
from logic.utils.object_utils import get_object_key, relation_formatter
from logic.entity_process.core.transformers.base import Base


class Group(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.GROUP
        self.object_class = self.db_service.Base.classes.mdl_groups
        self.has_relationships = True

        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log

    def get_relationship(self, row):
        relationships = []
        users = self.fetch_group_users(row["id"])

        if users:
            for user in users:
                qualifier = "User is a member of group"
                if user["to"] != "9999-12-31T23:59:59.999Z":
                    qualifier = "User was a member of group"

                relationships.append(
                    {
                        "objectId": get_object_key(ObjectEnum.USER, user["id"]),
                        "qualifier": qualifier,
                        "from": user["from"],
                        "to": user["to"],
                    }
                )

        return relationships

    def fetch_group_users(self, group_id):
        filter_conditions = [
            self.Log.target == "group_member",
            self.Log.objectid == group_id,
            self.Log.action == "added",
        ]
        filter_conditions2 = [
            self.Log.target == "group_member",
            self.Log.objectid == group_id,
            self.Log.action == "removed",
        ]

        added_users = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        removed_users = self.db_service.query_object(
            self.Log, filter_conditions2, sort_by=[("timecreated", "asc")]
        )

        users = relation_formatter(added_users, removed_users, "relateduserid")
        return users if users else None
