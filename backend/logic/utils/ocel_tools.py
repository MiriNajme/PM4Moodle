from logic.services.config_service import ConfigService
from logic.services.database_service import DatabaseService
from logic.services.file_service import FileService
from logic.entity_process.entity_process import EntityProcess
from logic.model.object_enum import ObjectEnum
from logic.model.event_types import EventType
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def get_database_config():
    config_initializer = ConfigService(os.path.dirname(__file__) + "/../config.cfg")
    config = config_initializer.get_config()
    return dict(config["database"])


def set_database_config(db_config: dict):
    config_path = os.path.dirname(__file__) + "/../config.cfg"
    config_initializer = ConfigService(config_path)
    config = config_initializer.get_config()
    config["database"] = db_config
    config_initializer.save_config(config)


def generate_ocel(module_events: dict = None):
    config_initializer = ConfigService(os.path.dirname(__file__) + "/../config.cfg")
    config = config_initializer.get_config()
    db_service = DatabaseService(config)
    file_service = FileService(config)
    entity = EntityProcess(db_service, file_service, config_initializer)

    if module_events is None:
        entity.process_all()
    else:
        entity.process_custom(module_events)

def write_ocel_to_file(data, file_name):
    config_initializer = ConfigService(os.path.dirname(__file__) + "/../config.cfg")
    config = config_initializer.get_config()
    file_service = FileService(config)
    file_service.write_json(data, file_name)

def read_ocel_file(file_name):
    config_initializer = ConfigService(os.path.dirname(__file__) + "/../config.cfg")
    config = config_initializer.get_config()
    file_service = FileService(config)
    return file_service.read_json(file_name)
