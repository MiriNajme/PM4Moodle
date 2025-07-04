from logic.entity_process.core.extractors.assign import Assign
from logic.entity_process.core.extractors.choice import Choice
from logic.entity_process.core.extractors.file import File
from logic.entity_process.core.extractors.folder import Folder
from logic.entity_process.core.extractors.forum import Forum
from logic.entity_process.core.extractors.label import Label
from logic.entity_process.core.extractors.page import Page
from logic.entity_process.core.extractors.quiz import Quiz
from logic.entity_process.core.extractors.url import Url


class EventExtractorRegistry:
    def __init__(
        self, db_service, related_object_columns, related_event_columns, ocel_event_log
    ):
        self.db_service = db_service
        self.related_object_columns = related_object_columns
        self.related_event_columns = related_event_columns
        self.ocel_event_log = ocel_event_log
        self.generators = [
            Assign(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            Choice(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            File(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            Folder(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            Label(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            Page(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            Url(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            Forum(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
            Quiz(
                self.db_service,
                self.related_object_columns,
                self.related_event_columns,
                self.ocel_event_log,
            ),
        ]

    def extract_all(self, module_events: dict = None):
        if module_events is None:
            for generator in self.generators:
                generator.extract()
        else:
            for generator in self.generators:
                if generator.object_type.value.name in module_events:
                    generator.extractBy(module_events[generator.object_type.value.name])
