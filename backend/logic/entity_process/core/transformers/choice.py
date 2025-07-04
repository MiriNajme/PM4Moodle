from logic.model.object_enum import ObjectEnum
from logic.utils.date_utils import format_date
from logic.utils.object_utils import get_object_key
from logic.entity_process.core.transformers.base import Base


class Choice(Base):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.CHOICE
        self.object_class = self.db_service.Base.classes.mdl_choice
        self.sort_by = [("timemodified", "asc")]
        self.has_relationships = True

        self.ChoiceOption = self.db_service.Base.classes.mdl_choice_options

    def get_relationship(self, row):
        relationships = super().get_relationship(row)

        choice_options = self.fetch_choice_options_by_choice_id(row["id"])
        if choice_options:
            for choice_option in choice_options:
                relationships.append(
                    {
                        "objectId": get_object_key(
                            ObjectEnum.OPTION, choice_option["id"]
                        ),
                        "qualifier": "Has option",
                        "from": format_date(choice_option["timemodified"]),
                        "to": "9999-12-31T23:59:59.999Z",
                    }
                )

        return relationships

    def fetch_choice_options_by_choice_id(self, choice_id):
        filter = [self.ChoiceOption.choiceid == choice_id]
        choice_options = self.db_service.query_object(
            self.ChoiceOption, filter, sort_by=[("text", "asc")]
        )
        return choice_options if choice_options else None
