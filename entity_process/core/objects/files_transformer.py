from model.object_enum import ObjectEnum
from utils.object_utils import get_object_key
from entity_process.core.objects.base_transformer import BaseTransformer


class FilesTransformer(BaseTransformer):
    def __init__(self, db_service, related_object_columns, ocel_event_log):
        super().__init__(db_service, related_object_columns, ocel_event_log)
        self.object_type = ObjectEnum.FILES
        self.object_class = self.db_service.Base.classes.mdl_files
        self.sort_by = [("timemodified", "asc")]

    def process_records(self, records):
        list_of_objects = []

        columns = self.get_columns()
        if not columns:
            return

        for row in records:
            attributes = self.get_attributes(row, columns)

            obj_type = ObjectEnum.FILES.value.name

            if row["filearea"] == "feedback_files":
                obj_type = "feedback_file"
            elif row["filearea"] == "submission_files":
                obj_type = "submission_file"

            row_obj = {
                "id": get_object_key(self.object_type, row["id"]),
                "type": obj_type,
                "attributes": attributes,
            }

            list_of_objects.append(row_obj)

        self.ocel_event_log["objects"].extend(list_of_objects)
