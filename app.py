from services.config_service import ConfigService
from services.database_service import DatabaseService
from services.file_service import FileService
from entity_process.entity_process import EntityProcess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def generate_ocel():
    # Initialize configuration
    config_initializer = ConfigService(os.path.dirname(__file__) + "\\config.cfg")
    config = config_initializer.get_config()

    db_service = DatabaseService(config)
    file_service = FileService(config)

    entity = EntityProcess(db_service, file_service, config_initializer)
    entity.process_all()


def write_ocel_to_file(data, file_name):
    # Initialize configuration
    config_initializer = ConfigService(os.path.dirname(__file__) + "\\config.cfg")
    config = config_initializer.get_config()
    file_service = FileService(config)
    file_service.write_json(data, file_name)


def read_ocel_file(file_name):
    # Initialize configuration
    config_initializer = ConfigService(os.path.dirname(__file__) + "\\config.cfg")
    config = config_initializer.get_config()
    file_service = FileService(config)
    return file_service.read_json(file_name)


if __name__ == "__main__":
    generate_ocel()
