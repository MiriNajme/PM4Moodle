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
    COMPLETED = EventValue("completed", "cpt", "complete", "Completes")
    
    # Folder events
    DOWNLOADED = EventValue("downloaded", "dld", "download", "Downloaded")
    
    # Assign events
    SET = EventValue("set", "set", "set", "Sets")

    # Choice events
    CREATED_ANSWER = EventValue("created_answer", "crt_answer", "select_option", "Related to")
    DELETED_ANSWER = EventValue(
        "deleted_answer", "del_answer", "remove_selection", "Related to"
    )

    def __str__(self):
        # This method will control how instances of EventType are converted to strings
        return self.value
