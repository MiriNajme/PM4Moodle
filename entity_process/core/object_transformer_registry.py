from entity_process.core.objects.completion_rule_transformer import (
    CompletionRuleTransformer,
)
from entity_process.core.objects.calendar_event_transformer import (
    CalendarEventTransformer,
)
from entity_process.core.objects.grade_history_transformer import (
    GradeHistoryTransformer,
)
from entity_process.core.objects.choice_option_transformer import (
    ChoiceOptionTransformer,
)
from entity_process.core.objects.course_transformer import CourseTransformer
from entity_process.core.objects.course_module_transformer import (
    CourseModuleTransformer,
)
from entity_process.core.objects.files_transformer import FilesTransformer
from entity_process.core.objects.grade_item_transformer import GradeItemTransformer
from entity_process.core.objects.group_transformer import GroupTransformer
from entity_process.core.objects.section_transformer import SectionTransformer
from entity_process.core.objects.tag_transformer import TagTransformer
from entity_process.core.objects.tag_instance_transformer import TagInstanceTransformer
from entity_process.core.objects.user_transformer import UserTransformer
from entity_process.core.objects.assign_transformer import AssignTransformer
from entity_process.core.objects.choice_transformer import ChoiceTransformer
from entity_process.core.objects.file_transformer import FileTransformer
from entity_process.core.objects.folder_transformer import FolderTransformer
from entity_process.core.objects.label_transformer import LabelTransformer
from entity_process.core.objects.page_transformer import PageTransformer
from entity_process.core.objects.url_transformer import UrlTransformer


class ObjectTransformerRegistry:
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        self.db_service = db_service
        self.related_object_columns = related_object_columns
        self.ocel_event_log = ocel_event_log

        self.objects = [
            CompletionRuleTransformer(
                db_service, related_object_columns, ocel_event_log
            ),
            GradeHistoryTransformer(db_service, related_object_columns, ocel_event_log),
            CalendarEventTransformer(
                db_service, related_object_columns, ocel_event_log
            ),
            ChoiceOptionTransformer(db_service, related_object_columns, ocel_event_log),
            CourseTransformer(db_service, related_object_columns, ocel_event_log),
            CourseModuleTransformer(db_service, related_object_columns, ocel_event_log),
            FilesTransformer(db_service, related_object_columns, ocel_event_log),
            GradeItemTransformer(db_service, related_object_columns, ocel_event_log),
            GroupTransformer(db_service, related_object_columns, ocel_event_log),
            SectionTransformer(db_service, related_object_columns, ocel_event_log),
            TagTransformer(db_service, related_object_columns, ocel_event_log),
            TagInstanceTransformer(db_service, related_object_columns, ocel_event_log),
            UserTransformer(db_service, related_object_columns, ocel_event_log),
            AssignTransformer(db_service, related_object_columns, ocel_event_log),
            ChoiceTransformer(db_service, related_object_columns, ocel_event_log),
            FileTransformer(db_service, related_object_columns, ocel_event_log),
            FolderTransformer(db_service, related_object_columns, ocel_event_log),
            LabelTransformer(db_service, related_object_columns, ocel_event_log),
            PageTransformer(db_service, related_object_columns, ocel_event_log),
            UrlTransformer(db_service, related_object_columns, ocel_event_log),
        ]

    def transform_all(self):
        for processor in self.objects:
            processor.transform()
