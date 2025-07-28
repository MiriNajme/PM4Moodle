import json
from logic.model.object_enum import ObjectEnum
from logic.utils.date_utils import format_date
from logic.utils.object_utils import (
    get_object_key,
    relation_formatter,
    check_key_existence,
)

from logic.entity_process.core.transformers.base import Base


class Course(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.COURSE
        self.object_class = self.db_service.Base.classes.mdl_course
        self.sort_by = [("timecreated", "asc")]
        self.has_relationships = True

        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log
        self.Group = self.db_service.Base.classes.mdl_groups
        self.Role = self.db_service.Base.classes.mdl_role

    def get_attributes(self, row, columns):
        attributes = []
        history_rows = self.get_course_update_history(row)

        for col in columns:
            attributes.append(
                {
                    "name": col["name"],
                    "value": row[col["name"]],
                    "time": format_date(row["timecreated"]),
                }
            )

        for hrow in history_rows:
            attributes.append(
                {
                    "name": hrow["name"],
                    "value": hrow["value"],
                    "time": format_date(hrow["time"]),
                }
            )

        attributes = sorted(attributes, key=lambda x: x["name"])
        return attributes

    def get_relationship(self, row):
        relationships = []

        # region GROUP
        groups = self.fetch_course_groups(row["id"])
        if groups:
            for group in groups:
                relationships.append(
                    {
                        "objectId": get_object_key(ObjectEnum.GROUP, group["id"]),
                        "qualifier": "Course contains group",
                        "from": group["from"],
                        "to": group["to"],
                    }
                )
        # endregion GROUP

        # region USER
        users = self.fetch_course_users(row["id"])
        if users:
            for user in users:
                role_names = ""
                roles = self.fetch_roles(user["id"], row["id"])

                if roles is None:
                    roles = self.fetch_roles_from_logs(user["id"], row["id"])

                if roles:
                    for role in roles:
                        role_names = role["shortname"] + ", " + role_names

                    role_names = role_names.rstrip(", ")

                relationships.append(
                    {
                        "objectId": get_object_key(ObjectEnum.USER, user["id"]),
                        "qualifier": "User enrolled as " + role_names,
                        "from": user["from"],
                        "to": user["to"],
                    }
                )
        # endregion USER

        return relationships

    def get_course_update_history(self, row):
        create_filter_conditions = [
            self.Log.target == "course",
            self.Log.action == "created",
            self.Log.objectid == row["id"],
        ]
        create_row = self.db_service.query_object(
            self.Log, create_filter_conditions, sort_by=[("timecreated", "asc")]
        )
        update_filter_conditions = [
            self.Log.target == "course",
            self.Log.action == "updated",
            self.Log.objectid == row["id"],
        ]
        update_rows = self.db_service.query_object(
            self.Log, update_filter_conditions, sort_by=[("timecreated", "asc")]
        )

        if (not update_rows) or (not create_row):
            return []

        create_row = json.loads(create_row[0]["other"])
        result = []
        for row in update_rows:
            new_other = json.loads(row["other"])
            new_other = new_other["updatedfields"]

            if new_other is None or not new_other:
                continue

            for key in new_other.keys():
                if not check_key_existence(key, self.related_object_columns["course"]):
                    continue

                if key in create_row:
                    row[key] = create_row[key]
                else:
                    row[key] = "Unknown"

                result.append(
                    {"name": key, "value": new_other[key], "time": row["timecreated"]}
                )

        return result

    def fetch_course_groups(self, course_id):
        all_groups = self.db_service.query_object(
            self.Group, [self.Group.courseid == course_id]
        )
        deleted_groups = self.fetch_from_log_event(
            course_id, target="group", action="deleted"
        )
        groups = relation_formatter(all_groups, deleted_groups, "id", "objectid")
        return groups if groups else None

    def fetch_course_users(self, course_id):
        enrolled_users = self.fetch_from_log_event(course_id, target="user_enrolment")
        unassigned_users = self.fetch_from_log_event(
            course_id, target="user_enrolment", action="deleted"
        )
        users = relation_formatter(enrolled_users, unassigned_users, "relateduserid")
        return users if users else None

    def fetch_roles(self, user_id, course_id):
        # noinspection SqlDialectInspection,LongLine
        sql_query = (
            "SELECT rr.shortname, ra.* from mdl_role_assignments ra inner join "
            "mdl_role rr on rr.id = ra.roleid "
            "WHERE userid= :user_id and contextid in "
            "(SELECT id from mdl_context WHERE contextlevel=50 and instanceid= :course_id )"
        )
        rows = self.db_service.query_text(
            sql_query, {"user_id": user_id, "course_id": course_id}
        )
        roles = []

        if rows:
            for row in rows:
                roles.append(
                    {
                        "shortname": row[0],
                        "id": row[1],
                        "roleid": row[2],
                        "contextid": row[3],
                        "userid": row[4],
                        "timemodified": row[5],
                        "modifierid": row[6],
                        "component": row[7],
                        "itemid": row[8],
                        "sortorder": row[9],
                    }
                )

        return roles if roles else None

    def fetch_roles_from_logs(self, user_id, course_id):
        filter_conditions = [
            self.Log.courseid == course_id,
            self.Log.relateduserid == user_id,
            self.Log.objecttable == "role",
            self.Log.action == "assigned",
        ]
        rows = self.db_service.query_object(self.Log, filter_conditions)

        if rows:
            role_ids = [row["objectid"] for row in rows]
            filter_conditions = [self.Role.id.in_(role_ids)]
            roles = self.db_service.query_object(self.Role, filter_conditions)

            return roles if roles else None

        return None

    # noinspection PyDefaultArgument
    def fetch_from_log_event(
        self, course_id, action="created", target=None, sort_by=[("timecreated", "asc")]
    ):
        filter_conditions = [
            self.Log.courseid == course_id,
            self.Log.action == action,
            self.Log.target == target,
        ]
        result = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=sort_by
        )
        return result

    # noinspection PyDefaultArgument
    def fetch_from_log_event2(
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
