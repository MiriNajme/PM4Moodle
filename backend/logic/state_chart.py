import json
import pandas as pd
from pm4py.objects.ocel.importer import importer as ocel_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
import networkx as nx
import matplotlib.pyplot as plt

with open("ocel-dfg (4).json") as f:
    ocel = json.load(f)

assign_events = {"create_assign", "update_assign", "submit_group_assign"}
url_events = {"create_url", "update_url", "delete_url", "view_url"}

events = ocel["events"]
filtered_events = []
for eid, event in events.items():
    if event["event_type"] in assign_events.union(url_events):
        filtered_events.append(
            {
                "event_id": eid,
                "event_type": event["event_type"],
                "timestamp": event["timestamp"],
                "omap": event["omap"],
            }
        )

filtered_events = sorted(filtered_events, key=lambda x: x["timestamp"])

object_sequences = {}
for ev in filtered_events:
    for oid in ev["omap"]:
        if oid not in object_sequences:
            object_sequences[oid] = []
        object_sequences[oid].append(ev)


def map_event_to_state(evtype):
    return {
        "create_assign": "created",
        "update_assign": "updated",
        "submit_group_assign": "submitted",
        "create_url": "created",
        "update_url": "updated",
        "view_url": "viewed",
        "delete_url": "deleted",
    }[evtype]


object_state_sequences = {}
for oid, evs in object_sequences.items():
    seq = []
    for ev in evs:
        state = map_event_to_state(ev["event_type"])
        if not seq or seq[-1] != state:
            seq.append(state)
    object_state_sequences[oid] = seq

transitions = {}
for seq in object_state_sequences.values():
    for a, b in zip(seq, seq[1:]):
        if (a, b) not in transitions:
            transitions[(a, b)] = 0
        transitions[(a, b)] += 1

G = nx.DiGraph()
for (a, b), cnt in transitions.items():
    G.add_edge(a, b, label=str(cnt))

pos = nx.spring_layout(G)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, font_size=14)
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("State Chart (Lifecycle) for Assign and URL Modules")
plt.show()
