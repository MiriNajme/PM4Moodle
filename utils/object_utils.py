import json
from decimal import Decimal
from model.object_enum import ObjectEnum
from utils.date_utils import format_date


def relation_formatter(main_list, second_list, key, second_key=None):
    if second_key is None:
        second_key = key

    result = []
    if main_list:
        for item in main_list:
            to = "9999-12-31T23:59:59.999Z"
            if second_list:
                for second_item in second_list:
                    if (
                        second_item[second_key] == item[key]
                        and second_item["timecreated"] >= item["timecreated"]
                    ):
                        to = format_date(second_item["timecreated"], 1)

            result.append(
                {"id": item[key], "from": format_date(item["timecreated"]), "to": to}
            )
    return result


def compare_history_logs(rows):
    result = []
    current = None
    is_added = False
    for row in rows:
        if current is None or current["objectid"] != row["objectid"]:
            current = row
            continue

        old_other = json.loads(current["other"])
        new_other = json.loads(row["other"])
        found_diff = False
        for key in old_other.keys():
            if str(old_other[key]) != str(new_other[key]):
                found_diff = True
                if not is_added:
                    result.append(
                        {
                            "name": key,
                            "value": old_other[key],
                            "time": format_date(row["timecreated"]),
                        }
                    )
                    is_added = True

                result.append(
                    {
                        "name": key,
                        "value": new_other[key],
                        "time": format_date(row["timecreated"]),
                    }
                )

        if found_diff:
            current = row

    return result


def check_key_existence(key, array):
    for obj in array:
        if obj.get("name") == key:
            return True
    return False


def convert_value_type(value):
    if isinstance(value, Decimal):
        value = str(float(value))

    return value


def get_object_key(abbr: ObjectEnum, object_id):
    return abbr.value.abbr + "_" + str(object_id)


def create_event_key(value):
    if isinstance(value, Decimal):
        value = float(value)

    return value
