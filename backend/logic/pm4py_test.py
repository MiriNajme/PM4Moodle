import argparse
import pm4py

from logic.utils.ocel_tools import generate_ocel, read_ocel_file
from logic.ocel_convert import (
    convert_objects,
    filter_events_by_id,
    filter_events_by_type,
)
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_dfg_analysis(module_events: dict) -> dict:
    path = os.path.join(os.path.dirname(__file__), "output")
    output_file = "ocel2__last.json"
    generate_ocel(module_events)
    full_path = os.path.join(path, output_file)
    try:
        log = pm4py.read.read_ocel2_json(full_path)
        dfg = pm4py.discover_ocdfg(log)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_file = output_file.replace(".json", f"_{timestamp}.png")
        image_path = os.path.join(path, image_file)
        pm4py.save_vis_ocdfg(dfg, image_path)
    except Exception as e:
        image_file = None

    return {
        "json_file": output_file,
        "image_file": image_file,
    }
