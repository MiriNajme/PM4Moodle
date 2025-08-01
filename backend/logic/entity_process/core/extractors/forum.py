import json
from sqlalchemy import not_
from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.extractors.base import Base
from logic.utils.date_utils import format_date
from logic.utils.object_utils import get_object_key
from logic.utils.extractor_utils import (
    build_attributes,
    get_formatted_event_id,
    get_formatted_relationship,
)


class Forum(Base):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.FORUM
        self.object_class = self.db_service.Base.classes.mdl_forum
        self.has_course_relation = True

        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log
        self.Discussion = self.db_service.Base.classes.mdl_forum_discussions
        self.Post = self.db_service.Base.classes.mdl_forum_posts
        self.Files = self.db_service.Base.classes.mdl_files

    # region Extra event extraction process
    def extract(self, courses: list = None):
        super().extract(courses)

        self.subscribe_to_forum_events()
        self.unsubscribe_from_forum_events()
        self.add_discussion_events()
        self.view_discussion_events()
        self.delete_discussion_events()
        self.lock_unlock_discussion_events()
        self.subscribe_to_discussion_events()
        self.unsubscribe_from_discussion_events()
        self.upload_post_events()
        self.delete_post_events()
        self.edit_post_events()
        self.add_grade_rate_events()

    def extractBy(self, courses: list = None, events: list = None):
        if not events:
            self.extract(courses)
            return

        self.selected_courses = courses

        self.module_id = self.db_service.fetch_module_id(
            self.object_type.value.module_name
        )

        if "create_forum" in events or "import_forum" in events:
            self.add_create_import_events()

        if "delete_forum" in events:
            self.add_delete_events()

        if "update_forum" in events:
            self.add_update_events()

        if "view_forum" in events:
            self.add_view_events()

        if "subscribe_to_forum" in events:
            self.subscribe_to_forum_events()

        if "unsubscribe_from_forum" in events:
            self.unsubscribe_from_forum_events()

        if "add_discussion" in events:
            self.add_discussion_events()

        if "view_discussion" in events:
            self.view_discussion_events()

        if "delete_discussion" in events:
            self.delete_discussion_events()

        if "lock_discussion" in events or "unlock_discussion" in events:
            self.lock_unlock_discussion_events()

        if "subscribe_to_discussion" in events:
            self.subscribe_to_discussion_events()

        if "unsubscribe_from_discussion" in events:
            self.unsubscribe_from_discussion_events()

        if "upload_post" in events:
            self.upload_post_events()

        if "delete_post" in events:
            self.delete_post_events()

        if "edit_post" in events:
            self.edit_post_events()

        if (
            "set_grade" in events
            or "update_grade" in events
            or "rate_user_forum" in events
        ):
            self.add_grade_rate_events()

    def subscribe_to_forum_events(self):
        filter_conditions = [
            self.Log.action == "created",
            self.Log.target == "subscription",
            self.Log.objecttable == "forum_subscriptions",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_subscribe_to_forum_event_object(event)
                )

    def unsubscribe_from_forum_events(self):
        filter_conditions = [
            self.Log.action == "deleted",
            self.Log.target == "subscription",
            self.Log.objecttable == "forum_subscriptions",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_unsubscribe_from_forum_event_object(event)
                )

    def add_discussion_events(self):
        filter_conditions = [
            self.Log.action == "created",
            self.Log.target == "discussion",
            self.Log.objecttable == "forum_discussions",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_add_discussion_event_object(event)
                )

    def view_discussion_events(self):
        filter_conditions = [
            self.Log.action == "viewed",
            self.Log.target == "discussion",
            self.Log.objecttable == "forum_discussions",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_view_discussion_event_object(event)
                )

    def delete_discussion_events(self):
        filter_conditions = [
            self.Log.action == "deleted",
            self.Log.target == "discussion",
            self.Log.objecttable == "forum_discussions",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_delete_discussion_event_object(event)
                )

    def lock_unlock_discussion_events(self):
        filter_conditions = [
            self.Log.action == "updated",
            self.Log.target == "discussion_lock",
            self.Log.objecttable == "forum_discussions",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_lock_unlock_discussion_event_object(event)
                )

    def subscribe_to_discussion_events(self):
        filter_conditions = [
            self.Log.action == "created",
            self.Log.target == "discussion_subscription",
            self.Log.objecttable == "forum_discussion_subs",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_subscribe_to_discussion_event_object(event)
                )

    def unsubscribe_from_discussion_events(self):
        filter_conditions = [
            self.Log.action == "deleted",
            self.Log.target == "discussion_subscription",
            self.Log.objecttable == "forum_discussion_subs",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_unsubscribe_from_discussion_event_object(event)
                )

    def upload_post_events(self):
        events = self.fetch_upload_post_events()
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_upload_post_event_object(event)
                )

    def delete_post_events(self):
        filter_conditions = [
            self.Log.action == "deleted",
            self.Log.target == "post",
            self.Log.objecttable == "forum_posts",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_delete_post_event_object(event)
                )

    def edit_post_events(self):
        filter_conditions = [
            self.Log.action == "updated",
            self.Log.target == "post",
            self.Log.objecttable == "forum_posts",
        ]
        events = self.fetch_related_events(filter_conditions)
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_edit_post_event_object(event)
                )

    def add_grade_rate_events(self):
        object_ids = []
        events = self.fetch_grade_events()

        if events:
            for event in events:
                if event["objectid"] in object_ids:
                    event_type = EventType.UPDATED
                else:
                    object_ids.append(event["objectid"])
                    event_type = EventType.SET

                result = self.get_grade_rate_event_object(event, event_type)
                if result:
                    self.ocel_event_log["events"].append(result)

    # endregion Extra event extraction process

    # region Extra event object construction
    def get_deleted_module_event_object(self, event):
        result = super().get_deleted_module_event_object(event)

        # region RELATIONSHIPS
        instance = json.loads(event["customdata"])
        if instance:
            forum_id = instance["cms"][0]["instance"]
            forum_discussion = self.fetch_related_forum_discussions(forum_id)

            for discussion in forum_discussion:
                result["relationships"].append(
                    get_formatted_relationship(
                        ObjectEnum.FORUM_DISCUSSION,
                        discussion["id"],
                        "Deletes discussion",
                    )
                )

                posts = self.fetch_related_forum_posts(discussion["id"])
                for post in posts:
                    result["relationships"].append(
                        get_formatted_relationship(
                            ObjectEnum.FORUM_POST,
                            post["id"],
                            "Deletes post",
                        )
                    )

        return result

    def get_subscribe_to_forum_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.SUBSCRIBE_TO_FORUM,
                ObjectEnum.FORUM,
                event["id"],
            ),
            "type": EventType.SUBSCRIBE_TO_FORUM.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.SUBSCRIBE_TO_FORUM.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        instance = json.loads(event["other"])
        if instance is None:
            return result

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM,
                instance["forumid"],
                f"{EventType.SUBSCRIBE_TO_FORUM.value.qualifier} {ObjectEnum.FORUM.value.name}",
            ),
        )

        result["relationships"] = relationships
        # endregion

        return result

    def get_unsubscribe_from_forum_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.UNSUBSCRIBE_FROM_FORUM,
                ObjectEnum.FORUM,
                event["id"],
            ),
            "type": EventType.UNSUBSCRIBE_FROM_FORUM.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.UNSUBSCRIBE_FROM_FORUM.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        instance = json.loads(event["other"])
        if instance is None:
            return result

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM,
                instance["forumid"],
                f"{EventType.UNSUBSCRIBE_FROM_FORUM.value.qualifier} {ObjectEnum.FORUM.value.name}",
            ),
        )

        result["relationships"] = relationships
        # endregion

        return result

    def get_add_discussion_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.ADD_DISCUSSION, ObjectEnum.FORUM_DISCUSSION, event["id"]
            ),
            "type": EventType.ADD_DISCUSSION.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.FORUM_DISCUSSION,
                event["objectid"],
                f"{EventType.ADD_DISCUSSION.value.qualifier} {self.object_type.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.ADD_DISCUSSION.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        discussion = self.fetch_discussion_by_id(event["objectid"])
        if discussion:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.FORUM,
                    discussion["forum"],
                    f"Added in forum",
                ),
            )

            if discussion["groupid"] > 0:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.GROUP,
                        discussion["groupid"],
                        f"Added for group",
                    ),
                )

        result["relationships"] = relationships
        # endregion

        return result

    def get_view_discussion_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.VIEW_DISCUSSION, ObjectEnum.FORUM_DISCUSSION, event["id"]
            ),
            "type": EventType.VIEW_DISCUSSION.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.FORUM_DISCUSSION,
                event["objectid"],
                f"{EventType.VIEW_DISCUSSION.value.qualifier} {self.object_type.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.VIEW_DISCUSSION.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        discussion = self.fetch_discussion_by_id(event["objectid"])
        if discussion:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.FORUM,
                    discussion["forum"],
                    f"Viewed in forum",
                ),
            )

        result["relationships"] = relationships
        # endregion

        return result

    def get_delete_discussion_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.DELETE_DISCUSSION, ObjectEnum.FORUM_DISCUSSION, event["id"]
            ),
            "type": EventType.DELETE_DISCUSSION.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.FORUM_DISCUSSION,
                event["objectid"],
                f"{EventType.DELETE_DISCUSSION.value.qualifier} {ObjectEnum.FORUM_DISCUSSION.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Deletes by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        other = json.loads(event["other"]) if event.get("other") else {}
        if other:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.FORUM,
                    other["forumid"],
                    f"Deleted from forum",
                ),
            )

        result["relationships"] = relationships
        # endregion

        return result

    def get_lock_unlock_discussion_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])

        other = json.loads(event["other"]) if event.get("other") else {}
        status = other.get("status")
        if status == "locked":
            event_type = EventType.LOCK_DISCUSSION
        else:
            event_type = EventType.UNLOCK_DISCUSSION

        result = {
            "id": get_formatted_event_id(
                event_type, ObjectEnum.FORUM_DISCUSSION, event["id"]
            ),
            "type": event_type.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.FORUM_DISCUSSION,
                event["objectid"],
                f"{event_type.value.qualifier} {ObjectEnum.FORUM_DISCUSSION.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{event_type.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM,
                other["forumid"],
                f"Pertains to forum",
            ),
        )

        discussion = self.fetch_discussion_by_id(event["objectid"])
        if discussion and discussion["groupid"] > 0:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.GROUP,
                    discussion["groupid"],
                    f"Added for group",
                ),
            )

        result["relationships"] = relationships
        # endregion

        return result

    def get_subscribe_to_discussion_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.SUBSCRIBE_TO_DISCUSSION,
                ObjectEnum.FORUM_DISCUSSION,
                event["id"],
            ),
            "type": EventType.SUBSCRIBE_TO_DISCUSSION.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.SUBSCRIBE_TO_DISCUSSION.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        instance = json.loads(event["other"])
        if instance is None:
            return result

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM_DISCUSSION,
                instance["discussion"],
                f"{EventType.SUBSCRIBE_TO_DISCUSSION.value.qualifier} {ObjectEnum.FORUM_DISCUSSION.value.name}",
            ),
        )

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM,
                instance["forumid"],
                f"{EventType.SUBSCRIBE_TO_DISCUSSION.value.qualifier} {ObjectEnum.FORUM.value.name}",
            ),
        )

        result["relationships"] = relationships
        # endregion

        return result

    def get_unsubscribe_from_discussion_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.UNSUBSCRIBE_FROM_DISCUSSION,
                ObjectEnum.FORUM_DISCUSSION,
                event["id"],
            ),
            "type": EventType.UNSUBSCRIBE_FROM_DISCUSSION.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.UNSUBSCRIBE_FROM_DISCUSSION.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        instance = json.loads(event["other"])
        if instance is None:
            return result

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM_DISCUSSION,
                instance["discussion"],
                f"{EventType.UNSUBSCRIBE_FROM_DISCUSSION.value.qualifier} {ObjectEnum.FORUM_DISCUSSION.value.name}",
            ),
        )

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM,
                instance["forumid"],
                f"{EventType.UNSUBSCRIBE_FROM_DISCUSSION.value.qualifier} {ObjectEnum.FORUM.value.name}",
            ),
        )

        result["relationships"] = relationships
        # endregion

        return result

    def get_upload_post_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.UPLOAD_POST, ObjectEnum.FORUM_POST, event["id"]
            ),
            "type": EventType.UPLOAD_POST.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.FORUM_POST,
                event["objectid"],
                f"{EventType.UPLOAD_POST.value.qualifier} {self.object_type.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.UPLOAD_POST.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        post = self.fetch_post_by_id(event["objectid"])
        if post:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.FORUM_DISCUSSION,
                    post["discussion"],
                    f"Uploaded in discussion",
                ),
            )

            discussion = self.fetch_discussion_by_id(event["objectid"])
            if discussion:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.FORUM,
                        discussion["forum"],
                        f"Uploaded in forum",
                    ),
                )

        result["relationships"] = relationships
        # endregion

        return result

    def get_delete_post_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.DELETE_POST, ObjectEnum.FORUM_POST, event["id"]
            ),
            "type": EventType.DELETE_POST.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.FORUM_POST,
                event["objectid"],
                f"{EventType.DELETE_POST.value.qualifier} {self.object_type.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.DELETE_POST.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        post = self.fetch_post_by_id(event["objectid"])
        if post:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.FORUM_DISCUSSION,
                    post["discussion"],
                    f"Deleted from discussion",
                ),
            )

            discussion = self.fetch_discussion_by_id(event["objectid"])
            if discussion:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.FORUM,
                        discussion["forum"],
                        f"Deleted from forum",
                    ),
                )

        result["relationships"] = relationships
        # endregion

        return result

    def get_edit_post_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.EDIT_POST, ObjectEnum.FORUM_POST, event["id"]
            ),
            "type": EventType.EDIT_POST.value.type,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.FORUM_POST,
                event["objectid"],
                f"{EventType.EDIT_POST.value.qualifier} {self.object_type.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                f"{EventType.EDIT_POST.value.qualifier} by user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        post = self.fetch_post_by_id(event["objectid"])
        if post:
            relationships.append(
                get_formatted_relationship(
                    ObjectEnum.FORUM_DISCUSSION,
                    post["discussion"],
                    f"Edited in discussion",
                ),
            )

            discussion = self.fetch_discussion_by_id(event["objectid"])
            if discussion:
                relationships.append(
                    get_formatted_relationship(
                        ObjectEnum.FORUM,
                        discussion["forum"],
                        f"Edited in forum",
                    ),
                )

        result["relationships"] = relationships
        # endregion

        return result

    def get_grade_rate_event_object(self, event, event_type: EventType):
        event_qualifier = "evt_set"
        if event_type == EventType.UPDATED:
            event_qualifier = "evt_upd"

        attributes = build_attributes(event, self.related_event_columns["log"])

        instance = json.loads(event["other"])
        if instance is None:
            return None

        grade_item = self.fetch_grade_item_by_id(instance["itemid"])
        is_rating = False

        if "rating" in grade_item["itemname"]:
            is_rating = True
            if event_type == EventType.UPDATED:
                return None
            else:
                event_qualifier = f"evt_{EventType.RATE_USER_FORUM.value.abbr}"
                event_type = EventType.RATE_USER_FORUM
        else:
            if event_type == EventType.UPDATED:
                event_qualifier = f"evt_{EventType.UPDATE_GRADE_FORUM.value.abbr}"
                event_type = EventType.UPDATE_GRADE_FORUM
            else:
                event_qualifier = f"evt_{EventType.SET_GRADE_FORUM.value.abbr}"
                event_type = EventType.SET_GRADE_FORUM

        grade = self.fetch_grade_grades_by(
            grade_item["id"],
            event["timecreated"],
            event["relateduserid"],
            event["userid"],
        )
        if grade:
            final_grade = float(grade.get("finalgrade"))
            if final_grade is not None:
                attributes.append({"name": "grade", "value": final_grade})

        result = {
            "id": f'{event_qualifier}_{event["id"]}',
            "type": event_type.value.name,
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Rated by user" if is_rating else "Graded by user",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["relateduserid"],
                "Rated for user" if is_rating else "Graded for user",
            ),
            {
                "objectId": get_object_key(ObjectEnum.COURSE, event["courseid"]),
                "qualifier": "Related to course",
            },
        ]

        relationships.append(
            get_formatted_relationship(
                ObjectEnum.FORUM,
                grade_item["iteminstance"],
                "Pertains to forum",
            ),
        )

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    # endregion Extra event object construction

    # region Data fetching helpers
    def fetch_related_events(self, filter_conditions=None):
        if filter_conditions is None:
            filter_conditions = []

        if self.selected_courses:
            filter_conditions.append(self.Log.courseid.in_(self.selected_courses))

        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_discussion_by_id(self, discussion_id):
        filter_conditions = [self.Discussion.id == discussion_id]
        rows = self.db_service.query_object(self.Discussion, filter_conditions)
        return rows[0] if rows else None

    def fetch_upload_post_events(self):
        filter_conditions = [
            self.Log.action == "created",
            self.Log.target == "post",
            self.Log.objecttable == "forum_posts",
        ]

        if self.selected_courses:
            filter_conditions.append(self.Log.courseid.in_(self.selected_courses))

        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None

    def fetch_post_by_id(self, post_id):
        filter_conditions = [self.Post.id == post_id]
        rows = self.db_service.query_object(self.Post, filter_conditions)
        return rows[0] if rows else None

    def fetch_files_by_context_id(self, context_id):
        filter_conditions = [
            self.Files.contextid == context_id,
            self.Files.component == "mod_forum",
            not_((self.Files.filename.like(".")) | (self.Files.filename.like(""))),
        ]
        rows = self.db_service.query_object(self.Files, filter_conditions)
        return rows if rows else None

    def fetch_grade_item_by_id(self, item_id):
        GradeItem = self.db_service.Base.classes.mdl_grade_items

        filter_conditions = [GradeItem.id == item_id]
        rows = self.db_service.query_object(GradeItem, filter_conditions)
        return rows[0] if rows else None

    def fetch_grade_events(self):
        filter_conditions = [
            self.Log.action == "graded",
            self.Log.target == "user",
            self.Log.objecttable == "grade_grades",
            self.Log.userid > 0,
        ]

        if self.selected_courses:
            filter_conditions.append(self.Log.courseid.in_(self.selected_courses))

        rows = self.db_service.query_object(
            self.Log,
            filter_conditions,
            sort_by=[("timecreated", "asc"), ("objectid", "asc")],
        )
        return rows if rows else None

    def fetch_grade_grades_by(
        self, grade_item_id, time_created, related_user_id, user_id
    ):
        grade_grades_history = self.db_service.Base.classes.mdl_grade_grades_history
        filter_conditions = [
            grade_grades_history.itemid == grade_item_id,
            grade_grades_history.userid == related_user_id,
            grade_grades_history.timemodified >= (time_created - 5),
            grade_grades_history.timemodified < (time_created + 5),
            (
                grade_grades_history.loggeduser == user_id
                or grade_grades_history.usermodified == user_id
            ),
        ]
        rows = self.db_service.query_object(grade_grades_history, filter_conditions)
        return rows[0] if rows else None

    def fetch_related_forum_discussions(self, forum_id):
        filter_conditions = [self.Discussion.forum == forum_id]
        rows = self.db_service.query_object(self.Discussion, filter_conditions)
        return rows if rows else []

    def fetch_related_forum_posts(self, discussion_id):
        filter_conditions = [self.Post.discussion == discussion_id]
        rows = self.db_service.query_object(self.Post, filter_conditions)
        return rows if rows else []

    # endregion Data fetching helpers
