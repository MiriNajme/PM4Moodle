from model.object_enum import ObjectEnum
from utils.object_utils import compare_history_logs
from entity_process.core.transformers.base import Base


class CalendarEvent(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.CALENDAR
        self.object_class = self.db_service.Base.classes.mdl_event

        self.Log = self.db_service.Base.classes.mdl_logstore_standard_log

    def get_attributes(self, row, columns):
        attributes = super().get_attributes(row, columns)

        for hrow in self.get_calendar_event_update_history(row["id"]):
            attributes.append(
                {"name": hrow["name"], "value": hrow["value"], "time": hrow["time"]}
            )

        attributes = sorted(attributes, key=lambda x: x["name"])
        return attributes

    def get_calendar_event_update_history(self, calendar_event_id):
        filter_conditions = [
            (
                self.Log.eventname.like("%calendar_event_created%")
                | self.Log.eventname.like("%calendar_event_updated%")
            ),
            self.Log.objectid == calendar_event_id,
        ]
        rows = self.db_service.query_object(
            self.Log,
            filter_conditions,
            sort_by=[("objectid", "asc"), ("timecreated", "asc")],
        )

        return compare_history_logs(rows)
