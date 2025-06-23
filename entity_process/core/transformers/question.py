from model.object_enum import ObjectEnum
from entity_process.core.transformers.base import Base
from utils.date_utils import format_date
from utils.object_utils import convert_value_type, get_object_key


class Question(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.QUESTION
        self.object_class = self.db_service.Base.classes.mdl_question
        self.sort_by = [("timecreated", "asc")]
        self.has_relationships = True
        self.has_relation_to_calendar_events = False

    def get_attributes(self, row, columns):
        attributes = []

        for col in columns:
            attributes.append(
                {
                    "name": col["name"],
                    "value": convert_value_type(row[col["name"]]),
                    "time": format_date(row["timecreated"]),
                }
            )

        return attributes

    def get_relationship(self, row):
        relationships = super().get_relationship(row)

        answers = self.fetch_answers(row["id"])
        if answers:
            for answer in answers:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.QUESTION_ANSWER, answer["id"]
                        ),
                        "qualifier": "An answer of question",
                    }
                )

        hints = self.fetch_hints(row["id"])
        if hints:
            for hint in hints:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.QUESTION_HINT, hint["id"]
                        ),
                        "qualifier": "A hint of question",
                    }
                )

        if row["qtype"] == "multichoice":            
            rel_rows = self.fetch_multi_choices(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.MULTI_CHOICE_QUESTION, rel_row["id"]
                            ),
                            "qualifier": f"Is a {row["qtype"]}",
                        }
                    )
        elif row["qtype"] == "truefalse":
            rel_rows = self.fetch_true_falses(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.TRUE_FALSE_QUESTION, rel_row["id"]
                            ),
                            "qualifier": f"Is a {row["qtype"]}",
                        }
                    )
        elif row["qtype"] == "shortanswer":
            rel_rows = self.fetch_short_answer_questions(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.SHORT_ANSWER_QUSESTION, rel_row["id"]
                            ),
                            "qualifier": f"Is a {row["qtype"]}",
                        }
                    )
        elif row["qtype"] == "numerical":
            rel_rows = self.fetch_numerical_questions(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.NUMERICAL_QUESTION, rel_row["id"]
                            ),
                            "qualifier": f"Is a {row["qtype"]}",
                        }
                    )            
            rel_rows = self.fetch_numerical_options(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.NUMERICAL_OPTION, rel_row["id"]
                            ),
                            "qualifier": f"has numerical options",
                        }
                    )
            rel_rows = self.fetch_numerical_units(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.NUMERICAL_UNIT, rel_row["id"]
                            ),
                            "qualifier": f"has numerical units",
                        }
                    )
        elif row["qtype"] == "match":
            rel_rows = self.fetch_match_subquestions(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.MATCH_QUSESTION_SUB_QUSETION, rel_row["id"]
                            ),
                            "qualifier": f"Has subquestions",
                        }
                    )
            rel_rows = self.fetch_match_options(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.MATCH_QUSESTION_OPTION, rel_row["id"]
                            ),
                            "qualifier": f"Is a {row["qtype"]}",
                        }
                    )
        elif row["qtype"] == "essay":
            rel_rows = self.fetch_essay_questions(row["id"])
            if rel_rows:
                for rel_row in rel_rows:
                    relationships.append(
                        {
                            "objectId": get_object_key(
                                ObjectEnum.ESSAY_OPTION, rel_row["id"]
                            ),
                            "qualifier": f"Is a {row["qtype"]}",
                        }
                    )
        
        return relationships

    def fetch_answers(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_answers
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_hints(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_hints
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_multi_choices(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_multichoice_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_true_falses(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_truefalse
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_match_subquestions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_match_subquestions
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_match_options(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_match_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_short_answer_questions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_shortanswer_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None
    
    def fetch_essay_questions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_essay_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_numerical_questions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_numerical
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_numerical_options(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_numerical_options
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None

    def fetch_numerical_units(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_numerical_units
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows if rows else None
