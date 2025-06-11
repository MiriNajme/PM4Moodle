import configparser
import json
import os
from datetime import datetime


class FileService:
    def __init__(self, config: configparser.ConfigParser):
        self.config = config['output']
        # path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) + self.config.get('file_path')
        path = os.path.join(os.path.dirname(__file__), '..') + self.config.get('file_path')
        self.file_path = path  # self.config.get('file_path')
        self.file_name_prefix = self.config.get('file_name_prefix')

    def write_ocel(self, event_type, data, copy_to_last):
        current_datetime = datetime.now().strftime('%m%d_%H%M')
        file_name = f"{self.file_name_prefix}_{str(event_type)}_{current_datetime}.json"
        self.write_json(data, file_name)

        # Optionally copy the data to 'ocel2__last.json'
        if copy_to_last:
            self.write_json(data, 'ocel2__last.json')

    def write_json(self, json_data, file_name):
        new_file_path = os.path.join(self.file_path, file_name)
        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)  # Ensure directory exists
        with open(new_file_path, 'w') as f:
            json.dump(json_data, f, indent=4)

        print(f"\t-- JSON data has been written to {new_file_path}")

    def read_json(self, file_name):
        new_file_path = os.path.join(self.file_path, file_name)
        with open(new_file_path) as f:
            return json.load(f)
