import argparse
import pm4py

# from pm4py.visualization.ocdfg import visualizer as ocdfg_visualizer

# from app import generate_ocel, read_ocel_file
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


def generate_dfg():
    try:
        # path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\output\\"
        path = os.path.dirname(__file__) + "\\output\\"

        # Create the parser
        parser = argparse.ArgumentParser(
            description="Add json file name. ex, ocel2_last"
        )
        # Add arguments
        parser.add_argument(
            "--genocel", type=str, default="y", help="generate OCEL2 json file. ex, y/n"
        )
        parser.add_argument(
            "--filename",
            type=str,
            default="ocel2__last",
            help="OCEL2 json file name. ex, ocel2_last",
        )
        parser.add_argument("--objectid", type=str, help="OCEL2 object id. ex, url11")
        parser.add_argument(
            "--convert",
            type=str,
            default="n",
            help="convert OCEL2 objects to object types. ex, y/n",
        )
        parser.add_argument(
            "--eventtype",
            type=str,
            default=None,
            help="filter OCEL2 by event type. ex, url",
        )

        # Parse arguments
        args = parser.parse_args()

        print("1) Generating OCEL2\n")
        if args.genocel == "y" or args.genocel == "Y":
            generate_ocel()
        else:
            print("\t-- Skipped\n")

        print("2) Generating DFG\n")

        # Load the OCEL log
        file_path = args.filename + ".json"
        if args.convert == "y" or args.convert == "Y":
            json_data = read_ocel_file(file_path)
            file_path = convert_objects(json_data)
            print(
                "\t-- object converted to object types successfully. you can check ",
                file_path,
            )

        if args.eventtype:
            json_data = read_ocel_file(file_path)
            file_path = filter_events_by_type(args.eventtype, json_data)
            print("\t-- filtered by event type successfully. you can check ", file_path)

        if args.objectid:
            json_data = read_ocel_file(file_path)
            file_path = filter_events_by_id(args.objectid, json_data)
            print(
                "\t-- filtered by events by object id successfully. you can check ",
                file_path,
            )

        file_path = path + file_path
        log = pm4py.read.read_ocel2_json(file_path)
        print("\t-- JSON file successfully imported and validated.\n")

        dfg = pm4py.discover_ocdfg(log)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_file = os.path.basename(file_path).replace(".json", f"_{timestamp}.png")
        image_path = os.path.join(path, image_file)

        pm4py.save_vis_ocdfg(dfg, image_path)
        print(f"\t-- DFG file successfully generated and saved as {image_file}.\n")

    except Exception as e:
        print(f"An error occurred: {e}")


# API
# This function is used to run the DFG analysis with optional parameters.
# It generates the OCEL, reads the JSON file, converts objects, filters events by type
# and ID, and finally discovers the DFG.
# It returns a dictionary with the JSON file name and the image file name.
def run_dfg_analysis(module_events: dict) -> dict:
    path = os.path.join(os.path.dirname(__file__), "output")
    output_file = "ocel2__last.json"
    generate_ocel(module_events)
    full_path = os.path.join(path, output_file)
    try:
        log = pm4py.read.read_ocel2_json(full_path)
        dfg = pm4py.discover_ocdfg(log)
        # Explicitly save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_file = output_file.replace(".json", f"_{timestamp}.png")
        image_path = os.path.join(path, image_file)
        pm4py.save_vis_ocdfg(dfg, image_path)
        # pm4py.view_ocdfg(dfg, format="png")  # Saves a .png file
    except Exception as e:
        # raise RuntimeError(f"PM4Py analysis failed: {e}")
        image_file = None

    return {
        "json_file": output_file,
        "image_file": image_file,  # .replace(".json", ".png")
    }


# if __name__ == "__main__":
#     print("\n")
#     generate_dfg()
#     print("*** DONE ***\n\n")

# py pm4py_test.py
# --filename ocel2__last
# --objectid url11
# --eventtype url
# --genocel y (generate ocel)
# --convert y


# py src\v1\pm4py_test.py  --genocel n --eventtype folder
# py src\v1\pm4py_test.py  --genocel n --objectid asn_2
# py src\v1\pm4py_test.py  --genocel n --convert y
