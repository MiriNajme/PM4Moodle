from enum import Enum


class ObjectValue:
    def __init__(self, name, abbr, table_name=None, module_name=None):
        self.name = name
        self.abbr = abbr
        self.table_name = table_name
        self.module_name = module_name


class ObjectEnum(Enum):
    USER = ObjectValue("user", "usr", "mdl_user")
    FILE = ObjectValue("file", "fil", "mdl_resource", "resource")
    PAGE = ObjectValue("page", "pag", "mdl_page", "page")
    FOLDER = ObjectValue("folder", "fld", "mdl_folder", "folder")
    COURSE = ObjectValue("course", "crs", "mdl_course")
    LABEL = ObjectValue("label", "lbl", "mdl_label", "label")
    URL = ObjectValue("url", "url", "mdl_url", "url")
    ASSIGN = ObjectValue("assign", "asn", "mdl_assign", "assign")
    GROUP = ObjectValue("group", "grp", "mdl_groups")
    CHOICE = ObjectValue("choice", "cho", "mdl_choice", "choice")
    QUIZ = ObjectValue("quiz", "quz", "mdl_quiz", "quiz")
    FORUM = ObjectValue("forum", "frm", "mdl_forum", "forum")
    OPTION = ObjectValue("option", "opt", "mdl_choice_options")
    FORUM_DISCUSSION = ObjectValue("discussion", "fdi", "mdl_forum_discussions")
    FORUM_POST = ObjectValue("post", "fpo", "mdl_forum_posts")
    QUESTION_BANK_ENTRY = ObjectValue(
        "question_bank_entry", "qbe", "mdl_question_bank_entries"
    )
    QUESTION = ObjectValue("question", "qst", "mdl_question")
    QUESTION_HINT = ObjectValue("question_hints", "qhi", "mdl_question_hints")
    QUESTION_ANSWER = ObjectValue("question_answers", "qan", "mdl_question_answers")
    COURSE_MODULE = ObjectValue("course_module", "cmd", "mdl_course_modules")
    FILES = ObjectValue("submission_file", "sfl", "mdl_files")
    FeedBack_FILE = ObjectValue("feedback_file", "ffl", "mdl_files")
    GRADE_ITEM = ObjectValue("grade_item", "gri", "mdl_grade_items", "grade_item")
    SECTION = ObjectValue("section", "sec", "mdl_course_sections")
    QUESTION_SLOT = ObjectValue("question_slots", "qsl", "mdl_quiz_slots")
    QUESTION_DATASET = ObjectValue("question_dataset", "qds", "mdl_question_datasets")
    DATASET_DEFINITION = ObjectValue(
        "dataset_definition", "qdsdef", "mdl_question_dataset_definitions"
    )
    TRUE_FALSE_QUESTION = ObjectValue(
        "truefalse_question", "qtf", "mdl_question_truefalse"
    )
    MULTI_CHOICE_QUESTION = ObjectValue(
        "multichoice_question", "qtmco", "mdl_qtype_multichoice_options"
    )
    MATCH_QUESTION_SUB_QUESTION = ObjectValue(
        "match_question_subquestion", "qtmsq", "mdl_qtype_match_subquestions"
    )
    MATCH_QUESTION_OPTION = ObjectValue(
        "match_question_option", "qtmo", "mdl_qtype_match_options"
    )
    SHORT_ANSWER_QUESTION = ObjectValue(
        "short_answer_question", "qtsaq", "mdl_qtype_shortanswer_options"
    )
    NUMERICAL_QUESTION = ObjectValue(
        "numerical_question", "qtnuq", "mdl_question_numerical"
    )
    NUMERICAL_OPTION = ObjectValue(
        "numerical_option", "nuopt", "mdl_question_numerical_options"
    )
    NUMERICAL_UNIT = ObjectValue(
        "numerical_unit", "nuopt", "mdl_question_numerical_units"
    )
    ESSAY_OPTION = ObjectValue("essay_option", "qtesq", "mdl_qtype_essay_options")
    CALCULATED_QUESTION = ObjectValue(
        "calculated_question", "calq", "mdl_question_calculated"
    )
    CALCULATED_OPTION = ObjectValue(
        "calculated_option", "calopt", "mdl_question_calculated_options"
    )

    @classmethod
    def all_values(cls):
        return [item.value for item in cls]

    def __str__(self):
        return self.value
