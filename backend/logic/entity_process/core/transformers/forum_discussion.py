from logic.model.object_enum import ObjectEnum
from logic.utils.date_utils import format_date
from logic.utils.object_utils import get_object_key
from logic.entity_process.core.transformers.base import Base


class ForumDiscussion(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.FORUM_DISCUSSION
        self.object_class = self.db_service.Base.classes.mdl_forum_discussions
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True

        self.POST = self.db_service.Base.classes.mdl_forum_posts

    def get_relationship(self, row):
        relationships = super().get_relationship(row)

        posts = self.fetch_posts_by_discussion_id(row["id"])
        if posts:
            for post in posts:
                relationships.append(
                    {
                        "objectId": get_object_key(ObjectEnum.FORUM_POST, post["id"]),
                        "qualifier": "Has post",
                        "from": format_date(post["created"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )

        return relationships

    def fetch_posts_by_discussion_id(self, discussion_id):
        filter = [self.POST.discussion == discussion_id]
        posts = self.db_service.query_object(
            self.POST, filter, sort_by=[("created", "asc")]
        )
        return posts if posts else None
