import pm4py
import sys
import os
import time
from datetime import datetime
from logic.utils.ocel_tools import generate_ocel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_dfg_analysis(courses: list , module_events: dict) -> dict:
    path = os.path.join(os.path.dirname(__file__), "output")
    output_file = "ocel2__last.json"

    # --- OCEL 2.0 extraction only (DB -> OCEL JSON) ---
    ocel_start = time.perf_counter()
    generate_ocel(courses, module_events)
    ocel_seconds = time.perf_counter() - ocel_start
    print(f"[TIMING] OCEL 2.0 extraction: {ocel_seconds:.3f}s", flush=True)

    full_path = os.path.join(path, output_file)
    dfg_seconds = None
    try:
        # --- DFG / OCDFG analysis + PNG (the other output) ---
        dfg_start = time.perf_counter()
        log = pm4py.read.read_ocel2_json(full_path)
        dfg = pm4py.discover_ocdfg(log)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_file = output_file.replace(".json", f"_{timestamp}.png")
        image_path = os.path.join(path, image_file)
        pm4py.save_vis_ocdfg(dfg, image_path)
        dfg_seconds = time.perf_counter() - dfg_start
        print(f"[TIMING] DFG analysis + PNG: {dfg_seconds:.3f}s", flush=True)
    except Exception as e:
        image_file = None

    return {
        "json_file": output_file,
        "image_file": image_file,
        "ocel_seconds": round(ocel_seconds, 3),
        "dfg_seconds": round(dfg_seconds, 3) if dfg_seconds is not None else None,
    }
