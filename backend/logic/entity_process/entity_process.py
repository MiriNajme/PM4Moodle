from logic.entity_process.core.object_transformer_registry import ObjectTransformerRegistry
from logic.entity_process.core.event_extractor_registry import EventExtractorRegistry
from logic.model.object_enum import ObjectEnum
from logic.utils.extractor_utils import get_module_event_objects_map

class EntityProcess:
    def __init__(self, db_service, file_service, config_service):
        self.db_service = db_service
        self.file_service = file_service
        self.config = config_service.get_config()
        self.related_object_columns = self.get_related_object_columns()
        self.related_event_columns = {}
        self.ocel_event_log = {
            "objectTypes": [],
            "eventTypes": [],
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

    def process_custom(self, module_events: dict = None):
        if module_events is None:
            process_all()
            return
            
        objects, events = self.get_selected_events_and_objects(module_events)
        
        self.create_objects_type(objects)

        registry = ObjectTransformerRegistry(
            self.db_service, self.related_object_columns, self.ocel_event_log
        )
        registry.transform_all(objects)

        self.create_events_type(events)
        event_registry = EventExtractorRegistry(
            self.db_service,
            self.related_object_columns,
            self.related_event_columns,
            self.ocel_event_log,
        )
        event_registry.extract_all(module_events)

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

        user_attributes = [
            d for d in result[ObjectEnum.USER.value.name] if d["name"] != "password"
        ]
        result[ObjectEnum.USER.value.name] = user_attributes

        return result

    def create_objects_type(self, objects: list = None):
        if objects is None or len(objects) == 0:
            for obj_name, columns in self.related_object_columns.items():
                self.ocel_event_log["objectTypes"].append(
                    {"name": obj_name, "attributes": columns}
                )
        else:
            for obj_name in objects:
                if obj_name in self.related_object_columns:
                    columns = self.related_object_columns[obj_name]
                    self.ocel_event_log["objectTypes"].append(
                        {"name": obj_name, "attributes": columns}
                    )
                    
    def create_events_type(self, events: list = None):
        Log = self.db_service.Base.classes.mdl_logstore_standard_log
        log_attributes = self.db_service.get_column_names_and_types(Log.__table__)
        self.related_event_columns["log"] = log_attributes

        TaskAdhoc = self.db_service.Base.classes.mdl_task_adhoc
        task_adhoc_attributes = self.db_service.get_column_names_and_types(
            TaskAdhoc.__table__
        )
        self.related_event_columns["task_adhoc"] = task_adhoc_attributes

        QuizAttempt = self.db_service.Base.classes.mdl_quiz_attempts
        quiz_attempt_attributes = self.db_service.get_column_names_and_types(
            QuizAttempt.__table__
        )
        self.related_event_columns["quiz_attempt"] = quiz_attempt_attributes

        QuizGrades = self.db_service.Base.classes.mdl_quiz_grades
        quiz_grades_attributes = self.db_service.get_column_names_and_types(
            QuizGrades.__table__
        )
        self.related_event_columns["quiz_grades"] = quiz_grades_attributes

        grade_attributes = log_attributes.copy() + [{"name": "grade", "type": "float"}]

        event_types = [
            {
                "name": "set_grade",
                "attributes": grade_attributes,
            },
            {
                "name": "update_grade",
                "attributes": grade_attributes,
            },
            
            # region ASSIGN
            {"name": "create_assign", "attributes": log_attributes},
            {"name": "import_assign", "attributes": []},
            {"name": "update_assign", "attributes": log_attributes},
            {"name": "delete_assign", "attributes": task_adhoc_attributes},
            {"name": "view_assign", "attributes": log_attributes},
            {"name": "submit_group_assign", "attributes": log_attributes},
            {"name": "submit_individual_assign", "attributes": log_attributes},
            {"name": "resubmit_group_assign", "attributes": log_attributes},
            {"name": "resubmit_individual_assign", "attributes": log_attributes},
            {"name": "remove_assign_submission", "attributes": log_attributes},
            # endregion ASSIGN
            
            # region CHOICE
            {"name": "create_choice", "attributes": log_attributes},
            {"name": "import_choice", "attributes": []},
            {"name": "update_choice", "attributes": log_attributes},
            {"name": "delete_choice", "attributes": task_adhoc_attributes},
            {"name": "view_choice", "attributes": log_attributes},
            {"name": "created_answer", "attributes": log_attributes},
            {"name": "deleted_answer", "attributes": log_attributes},
            # endregion CHOICE
            
            # region FILE
            {"name": "create_file", "attributes": log_attributes},
            {"name": "import_file", "attributes": []},
            {"name": "update_file", "attributes": log_attributes},
            {"name": "delete_file", "attributes": task_adhoc_attributes},
            {"name": "view_file", "attributes": log_attributes},
            # endregion FILE
            
            # region FOLDER
            {"name": "create_folder", "attributes": log_attributes},
            {"name": "import_folder", "attributes": []},
            {"name": "update_folder", "attributes": log_attributes},
            {"name": "delete_folder", "attributes": task_adhoc_attributes},
            {"name": "view_folder", "attributes": log_attributes},
            {"name": "download_folder", "attributes": log_attributes},
            # endregion FOLDER
            
            # region LABEL
            {"name": "create_label", "attributes": log_attributes},
            {"name": "import_label", "attributes": []},
            {"name": "update_label", "attributes": log_attributes},
            {"name": "delete_label", "attributes": task_adhoc_attributes},
            # endregion LABEL
            
            # region PAGE
            {"name": "create_page", "attributes": log_attributes},
            {"name": "import_page", "attributes": []},
            {"name": "update_page", "attributes": log_attributes},
            {"name": "delete_page", "attributes": task_adhoc_attributes},
            {"name": "view_page", "attributes": log_attributes},
            # endregion PAGE
            
            # region URL
            {"name": "create_url", "attributes": log_attributes},
            {"name": "import_url", "attributes": []},
            {"name": "update_url", "attributes": log_attributes},
            {"name": "delete_url", "attributes": task_adhoc_attributes},
            {"name": "view_url", "attributes": log_attributes},
            # endregion URL
            
            # region FORUM
            {"name": "create_forum", "attributes": log_attributes},
            {"name": "import_forum", "attributes": []},
            {"name": "update_forum", "attributes": log_attributes},
            {"name": "delete_forum", "attributes": task_adhoc_attributes},
            {"name": "view_forum", "attributes": log_attributes},
            {"name": "subscribe_to_forum", "attributes": log_attributes},
            {"name": "unsubscribe_from_forum", "attributes": log_attributes},
            {"name": "add_discussion", "attributes": log_attributes},
            {"name": "delete_discussion", "attributes": log_attributes},
            {"name": "lock_discussion", "attributes": log_attributes},
            {"name": "unlock_discussion", "attributes": log_attributes},
            {"name": "subscribe_to_discussion", "attributes": log_attributes},
            {"name": "unsubscribe_from_discussion", "attributes": log_attributes},
            {"name": "upload_post", "attributes": log_attributes},
            {"name": "delete_post", "attributes": log_attributes},
            {"name": "edit_post", "attributes": log_attributes},
            {"name": "rate_user_forum", "attributes": log_attributes},
            {"name": "update_rate_user_forum", "attributes": log_attributes},
            # endregion FORUM
            
            # region QUIZ
            {"name": "create_quiz", "attributes": log_attributes},
            {"name": "import_quiz", "attributes": []},
            {"name": "update_quiz", "attributes": log_attributes},
            {"name": "delete_quiz", "attributes": task_adhoc_attributes},
            {"name": "view_quiz", "attributes": log_attributes},
            {"name": "create_question", "attributes": log_attributes},
            {"name": "delete_question", "attributes": log_attributes},
            {"name": "add_question_slot", "attributes": log_attributes},
            {"name": "delete_question_slot", "attributes": log_attributes},
            {"name": "attempt_quiz", "attributes": quiz_attempt_attributes},
            {"name": "reattempt_quiz", "attributes": quiz_attempt_attributes},
            {"name": "set_grade_quiz", "attributes": quiz_grades_attributes},
            # endregion QUIZ
        ]

        if events is not None and len(events) > 0:
            event_types = [
                event for event in event_types if event["name"] in events
            ]
        
        self.ocel_event_log["eventTypes"].extend(event_types)
    
    def get_selected_events_and_objects(self, selected: dict = None):
        if selected is not None:
            modules_map = get_module_event_objects_map()
            objects = set([
                ObjectEnum.COURSE_MODULE.value.name,
                ObjectEnum.COURSE.value.name,
                ObjectEnum.CALENDAR.value.name,
                ObjectEnum.TAG_INSTANCE.value.name,
                ObjectEnum.TAG.value.name,
                ObjectEnum.SECTION.value.name,
                ObjectEnum.GROUP.value.name,
                ObjectEnum.USER.value.name,
            ])
            events = []

            for module, event_list in selected.items():
                if module in modules_map:
                    module_map = modules_map[module]
                    if module == ObjectEnum.QUESTION.value.name or \
                        module == ObjectEnum.QUIZ.value.name:
                        objects.update([
                            ObjectEnum.QUESTION.value.name,
                            ObjectEnum.QUIZ.value.name,
                            ObjectEnum.QUESTION_ANSWER.value.name,
                            ObjectEnum.QUESTION_HINT.value.name,
                            ObjectEnum.MULTI_CHOICE_QUESTION.value.name,
                            ObjectEnum.TRUE_FALSE_QUESTION.value.name,
                            ObjectEnum.SHORT_ANSWER_QUESTION.value.name,
                            ObjectEnum.NUMERICAL_QUESTION.value.name,
                            ObjectEnum.NUMERICAL_OPTION.value.name,
                            ObjectEnum.NUMERICAL_UNIT.value.name,
                            ObjectEnum.MATCH_QUESTION_SUB_QUESTION.value.name, 
                            ObjectEnum.MATCH_QUESTION_OPTION.value.name,
                            ObjectEnum.ESSAY_OPTION.value.name,
                            ObjectEnum.CALCULATED_QUESTION.value.name,
                            ObjectEnum.CALCULATED_OPTION.value.name,
                            ObjectEnum.NUMERICAL_OPTION.value.name,
                            ObjectEnum.NUMERICAL_UNIT.value.name,
                            ObjectEnum.QUESTION_DATASET.value.name,
                            ObjectEnum.DATASET_DEFINITION.value.name,
                        ])
                    elif module == ObjectEnum.ASSIGN.value.name:
                        objects.update([
                            ObjectEnum.GRADE_ITEM.value.name,
                        ])
                    
                    for event in event_list:
                        if event in module_map:
                            objects.update(module_map[event])
                            events.append(event)
            
            return sorted(objects), sorted(events)
        return [], []
    
    def write_output(self):
        self.file_service.write_ocel(
            event_type="all_objects", data=self.ocel_event_log, copy_to_last=True
        )
