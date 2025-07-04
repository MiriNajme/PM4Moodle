from logic.model.object_enum import ObjectEnum
from logic.utils.date_utils import format_date
from logic.utils.object_utils import get_object_key
from logic.entity_process.core.transformers.base import Base


class Forum(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.FORUM
        self.object_class = self.db_service.Base.classes.mdl_forum
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True

        self.Discussion = self.db_service.Base.classes.mdl_forum_discussions

    def get_relationship(self, row):
        relationships = super().get_relationship(row)

        discussions = self.fetch_discussions_by_forum_id(row["id"])
        if discussions:
            for discussion in discussions:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.FORUM_DISCUSSION, discussion["id"]
                        ),
                        "qualifier": "Has discussion",
                        "from": format_date(discussion["timemodified"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )

        return relationships

    def fetch_discussions_by_forum_id(self, forum_id):
        filter = [self.Discussion.forum == forum_id]
        discussions = self.db_service.query_object(self.Discussion, filter)
        return discussions if discussions else None
