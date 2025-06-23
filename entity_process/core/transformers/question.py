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

        # Always related: Answers and Hints
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

        qtype = row["qtype"]
        qtype_qualifier = f"Is a {qtype}"
        # Type-based relationships
        if qtype == "multichoice":
            self.append_relationships(
                ObjectEnum.MULTI_CHOICE_QUESTION,
                self.fetch_multi_choices(row["id"]),
                qtype_qualifier,
                relationships,
            )
        elif qtype == "truefalse":
            self.append_relationships(
                ObjectEnum.TRUE_FALSE_QUESTION,
                self.fetch_true_falses(row["id"]),
                qtype_qualifier,
                relationships,
            )
        elif qtype == "shortanswer":
            self.append_relationships(
                ObjectEnum.SHORT_ANSWER_QUESTION,
                self.fetch_short_answer_questions(row["id"]),
                qtype_qualifier,
                relationships,
            )
        elif qtype == "numerical":
            self.append_relationships(
                ObjectEnum.NUMERICAL_QUESTION,
                self.fetch_numerical_questions(row["id"]),
                qtype_qualifier,
                relationships,
            )
            self.append_relationships(
                ObjectEnum.NUMERICAL_OPTION,
                self.fetch_numerical_options(row["id"]),
                "Has numerical options",
                relationships,
            )
            self.append_relationships(
                ObjectEnum.NUMERICAL_UNIT,
                self.fetch_numerical_units(row["id"]),
                "Has numerical units",
                relationships,
            )
        elif qtype == "match":
            self.append_relationships(
                ObjectEnum.MATCH_QUESTION_SUB_QUESTION,
                self.fetch_match_subquestions(row["id"]),
                "Has subquestions",
                relationships,
            )
            self.append_relationships(
                ObjectEnum.MATCH_QUESTION_OPTION,
                self.fetch_match_options(row["id"]),
                qtype_qualifier,
                relationships,
            )
        elif qtype == "essay":
            self.append_relationships(
                ObjectEnum.ESSAY_OPTION,
                self.fetch_essay_questions(row["id"]),
                qtype_qualifier,
                relationships,
            )
        elif qtype == "calculated":
            self.append_relationships(
                ObjectEnum.CALCULATED_QUESTION,
                self.fetch_calculated_questions(row["id"]),
                qtype_qualifier,
                relationships,
            )
            self.append_relationships(
                ObjectEnum.CALCULATED_OPTION,
                self.fetch_calculated_options(row["id"]),
                "Has calculated option",
                relationships,
            )
            self.append_relationships(
                ObjectEnum.NUMERICAL_OPTION,
                self.fetch_numerical_options(row["id"]),
                "Has numerical options",
                relationships,
            )
            self.append_relationships(
                ObjectEnum.NUMERICAL_UNIT,
                self.fetch_numerical_units(row["id"]),
                "Has numerical units",
                relationships,
            )
            self.append_relationships(
                ObjectEnum.QUESTION_DATASET,
                self.fetch_question_datasets(row["id"]),
                "Has datasets",
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

    def fetch_multi_choices(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_multichoice_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_true_falses(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_truefalse
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_match_subquestions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_match_subquestions
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_match_options(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_match_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_short_answer_questions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_shortanswer_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []
    
    def fetch_essay_questions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_qtype_essay_options
        filter_conditions = [TABLE.questionid == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_numerical_questions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_numerical
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_numerical_options(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_numerical_options
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_numerical_units(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_numerical_units
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []

    def fetch_calculated_questions(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_calculated
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []
    
    def fetch_calculated_options(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_calculated_options
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []
    
    def fetch_question_datasets(self, question_id):
        TABLE = self.db_service.Base.classes.mdl_question_datasets
        filter_conditions = [TABLE.question == question_id]
        rows = self.db_service.query_object(TABLE, filter_conditions)
        return rows or []
