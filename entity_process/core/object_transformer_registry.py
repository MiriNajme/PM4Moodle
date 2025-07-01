from entity_process.core.transformers.completion_rule import (
    CompletionRule,
)
from entity_process.core.transformers.calendar_event import (
    CalendarEvent,
)
from entity_process.core.transformers.forum_discussion import (
    ForumDiscussion,
)
from entity_process.core.transformers.forum_post import ForumPost
from entity_process.core.transformers.forum import Forum
from entity_process.core.transformers.choice_option import (
    ChoiceOption,
)
from entity_process.core.transformers.course import Course
from entity_process.core.transformers.course_module import (
    CourseModule,
)
from entity_process.core.transformers.files import Files
from entity_process.core.transformers.grade_item import GradeItem
from entity_process.core.transformers.group import Group
from entity_process.core.transformers.section import Section
from entity_process.core.transformers.tag import Tag
from entity_process.core.transformers.tag_instance import TagInstance
from entity_process.core.transformers.user import User
from entity_process.core.transformers.assign import Assign
from entity_process.core.transformers.choice import Choice
from entity_process.core.transformers.file import File
from entity_process.core.transformers.folder import Folder
from entity_process.core.transformers.label import Label
from entity_process.core.transformers.page import Page
from entity_process.core.transformers.question import Question
from entity_process.core.transformers.question_answer import QuestionAnswer
from entity_process.core.transformers.question_hint import QuestionHint
from entity_process.core.transformers.question_bank_entry import QuestionBankEntry
from entity_process.core.transformers.question_slot import QuestionSlot
from entity_process.core.transformers.multichoice_question import MultiChoiceQustion
from entity_process.core.transformers.trufalse_question import TrueFalseQustion
from entity_process.core.transformers.match_question_options import MatchQuestionOption
from entity_process.core.transformers.match_question_subquestion import (
    MatchQuestionSubQuestion,
)
from entity_process.core.transformers.short_asnwer_question import (
    ShortAnswerQuestion,
)
from entity_process.core.transformers.numerical_question import (
    NumericalQuestion,
)
from entity_process.core.transformers.numerical_option import (
    NumericalOption,
)
from entity_process.core.transformers.numerical_unit import (
    NumericalUnit,
)
from entity_process.core.transformers.essay_question import (
    EssayQuestion,
)
from entity_process.core.transformers.calculated_question import (
    CalculatedQuestion,
)
from entity_process.core.transformers.calculated_options import (
    CalculatedOptions,
)
from entity_process.core.transformers.question_dataset import (
    QuestionDataset,
)
from entity_process.core.transformers.dataset_definition import (
    DatasetDefinition,
)
from entity_process.core.transformers.quiz import Quiz
from entity_process.core.transformers.url import Url


class ObjectTransformerRegistry:
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        self.db_service = db_service
        self.related_object_columns = related_object_columns
        self.ocel_event_log = ocel_event_log

        self.transformer = [
            CompletionRule(db_service, related_object_columns, ocel_event_log),
            CalendarEvent(db_service, related_object_columns, ocel_event_log),
            ChoiceOption(db_service, related_object_columns, ocel_event_log),
            Course(db_service, related_object_columns, ocel_event_log),
            CourseModule(db_service, related_object_columns, ocel_event_log),
            Files(db_service, related_object_columns, ocel_event_log),
            GradeItem(db_service, related_object_columns, ocel_event_log),
            Group(db_service, related_object_columns, ocel_event_log),
            Section(db_service, related_object_columns, ocel_event_log),
            Tag(db_service, related_object_columns, ocel_event_log),
            TagInstance(db_service, related_object_columns, ocel_event_log),
            User(db_service, related_object_columns, ocel_event_log),
            Assign(db_service, related_object_columns, ocel_event_log),
            Choice(db_service, related_object_columns, ocel_event_log),
            File(db_service, related_object_columns, ocel_event_log),
            Folder(db_service, related_object_columns, ocel_event_log),
            Label(db_service, related_object_columns, ocel_event_log),
            Page(db_service, related_object_columns, ocel_event_log),
            Url(db_service, related_object_columns, ocel_event_log),
            Forum(db_service, related_object_columns, ocel_event_log),
            ForumDiscussion(db_service, related_object_columns, ocel_event_log),
            ForumPost(db_service, related_object_columns, ocel_event_log),
            Quiz(db_service, related_object_columns, ocel_event_log),
            Question(db_service, related_object_columns, ocel_event_log),
            QuestionAnswer(db_service, related_object_columns, ocel_event_log),
            QuestionHint(db_service, related_object_columns, ocel_event_log),
            QuestionBankEntry(db_service, related_object_columns, ocel_event_log),
            QuestionDataset(db_service, related_object_columns, ocel_event_log),
            DatasetDefinition(db_service, related_object_columns, ocel_event_log),
            # QuestionSlot(db_service, related_object_columns, ocel_event_log),
            MultiChoiceQustion(db_service, related_object_columns, ocel_event_log),
            TrueFalseQustion(db_service, related_object_columns, ocel_event_log),
            MatchQuestionSubQuestion(
                db_service, related_object_columns, ocel_event_log
            ),
            MatchQuestionOption(db_service, related_object_columns, ocel_event_log),
            ShortAnswerQuestion(db_service, related_object_columns, ocel_event_log),
            EssayQuestion(db_service, related_object_columns, ocel_event_log),
            NumericalQuestion(db_service, related_object_columns, ocel_event_log),
            NumericalOption(db_service, related_object_columns, ocel_event_log),
            NumericalUnit(db_service, related_object_columns, ocel_event_log),
            CalculatedQuestion(db_service, related_object_columns, ocel_event_log),
            CalculatedOptions(db_service, related_object_columns, ocel_event_log),
        ]

    def transform_all(self):
        for processor in self.transformer:
            processor.transform()
