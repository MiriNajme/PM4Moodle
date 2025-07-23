from enum import Enum


class EventValue:
    def __init__(self, name, abbr, type, qualifier=None):
        self.name = name
        self.abbr = abbr
        self.type = type
        self.qualifier = qualifier


class EventType(Enum):
    CREATED = EventValue("created", "crt", "create", "Creates")
    DELETED = EventValue("deleted", "del", "delete", "Deletes")
    IMPORTED = EventValue("imported", "imp", "import", "Imports")
    UPDATED = EventValue("updated", "upd", "update", "Updates")
    VIEWED = EventValue("viewed", "vew", "view", "Views")

    # Folder events
    DOWNLOADED = EventValue("downloaded", "dld", "download", "Downloaded")

    # Assign events
    SET = EventValue("set", "set", "set", "Sets")

    # Choice events
    MAKE_A_CHOICE = EventValue(
        "make_a_choice", "mak_a_choice", "make_a_choice", "Related to"
    )
    REMOVE_A_CHOICE = EventValue(
        "remove_a_choice", "rmv_a_choice", "remove_a_choice", "Related to"
    )

    # region Forum events
    ADD_DISCUSSION = EventValue(
        "add_discussion", "add_disc", "add_discussion", "Adds discussion"
    )
    VIEW_DISCUSSION = EventValue("view_discussion", "vew_disc", "view_discussion", "Views discussion")
    DELETE_DISCUSSION = EventValue(
        "delete_discussion", "del_disc", "delete_discussion", "Deletes discussion"
    )
    LOCK_DISCUSSION = EventValue(
        "lock_discussion", "lock_disc", "lock_discussion", "Locks discussion"
    )
    UNLOCK_DISCUSSION = EventValue(
        "unlock_discussion", "unlock_disc", "unlock_discussion", "Unlocks discussion"
    )
    SUBSCRIBE_TO_FORUM = EventValue(
        "subscribe_to_forum", "sub_frm", "subscribe_to_forum", "Subscribes in"
    )
    UNSUBSCRIBE_FROM_FORUM = EventValue(
        "unsubscribe_from_forum",
        "unsub_frm",
        "unsubscribe_from_forum",
        "Unsubscribes from",
    )
    SUBSCRIBE_TO_DISCUSSION = EventValue(
        "subscribe_to_discussion",
        "sub_disc",
        "subscribe_to_discussion",
        "Subscribes in",
    )
    UNSUBSCRIBE_FROM_DISCUSSION = EventValue(
        "unsubscribe_from_discussion",
        "unsub_disc",
        "unsubscribe_from_discussion",
        "Unsubscribes from",
    )
    UPLOAD_POST = EventValue("upload_post", "upl_post", "upload_post", "Uploads post")
    EDIT_POST = EventValue("edit_post", "edt_post", "edit_post", "Edits post")
    DELETE_POST = EventValue("delete_post", "del_post", "delete_post", "Deletes post")
    SET_GRADE_FORUM = EventValue(
        "set_grade", "set_grade", "set_grade", "Sets grade for"
    )
    UPDATE_GRADE_FORUM = EventValue(
        "update_grade",
        "upd_grade",
        "update_grade",
        "Updates grade for",
    )
    RATE_USER_FORUM = EventValue(
        "rate_user_forum", "rat_usr_frm", "rate_user_forum", "Rates user in forum"
    )
    # endregion Forum events

    # region QUIZ
    CREATE_QUESTION = EventValue("create_question", "crt_ques", "create_question", "Creates")
    DELETE_QUESTION = EventValue("delete_question", "del_ques", "delete_question", "Deletes")
    ADD_QUESTION_SLOT = EventValue(
        "add_question_to_quiz", "add_ques_slt", "add_question_to_quiz", "Adds"
    )
    DELETE_QUESTION_SLOT = EventValue(
        "delete_question_from_quiz", "del_ques_slt", "delete_question_from_quiz", "Deletes"
    )
    QUIZ_ATTEMPT = EventValue("attempt_quiz", "quz_atmp", "attempt_quiz", "Attempts")
    QUIZ_REATTEMPT = EventValue(
        "reattempt_quiz", "quz_reatmp", "reattempt_quiz", "Reattempts"
    )
    QUIZ_SET_GRADE = EventValue("set_grade", "set_grade", "set_grade", "Sets grade for")
    # endregion QUIZ

    def __str__(self):
        return self.value
