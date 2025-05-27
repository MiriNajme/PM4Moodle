from entity_process.core.object_transformer_registry import ObjectTransformerRegistry
from entity_process.core.event_extractor_registry import EventExtractorRegistry
from model.object_enum import ObjectEnum


class EntityProcess:
    def __init__(self, db_service, file_service, config_service):
        self.db_service = db_service
        self.file_service = file_service
        self.config = config_service.get_config()
        self.related_object_columns = self.get_related_object_columns()
        self.related_event_columns = {}
        self.ocel_event_log = {
            "objectTypes": [],
            "event_types": [],
            "objects": [],
            "events": [],
        }

    def process_all(self):
        self.create_objects_type()

        registry = ObjectTransformerRegistry(
            self.db_service, self.related_object_columns, self.ocel_event_log
        )
        registry.transform_all()

        self.create_events_type()

        event_registry = EventExtractorRegistry(
            self.db_service,
            self.related_object_columns,
            self.related_event_columns,
            self.ocel_event_log,
        )
        event_registry.extract_all()

        self.write_output()

    def get_related_object_columns(self):
        result = {}
        for obj in ObjectEnum:
            table_name = obj.value.table_name
            if not table_name:
                continue

            table = self.db_service.metadata.tables.get(table_name)
            if table is not None:
                try:
                    result[obj.value.name] = self.db_service.get_column_names_and_types(
                        table
                    )
                except Exception as e:
                    print(f"[WARN] Failed to get columns for {table_name}: {e}")

        # remove password columns from the user object
        user_attributes = [
            d for d in result[ObjectEnum.USER.value.name] if d["name"] != "password"
        ]
        result[ObjectEnum.USER.value.name] = user_attributes

        # Add the 'completion_rule_attributes' object type with its columns
        result[ObjectEnum.COMPLETION_RULE.value.name] = [
            {"name": "id", "type": "string"},
            {"name": "is_manual", "type": "integer"},
            {"name": "must_be_viewed", "type": "integer"},
            {"name": "must_be_submitted", "type": "integer"},
            {"name": "must_be_graded", "type": "integer"},
            {"name": "must_be_passed", "type": "integer"},
        ]

        return result

    def create_objects_type(self):
        for obj_name, columns in self.related_object_columns.items():
            self.ocel_event_log["objectTypes"].append(
                {"name": obj_name, "attributes": columns}
            )

    def create_events_type(self):
        Log = self.db_service.Base.classes.mdl_logstore_standard_log
        log_attributes = self.db_service.get_column_names_and_types(Log.__table__)
        self.related_event_columns["log"] = log_attributes

        TaskAdhoc = self.db_service.Base.classes.mdl_task_adhoc
        task_adhoc_attributes = self.db_service.get_column_names_and_types(
            TaskAdhoc.__table__
        )
        self.related_event_columns["task_adhoc"] = task_adhoc_attributes

        CourseModuleCompletion = (
            self.db_service.Base.classes.mdl_course_modules_completion
        )
        course_module_completion_attributes = (
            self.db_service.get_column_names_and_types(CourseModuleCompletion.__table__)
        )
        self.related_event_columns["course_module_completion"] = (
            course_module_completion_attributes
        )

        event_types = [
            {"name": "create_assign", "attributes": log_attributes},
            {"name": "import_assign", "attributes": []},
            {"name": "update_assign", "attributes": log_attributes},
            {"name": "delete_assign", "attributes": task_adhoc_attributes},
            {
                "name": "complete_assign_manually",
                "attributes": course_module_completion_attributes,
            },
            {
                "name": "complete_assign_automatic",
                "attributes": course_module_completion_attributes,
            },
            {"name": "submit_group_assign", "attributes": log_attributes},
            {"name": "submit_individual_assign", "attributes": log_attributes},
            {"name": "draft_group_assign", "attributes": log_attributes},
            {"name": "draft_individual_assign", "attributes": log_attributes},
            {"name": "resubmit_group_assign", "attributes": log_attributes},
            {"name": "resubmit_individual_assign", "attributes": log_attributes},
            {"name": "redraft_group_assign", "attributes": log_attributes},
            {"name": "redraft_individual_assign", "attributes": log_attributes},
            {"name": "edit_assign_submission", "attributes": log_attributes},
            {"name": "remove_assign_submission", "attributes": log_attributes},
            {"name": "set_grade_assignment", "attributes": log_attributes},
            {"name": "update_grade_assignment", "attributes": log_attributes},
            {"name": "create_choice", "attributes": log_attributes},
            {"name": "import_choice", "attributes": []},
            {"name": "update_choice", "attributes": log_attributes},
            {"name": "delete_choice", "attributes": task_adhoc_attributes},
            {"name": "view_choice", "attributes": log_attributes},
            {
                "name": "complete_choice_manually",
                "attributes": course_module_completion_attributes,
            },
            {"name": "complete_choice_automatic", "attributes": log_attributes},
            {"name": "select_option", "attributes": log_attributes},
            {"name": "remove_selection", "attributes": log_attributes},
            {"name": "create_file", "attributes": log_attributes},
            {"name": "import_file", "attributes": []},
            {"name": "update_file", "attributes": log_attributes},
            {"name": "delete_file", "attributes": task_adhoc_attributes},
            {"name": "view_file", "attributes": log_attributes},
            {
                "name": "complete_file_manually",
                "attributes": course_module_completion_attributes,
            },
            {"name": "complete_file_automatic", "attributes": log_attributes},
            {"name": "create_folder", "attributes": log_attributes},
            {"name": "import_folder", "attributes": []},
            {"name": "update_folder", "attributes": log_attributes},
            {"name": "delete_folder", "attributes": task_adhoc_attributes},
            {"name": "view_folder", "attributes": log_attributes},
            {
                "name": "complete_folder_manually",
                "attributes": course_module_completion_attributes,
            },
            {"name": "complete_folder_automatic", "attributes": log_attributes},
            {"name": "download_folder", "attributes": log_attributes},
            {"name": "create_label", "attributes": log_attributes},
            {"name": "import_label", "attributes": []},
            {"name": "update_label", "attributes": log_attributes},
            {"name": "delete_label", "attributes": task_adhoc_attributes},
            {
                "name": "complete_label_manually",
                "attributes": course_module_completion_attributes,
            },
            {"name": "complete_label_automatic", "attributes": log_attributes},
            {"name": "create_page", "attributes": log_attributes},
            {"name": "import_page", "attributes": []},
            {"name": "update_page", "attributes": log_attributes},
            {"name": "delete_page", "attributes": task_adhoc_attributes},
            {"name": "view_page", "attributes": log_attributes},
            {
                "name": "complete_page_manually",
                "attributes": course_module_completion_attributes,
            },
            {"name": "complete_page_automatic", "attributes": log_attributes},
            {"name": "create_url", "attributes": log_attributes},
            {"name": "import_url", "attributes": []},
            {"name": "update_url", "attributes": log_attributes},
            {"name": "delete_url", "attributes": task_adhoc_attributes},
            {"name": "view_url", "attributes": log_attributes},
            {
                "name": "complete_url_manually",
                "attributes": course_module_completion_attributes,
            },
            {"name": "complete_url_automatic", "attributes": log_attributes},
        ]
        self.ocel_event_log["event_types"].extend(event_types)

    def write_output(self):
        self.file_service.write_ocel(
            event_type="all_objects", data=self.ocel_event_log, copy_to_last=True
        )
