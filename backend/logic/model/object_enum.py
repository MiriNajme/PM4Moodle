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
    QUESTION_HINT = ObjectValue("hint", "qhi", "mdl_question_hints")
    QUESTION_ANSWER = ObjectValue("answer", "qan", "mdl_question_answers")
    
    @classmethod
    def all_values(cls):
        return [item.value for item in cls]

    def __str__(self):
        return self.value
