from flask import Flask, jsonify, request, send_from_directory, url_for
from flasgger import Swagger, swag_from
from flask_cors import CORS
import os
import glob
from logic.model.event_types import EventType
from logic.model.object_enum import ObjectEnum
from logic.utils.extractor_utils import get_module_events_map
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
def run_analysis():
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

    return jsonify(
        {
            "image_url": url_for(
                "serve_output_file", filename=result["image_file"], _external=True
            ),
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
