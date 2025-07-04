from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.utils.extractor_utils import (
    build_attributes,
    get_formatted_event_id,
    get_formatted_relationship,
    get_module_event_type_name,
)
from logic.utils.date_utils import format_date
from logic.entity_process.core.extractors.base import Base


class Folder(Base):

    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        super().__init__(
            db_service,
            related_object_columns,
            related_event_columns,
            ocel_event_log,
        )
        self.object_type = ObjectEnum.FOLDER
        self.object_class = self.db_service.Base.classes.mdl_folder
        self.has_view_events = True

    def extract(self):
        super().extract()
        self.add_download_events()

    def extractBy(self, events: list = None):
        if not events:
            self.extract()
            return

        if "create_folder" in events or "import_folder" in events:
            self.add_create_import_events()

        if "delete_folder" in events:
            self.add_delete_events()

        if "update_folder" in events:
            self.add_update_events()

        if "view_folder" in events:
            self.add_view_events()

        if (
            "complete_folder_manually" in events
            or "complete_folder_automatic" in events
        ):
            self.add_complete_events()

        if "download_folder" in events:
            self.add_download_events()

    def add_download_events(self):
        events = self.fetch_downloaded_folder_events()
        if events:
            for event in events:
                self.ocel_event_log["events"].append(
                    self.get_downloaded_folder_event_object(event)
                )

    def get_downloaded_folder_event_object(self, event):
        attributes = build_attributes(event, self.related_event_columns["log"])
        result = {
            "id": get_formatted_event_id(
                EventType.DOWNLOADED, self.object_type, event["id"]
            ),
            "type": get_module_event_type_name(self.object_type, EventType.DOWNLOADED),
            "time": format_date(event["timecreated"]),
            "attributes": attributes,
        }

        # region RELATIONSHIPS
        relationships = [
            get_formatted_relationship(
                self.object_type,
                event["objectid"],
                f"{EventType.DOWNLOADED.value.qualifier} {self.object_type.value.name}",
            ),
            get_formatted_relationship(
                ObjectEnum.USER,
                event["userid"],
                "Downloaded by user",
            ),
        ]

        result["relationships"] = relationships
        # endregion RELATIONSHIPS

        return result

    def fetch_downloaded_folder_events(self):
        filter_conditions = [
            self.Log.action == "downloaded",
            self.Log.objecttable == self.object_type.value.module_name,
        ]
        events = self.db_service.query_object(
            self.Log, filter_conditions, sort_by=[("timecreated", "asc")]
        )
        return events if events else None
