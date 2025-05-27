from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key
from entity_process.core.objects.base_transformer import BaseTransformer


class CompletionRuleTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.COMPLETION_RULE

    def transform(self):
        rules = [
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 1),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 1),
                    },
                    {"name": "is_manual", "value": 1},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 2),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 2),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 3),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 3),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 4),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 4),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 5),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 5),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 6),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 6),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 7),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 7),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 8),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 8),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 9),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 9),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 10),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 10),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 11),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 11),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 1},
                    {"name": "must_be_graded", "value": 0},
                    {"name": "must_be_passed", "value": 1},
                    {"name": "make_a_choice", "value": 0},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 12),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 12),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 0},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 1},
                ],
            },
            {
                "id": get_object_key(ObjectEnum.COMPLETION_RULE, 13),
                "type": ObjectEnum.COMPLETION_RULE.value.name,
                "attributes": [
                    {
                        "name": "id",
                        "value": get_object_key(ObjectEnum.COMPLETION_RULE, 13),
                    },
                    {"name": "is_manual", "value": 0},
                    {"name": "must_be_viewed", "value": 1},
                    {"name": "must_be_submitted", "value": 0},
                    {"name": "must_be_graded", "value": None},
                    {"name": "must_be_passed", "value": 0},
                    {"name": "make_a_choice", "value": 1},
                ],
            },
        ]

        self.ocel_event_log["objects"].extend(rules)
