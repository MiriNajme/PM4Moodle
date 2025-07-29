from logic.model.object_enum import ObjectEnum
from logic.entity_process.core.transformers.base import Base
from logic.utils.date_utils import format_date
from logic.utils.object_utils import convert_value_type, get_object_key


class Question(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.QUESTION
        self.object_class = self.db_service.Base.classes.mdl_question
        self.sort_by = [("timecreated", "asc")]
        self.has_relationships = True

    def get_attributes(self, row, columns):
        return [
            {
                "name": col["name"],
                "value": convert_value_type(row[col["name"]]),
                "time": format_date(row["timecreated"]),
            }
            for col in columns
        ]

    def append_relationships(self, enum_type, rows, qualifier, relationships):
        """
        Appends relationship dicts to relationships list for each row.
        """
        for rel_row in rows:
            relationships.append(
                {
                    "objectId": get_object_key(enum_type, rel_row["id"]),
                    "qualifier": qualifier,
                }
            )

    def get_relationship(self, row):
        relationships = super().get_relationship(row)

        self.append_relationships(
            ObjectEnum.QUESTION_ANSWER,
            self.fetch_answers(row["id"]),
            "An answer of question",
            relationships,
        )

        self.append_relationships(
            ObjectEnum.QUESTION_HINT,
            self.fetch_hints(row["id"]),
            "A hint of question",
            relationships,
        )

        return relationships

    def fetch_answers(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_answers
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_hints(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_hints
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []
