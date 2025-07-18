from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.utils.object_utils import get_object_key


def get_formatted_event_id(eventType: EventType, objectEnum: ObjectEnum, id):
    return f"evt_{objectEnum.value.name}_{eventType.value.abbr}_{id}"


def get_module_event_type_name(objectEnum: ObjectEnum, eventType: EventType):
    return f"{eventType.value.type}_{objectEnum.value.name.lower()}"


def build_attributes(event, columns):
    return [{"name": col["name"], "value": event[col["name"]]} for col in columns]


def get_formatted_relationship(objectEnum: ObjectEnum, id, qualifier):
    return {
        "objectId": get_object_key(objectEnum, id),
        "qualifier": qualifier,
    }


_event_type_to_qualifier = {
    EventType.CREATED: "Created in course",
    EventType.UPDATED: "Updated in course",
    EventType.VIEWED: "Viewed in course",
    EventType.IMPORTED: "Imported in course",
    EventType.DELETED: "Deleted in course",
}


def get_course_relationship_qualifier(event_type: EventType):
    return _event_type_to_qualifier.get(event_type, "Unknown event type in course")


def get_module_events_map():
    modules = {
        ObjectEnum.ASSIGN.value.name: {
            "create_assign": "Created",
            "import_assign": "Imported",
            "update_assign": "Updated",
            "delete_assign ": "Deleted",
            "view_assign": "Viewed",
            "submit_group_assign": "Submitted",
            "submit_individual_assign": "Submitted",
            "resubmit_group_assign": "Resubmitted",
            "resubmit_individual_assign": "Resubmitted",
            "set_grade": "graded",
            "update_grade": "Updated",
        },
        ObjectEnum.CHOICE.value.name: {
            "create_choice": "Created",
            "import_choice": "Imported",
            "update_choice": "Updated",
            "delete_choice": "Deleted",
            "view_choice": "Viewed",
            "created_answer": "answered",
            "deleted_answer": "Answer deleted",
        },
        ObjectEnum.FILE.value.name: {
            "create_file": "Created",
            "import_file": "Imported",
            "update_file": "Updated",
            "delete_file": "Deleted",
            "view_file": "Viewed",
        },
        ObjectEnum.FOLDER.value.name: {
            "create_folder": "Created",
            "import_folder": "Imported",
            "update_folder": "Updated",
            "delete_folder": "Deleted",
            "view_folder": "Viewed",
            "download_folder": "Downloaded",
        },
        ObjectEnum.LABEL.value.name: {
            "create_label": "Created",
            "import_label": "Imported",
            "update_label": "Updated",
            "delete_label": "Deleted",
        },
        ObjectEnum.PAGE.value.name: {
            "create_page": "Created",
            "import_page": "Imported",
            "update_page": "Updated",
            "delete_page": "Deleted",
            "view_page": "Viewed",
        },
        ObjectEnum.URL.value.name: {
            "create_url": "Created",
            "import_url": "Imported",
            "update_url": "Updated",
            "delete_url": "Deleted",
            "view_url": "Viewed",
        },
        ObjectEnum.FORUM.value.name: {
            "create_forum": "Created",
            "import_forum": "Imported",
            "update_forum": "Updated",
            "delete_forum": "Deleted",
            "view_forum": "Viewed",
            "subscribe_to_forum": "Subscribed",
            "unsubscribe_from_forum": "Unsubscribed",
            "add_discussion": "Added",
            "delete_discussion": "Deleted",            "lock_discussion": "Locked",
            "unlock_discussion": "Unlocked",
            "subscribe_to_discussion": "Subscribed",
            "unsubscribe_from_discussion": "Unsubscribed",
            "upload_post": "Uploaded",
            "delete_post": "Deleted",
            "edit_post": "Edited",
            "set_grade": "Graded",
            "update_grade": "Grade Updated",
            "rate_user_forum": "Rated",
            "update_rate_user_forum": "Rating Updated",
        },
        ObjectEnum.QUIZ.value.name: {
            "create_quiz": "Created",
            "import_quiz": "Imported",
            "update_quiz": "Updated",
            "delete_quiz": "Deleted",
            "view_quiz": "Viewed",
            "create_question": "Create question",
            "delete_question": "Delete question",
            "add_question_slot": "Add question slot",
            "delete_question_slot": "Delete question slot",
            "attempt_quiz": "Attempted",
            "reattempt_quiz": "Reattempted",
            "set_grade_quiz": "Graded",
        },
    }

    return modules


