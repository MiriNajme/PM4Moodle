from model.event_types import EventType
from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key


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
    EventType.COMPLETED: "Completed in course",
}


def get_course_relationship_qualifier(event_type: EventType):
    return _event_type_to_qualifier.get(event_type, "Unknown event type in course")
