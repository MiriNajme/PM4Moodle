from logic.entity_process.core.transformers.forum_discussion import (
    ForumDiscussion,
)
from logic.entity_process.core.transformers.forum_post import ForumPost
from logic.entity_process.core.transformers.forum import Forum
from logic.entity_process.core.transformers.choice_option import (
    ChoiceOption,
)
from logic.entity_process.core.transformers.course import Course
from logic.entity_process.core.transformers.group import Group
from logic.entity_process.core.transformers.user import User
from logic.entity_process.core.transformers.assign import Assign
from logic.entity_process.core.transformers.choice import Choice
from logic.entity_process.core.transformers.file import File
from logic.entity_process.core.transformers.folder import Folder
from logic.entity_process.core.transformers.label import Label
from logic.entity_process.core.transformers.page import Page
from logic.entity_process.core.transformers.question import Question
from logic.entity_process.core.transformers.question_answer import QuestionAnswer
from logic.entity_process.core.transformers.question_hint import QuestionHint
from logic.entity_process.core.transformers.question_bank_entry import QuestionBankEntry
from logic.entity_process.core.transformers.quiz import Quiz
from logic.entity_process.core.transformers.url import Url


class ObjectTransformerRegistry:
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        self.db_service = db_service
        self.related_object_columns = related_object_columns
        self.ocel_event_log = ocel_event_log

        self.transformer = [
            User(db_service, related_object_columns, ocel_event_log),
            File(db_service, related_object_columns, ocel_event_log),
            Page(db_service, related_object_columns, ocel_event_log),
            Folder(db_service, related_object_columns, ocel_event_log),
            Course(db_service, related_object_columns, ocel_event_log),
            Label(db_service, related_object_columns, ocel_event_log),
            Url(db_service, related_object_columns, ocel_event_log),
            Assign(db_service, related_object_columns, ocel_event_log),
            Group(db_service, related_object_columns, ocel_event_log),
            Choice(db_service, related_object_columns, ocel_event_log),
            Quiz(db_service, related_object_columns, ocel_event_log),
            Forum(db_service, related_object_columns, ocel_event_log),
            ChoiceOption(db_service, related_object_columns, ocel_event_log),
            ForumDiscussion(db_service, related_object_columns, ocel_event_log),
            ForumPost(db_service, related_object_columns, ocel_event_log),
            QuestionBankEntry(db_service, related_object_columns, ocel_event_log),
            Question(db_service, related_object_columns, ocel_event_log),
            QuestionHint(db_service, related_object_columns, ocel_event_log),
            QuestionAnswer(db_service, related_object_columns, ocel_event_log),
        ]

    def transform_all(self, objects: list = None):
        if objects is None or len(objects) == 0:
            for processor in self.transformer:
                processor.transform()
        else:
            for processor in self.transformer:
                if processor.object_type.value.name in objects:
                    processor.transform()
