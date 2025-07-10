import type { ModuleType, OcelEventModel, OcelJsonContent } from "../services";
import { Assign } from "../components/icons/Assign";
import { Choice } from "../components/icons/Choice";
import { File } from "../components/icons/File";
import { Folder } from "../components/icons/Folder";
import { Forum } from "../components/icons/Forum";
import { Label } from "../components/icons/Label";
import { Page } from "../components/icons/Page";
import { Quiz } from "../components/icons/Quiz";
import { Unknown } from "../components/icons/Unknown";
import { Url } from "../components/icons/Url";
import type React from "react";

export function getModuleIcon(module: string) {
  switch (module) {
    case "assign":
      return <Assign />;
    case "choice":
      return <Choice />;
    case "file":
      return <File />;
    case "folder":
      return <Folder />;
    case "label":
      return <Label />;
    case "page":
      return <Page />;
    case "url":
      return <Url />;
    case "forum":
      return <Forum />;
    case "quiz":
      return <Quiz />;
    default:
      return <Unknown />;
  }
}

export type Transition = { from: string; to: string; count: number };

export type OcelFullRelationChartState = {
  module: string;
  icon: React.ReactNode;
  chartData: {
    states: string[];
    transitions: Transition[];
  };
};

const modulePrefixes: Record<string, string> = {
  assign: "asn_",
  choice: "cho_",
  file: "fil_",
  folder: "fld_",
  label: "lbl_",
  page: "pag_",
  url: "url_",
  forum: "frm_",
  quiz: "quz_",
};

/**
 * Aggregates all event-to-event transitions per module (all relations, with cycles/loops)
 */
export function ocelToFullRelationStateChart(
  ocel: OcelJsonContent,
  modules: string[],
  moduleEventsMappings: ModuleType
): OcelFullRelationChartState[] {
  return modules
    .filter((module) => moduleEventsMappings[module])
    .map((module) => {
      const mapping = moduleEventsMappings[module];
      const relevantEventTypes = Object.keys(mapping);

      // Map: objectId -> sorted event type sequence for this module
      const objTypeEvents: Record<string, OcelEventModel[]> = {};

      // Group events by object (for this module)
      for (const event of ocel?.events ?? []) {
        if (!event.type || !relevantEventTypes.includes(event.type)) continue;

        // Get the module prefix for this module
        const prefix = modulePrefixes[module];
        const objIds = (event.relationships ?? [])
          .filter((rel) => rel.objectId.startsWith(prefix))
          .map((rel) => rel.objectId);

        for (const objId of objIds) {
          if (!objTypeEvents[objId]) objTypeEvents[objId] = [];
          objTypeEvents[objId].push(event);
        }
      }

      // Aggregate all transitions across all objects
      const transitionsMap = new Map<string, number>();
      const statesSet = new Set<string>();
      for (const events of Object.values(objTypeEvents)) {
        // Sort events for each object by time
        const sorted = events.sort(
          (a, b) => new Date(a.time).getTime() - new Date(b.time).getTime()
        );
        // Build sequence of event type display names
        const seq = sorted.map((event) => mapping[event.type] || event.type);

        // Register states
        seq.forEach((s) => statesSet.add(s));
        // For each transition
        for (let i = 0; i < seq.length - 1; i++) {
          const key = `${seq[i]}->${seq[i + 1]}`;
          transitionsMap.set(key, (transitionsMap.get(key) ?? 0) + 1);
        }
        // // Optionally connect Start/End
        // if (seq.length) {
        //   // Start -> first
        //   const startKey = `Start->${seq[0]}`;
        //   transitionsMap.set(startKey, (transitionsMap.get(startKey) ?? 0) + 1);
        //   // last -> End
        //   const endKey = `${seq[seq.length - 1]}->End`;
        //   transitionsMap.set(endKey, (transitionsMap.get(endKey) ?? 0) + 1);
        // }
      }

      // Build arrays for state chart
      // const states = ["Start", ...Array.from(statesSet), "End"];
      const states = [...Array.from(statesSet)];
      const transitions: Transition[] = Array.from(
        transitionsMap.entries()
      ).map(([key, count]) => {
        const [from, to] = key.split("->");
        return { from, to, count };
      });

      return {
        module,
        icon: getModuleIcon(module),
        chartData: {
          states,
          transitions,
        },
      };
    });
}
