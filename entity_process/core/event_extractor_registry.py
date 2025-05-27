from entity_process.core.events.assign_extractor import AssignExtractor
from entity_process.core.events.choice_extractor import ChoiceExtractor
from entity_process.core.events.file_extractor import FileExtractor
from entity_process.core.events.folder_extractor import FolderExtractor
from entity_process.core.events.label_extractor import LabelExtractor
from entity_process.core.events.page_extractor import PageExtractor
from entity_process.core.events.url_extractor import UrlExtractor


class EventExtractorRegistry:
    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        self.db_service = db_service
        self.related_object_columns = related_object_columns
        self.related_event_columns = related_event_columns
        self.ocel_event_log = ocel_event_log
        self.generators = [
            AssignExtractor(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            ChoiceExtractor(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            FileExtractor(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            FolderExtractor(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            LabelExtractor(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            PageExtractor(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            UrlExtractor(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
        ]

    def extract_all(self):
        for generator in self.generators:
            generator.extract()
