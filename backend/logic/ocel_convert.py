import copy
# from app import write_ocel_to_file
from logic.utils.ocel_tools import write_ocel_to_file

def convert_objects(ocel_json):
    result = copy.deepcopy(ocel_json)
    object_types = result["objectTypes"]
    object_type_map = {object_type["name"]: object_type["attributes"] for object_type in object_types}
    for obj in result["objects"]:
        attributes = object_type_map[obj["type"]]
        object_types.append({
            "name": obj["id"],
            "attributes": attributes
        })
        obj["type"] = obj["id"]

    write_ocel_to_file(result, "ocel2__last_objects.json")
    return "ocel2__last_objects.json"


def filter_events_by_type(event_type, ocel_json):
    result = copy.deepcopy(ocel_json)
    events = result["events"]
    delete_indexs = []
    event_types = [event_type]
    index = -1

    if "," in event_type:
        event_types = event_type.split(",")
    
    for event in events:
        index += 1
        is_found = False
        
        for et in event_types:
            if et in event["type"]:
                is_found = True
                            
        if is_found == False:
            delete_indexs.append(index)

    delete_indexs.sort(reverse=True)

    for index in delete_indexs:
        del events[index]

    file_name = "ocel2__last_" + event_type + ".json"
    write_ocel_to_file(result, file_name)
    return file_name


def filter_events_by_id(object_id, ocel_json):
    result = copy.deepcopy(ocel_json)
    events = result["events"]
    delete_indexs = []
    index = -1

    for event in events:
        not_found = True
        index += 1

        for item in event["relationships"]:
            if item["objectId"] == object_id:
                not_found = not_found and False

        if not_found is True:
            delete_indexs.append(index)

    delete_indexs.sort(reverse=True)

    for index in delete_indexs:
        del events[index]

    file_name = "ocel2__last_" + object_id + ".json"
    write_ocel_to_file(result, file_name)
    return file_name
