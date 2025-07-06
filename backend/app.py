from flask import Flask, jsonify, request, send_from_directory, url_for
from flasgger import Swagger, swag_from
from flask_cors import CORS
import os
import glob
from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.utils.extractor_utils import get_module_events_map
from logic.utils.ocel_tools import get_database_config, set_database_config
from logic.pm4py_test import run_dfg_analysis

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "logic", "output")


def clean_output_files(filename_base):
    extensions = ["json", "png"]
    for ext in extensions:
        pattern = os.path.join(OUTPUT_DIR, f"{filename_base}.{ext}")
        for f in glob.glob(pattern):
            os.remove(f)


@app.route("/api/event-types")
def get_event_types():
    """
    Get list of event types
    ---
    responses:
      200:
        description: A list of event types
        examples:
          application/json: ["viewed", "created", "deleted"]
    """
    types = [e.value.name for e in EventType]
    return jsonify(types)


@app.route("/api/objects")
def get_object_enums():
    """
    Get list of object enums
    ---
    responses:
      200:
        description: A list of object types
        examples:
          application/json: ["assign", "folder", "file"]
    """
    enums = [e.value.name for e in ObjectEnum]
    return jsonify(enums)


@app.route("/api/modules")
def get_modules():
    """
    Get list of modules
    ---
    responses:
      200:
        description: A list of modules with all eventtypes and object enums
        examples:
          application/json: {assign: ["created", "imported", "updated", "deleted", "viewed", "completed", "submit_group_assign", ...], folder: ["created", "imported", ...], ...}
    """
    modules = get_module_events_map()
    return jsonify(modules)


@app.route("/api/get-db-config")
def get_db_config():
    """
    Get DB configuration
    ---
    responses:
      200:
        description: Database configuration
        examples:
          application/json: {"host": "localhost", "port": 3306, "user, "root", "password": "", "db_name": "moodle"}
    """
    return jsonify(get_database_config())


@app.route("/api/set-db-config", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "host": {"type": "string", "example": "localhost"},
                        "port": {"type": "integer", "example": 3306},
                        "user": {"type": "string", "example": "root"},
                        "password": {"type": "string", "example": ""},
                        "db_name": {"type": "string", "example": "moodle"},
                    },
                    "required": ["host", "port", "user", "password", "db_name"],
                },
            }
        ],
        "responses": {200: {"description": "Success"}},
    }
)
def set_db_config():
    """
    Set database configuration for Moodle
    ---
    parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            host:
              type: string
              example: localhost
            port:
              type: integer
              example: 3306
            user:
              type: string
              example: root
            password:
              type: string
              example: ""
            db_name:
              type: string
              example: moodle
          required:
            - host
            - port
            - user
            - password
            - db_name
    responses:
      200:
        description: Success
    """
    data = request.json
    required_keys = {"host", "port", "user", "password", "db_name"}
    if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
        return jsonify({"error": "Invalid request body"}), 400

    set_database_config(data)
    return jsonify()


@app.route("/api/run-extraction", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            }
        ],
        "responses": {200: {"description": "Success"}},
    }
)
def run_extraction():
    """
    Run OCEL generation and DFG analysis
    ---
    parameters:
      - name: body
        in: body
        schema:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
    responses:
      200:
        description: OCEL and image URLs
    """
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request body"}), 400

    # Example: data = {"assign": ["created", "viewed"], "file": ["deleted"]}
    if not data:
        module_events = None
    else:
        module_events = data

    result = run_dfg_analysis(module_events)

    if result["image_file"] is not None:
        img_url = url_for(
            "serve_output_file", filename=result["image_file"], _external=True
        )
    else:
        img_url = ""

    return jsonify(
        {
            "image_url": img_url,
            "json_url": url_for(
                "serve_output_file", filename=result["json_file"], _external=True
            ),
        }
    )


@app.route("/output/<path:filename>")
def serve_output_file(filename):
    """
    Serve generated OCEL or DFG files
    ---
    parameters:
      - name: filename
        in: path
        type: string
        required: true
    responses:
      200:
        description: Static file
    """
    return send_from_directory(OUTPUT_DIR, filename)
