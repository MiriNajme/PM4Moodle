from enum import Enum


class ObjectValue:
    def __init__(self, name, abbr, table_name=None, module_name=None, module_id=None):
        self.name = name
        self.abbr = abbr
        self.table_name = table_name
        self.module_id = module_id
        self.module_name = module_name


class ObjectEnum(Enum):
    ASSIGN = ObjectValue("assign", "asn", "mdl_assign", "assign", 1)
    CALENDAR = ObjectValue("calendar_event", "cal", "mdl_event")
    CHOICE = ObjectValue("choice", "cho", "mdl_choice", "choice", 5)
    OPTION = ObjectValue("option", "opt", "mdl_choice_options")
    COURSE = ObjectValue("course", "crs", "mdl_course")
    COURSE_MODULE = ObjectValue("course_module", "cmd", "mdl_course_modules")
    COMPLETION_RULE = ObjectValue("completion_rule", "cpr")
    FILE = ObjectValue("file", "fil", "mdl_resource", "resource", 18)
    FILES = ObjectValue("submission_file", "sfl", "mdl_files")
    FeedBack_FILE = ObjectValue("feedback_file", "ffl", "mdl_files")
    FOLDER = ObjectValue("folder", "fld", "mdl_folder", "folder", 8)
    GRADE_ITEM = ObjectValue("grade_item", "gri", "mdl_grade_items", "grade_item")
    GRADES_HISTORY = ObjectValue("grade", "grd", "mdl_grade_grades_history")
    GROUP = ObjectValue("group", "grp", "mdl_groups")
    LABEL = ObjectValue("label", "lbl", "mdl_label", "label", 13)
    PAGE = ObjectValue("page", "pag", "mdl_page", "page", 16)
    SECTION = ObjectValue("section", "sec", "mdl_course_sections")
    TAG = ObjectValue("tag", "tag", "mdl_tag")
    TAG_INSTANCE = ObjectValue("tag_instance", "tgi", "mdl_tag_instance")
    URL = ObjectValue("url", "url", "mdl_url", "url", 21)
    USER = ObjectValue("user", "usr", "mdl_user")

    @classmethod
    def all_values(cls):
        return [item.value for item in cls]

    def __str__(self):
        # This method will control how instances of EventType are converted to strings
        return self.value