def get_module_event_objects_map():
    modules = {
        ObjectEnum.ASSIGN.value.name: {
            "create_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.FILES.value.name,
            ],
            "import_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.FILES.value.name,
            ],
            "update_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.FILES.value.name,
            ],
            "delete_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
            ],
            "submit_group_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.FILES.value.name,
                ObjectEnum.GROUP.value.name,
            ],
            "submit_individual_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.FILES.value.name,
                ObjectEnum.GROUP.value.name,
            ],
            "resubmit_group_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.FILES.value.name,
                ObjectEnum.GROUP.value.name,
            ],
            "resubmit_individual_assign": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.FILES.value.name,
                ObjectEnum.GROUP.value.name,
            ],
            "set_grade": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.FILES.value.name,
            ],
            "update_grade": [
                ObjectEnum.ASSIGN.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.FILES.value.name,
            ],
        },
        ObjectEnum.CHOICE.value.name: {
            "create_choice": [
                ObjectEnum.CHOICE.value.name,
                ObjectEnum.OPTION.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_choice": [
                ObjectEnum.CHOICE.value.name,
                ObjectEnum.OPTION.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_choice": [
                ObjectEnum.CHOICE.value.name,
                ObjectEnum.OPTION.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_choice": [
                ObjectEnum.CHOICE.value.name,
                ObjectEnum.OPTION.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_choice": [
                ObjectEnum.CHOICE.value.name,
                ObjectEnum.OPTION.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
            ],           
            "created_answer": [
                ObjectEnum.CHOICE.value.name,
                ObjectEnum.OPTION.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.OPTION.value.name,
            ],
            "deleted_answer": [
                ObjectEnum.CHOICE.value.name,
                ObjectEnum.OPTION.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.OPTION.value.name,
            ],
        },
        ObjectEnum.FILE.value.name: {
            "create_file": [
                ObjectEnum.FILE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_file": [
                ObjectEnum.FILE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_file": [
                ObjectEnum.FILE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_file": [
                ObjectEnum.FILE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_file": [
                ObjectEnum.FILE.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
            ],
        },
        ObjectEnum.FOLDER.value.name: {
            "create_folder": [
                ObjectEnum.FOLDER.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_folder": [
                ObjectEnum.FOLDER.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_folder": [
                ObjectEnum.FOLDER.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_folder": [
                ObjectEnum.FOLDER.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_folder": [
                ObjectEnum.FOLDER.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
            ],
            "download_folder": [
                ObjectEnum.FOLDER.value.name,
                ObjectEnum.USER.value.name,
            ],
        },
        ObjectEnum.LABEL.value.name: {
            "create_label": [
                ObjectEnum.LABEL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_label": [
                ObjectEnum.LABEL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_label": [
                ObjectEnum.LABEL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_label": [
                ObjectEnum.LABEL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
        },
        ObjectEnum.PAGE.value.name: {
            "create_page": [
                ObjectEnum.PAGE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_page": [
                ObjectEnum.PAGE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_page": [
                ObjectEnum.PAGE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_page": [
                ObjectEnum.PAGE.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_page": [
                ObjectEnum.PAGE.value.name,
                ObjectEnum.USER.value.name,
            ],
        },
        ObjectEnum.URL.value.name: {
            "create_url": [
                ObjectEnum.URL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_url": [
                ObjectEnum.URL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_url": [
                ObjectEnum.URL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_url": [
                ObjectEnum.URL.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_url": [
                ObjectEnum.URL.value.name,
                ObjectEnum.USER.value.name,
            ],
        },
        ObjectEnum.FORUM.value.name: {
            "create_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
            ],
            "subscribe_to_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.USER.value.name,
            ],
            "unsubscribe_from_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.USER.value.name,
            ],
            "add_discussion": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_discussion": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "lock_discussion": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "unlock_discussion": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "subscribe_to_discussion": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "unsubscribe_from_discussion": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "upload_post": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.FORUM_POST.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
            ],
            "delete_post": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.FORUM_POST.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
            ],
            "edit_post": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.FORUM_DISCUSSION.value.name,
                ObjectEnum.FORUM_POST.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
            ],
            "set_grade": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_grade": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.USER.value.name,
            ],
            "rate_user_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_rate_user_forum": [
                ObjectEnum.FORUM.value.name,
                ObjectEnum.USER.value.name,
            ],
        },
        ObjectEnum.QUIZ.value.name: {
            "create_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "import_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "update_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.USER.value.name,
            ],
            "view_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.USER.value.name,
                ObjectEnum.COURSE.value.name,
            ],
            "create_question": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.QUESTION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_question": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.QUESTION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "add_question_slot": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.QUESTION.value.name,
                ObjectEnum.QUESTION_BANK_ENTRY.value.name,
                ObjectEnum.USER.value.name,
            ],
            "delete_question_slot": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.QUESTION.value.name,
                ObjectEnum.USER.value.name,
            ],
            "attempt_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.USER.value.name,
            ],
            "reattempt_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.USER.value.name,
            ],
            "set_grade_quiz": [
                ObjectEnum.QUIZ.value.name,
                ObjectEnum.USER.value.name,
            ],
        },
    }

    return modules
