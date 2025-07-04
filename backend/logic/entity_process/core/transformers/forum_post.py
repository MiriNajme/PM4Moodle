from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.transformers.base import Base


class ForumPost(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.FORUM_POST
        self.object_class = self.db_service.Base.classes.mdl_forum_posts
        self.sort_by = [("modified", "asc")]
        self.has_relationships = True
