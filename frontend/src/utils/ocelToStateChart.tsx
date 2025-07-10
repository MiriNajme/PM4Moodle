import type { ModuleType, OcelEventModel, OcelJsonContent } from "../services";

export function getModuleIcon(module: string) {
  switch (module) {
    case "assign":
      return "📝";
    case "choice":
      return "🔀";
    case "file":
      return "📃";
    case "folder":
      return "📂";
    case "label":
      return "🏷️";
    case "page":
      return "📄";
    case "url":
      return "🔗";
    case "forum":
      return "💬";
    case "quiz":
      return "✅";
    default:
      return "📦";
  }
}

export type Transition = { from: string; to: string; count: number };

export type OcelFullRelationChartState = {
  module: string;
  icon: string;
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

      const objTypeEvents: Record<string, OcelEventModel[]> = {};

      for (const event of ocel?.events ?? []) {
        if (!event.type || !relevantEventTypes.includes(event.type)) continue;

        const prefix = modulePrefixes[module];
        const objIds = (event.relationships ?? [])
          .filter((rel) => rel.objectId.startsWith(prefix))
          .map((rel) => rel.objectId);

        for (const objId of objIds) {
          if (!objTypeEvents[objId]) objTypeEvents[objId] = [];
          objTypeEvents[objId].push(event);
        }
      }

      const transitionsMap = new Map<string, number>();
      const statesSet = new Set<string>();
      for (const events of Object.values(objTypeEvents)) {
        const sorted = events.sort(
          (a, b) => new Date(a.time).getTime() - new Date(b.time).getTime()
        );
        const seq = sorted.map((event) => mapping[event.type] || event.type);

        seq.forEach((s) => statesSet.add(s));
        for (let i = 0; i < seq.length - 1; i++) {
          const key = `${seq[i]}->${seq[i + 1]}`;
          transitionsMap.set(key, (transitionsMap.get(key) ?? 0) + 1);
        }
      }

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
