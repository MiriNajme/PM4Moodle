import type { ModuleType, OCEL_Json_content } from "../services";

export function sequenceToStateChart(states: string[]) {
  if (!states || states.length === 0) {
    return {
      states: ["Start", "End"],
      transitions: [{ from: "Start", to: "End" }],
    };
  }

  return {
    states: ["Start", ...states, "End"],
    transitions: [
      { from: "Start", to: states[0] },
      ...states.slice(1).map((to, i) => ({
        from: states[i],
        to,
      })),
      { from: states[states.length - 1], to: "End" },
    ],
  };
}

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
      return "📦"; // Default package icon
  }
}

export type OcelChartState = {
  module: string;
  icon: string;
  chartData: {
    states: string[];
    transitions: { from: string; to: string }[];
  };
};

export function ocelToStateChart(
  ocel: OCEL_Json_content,
  modules: string[],
  moduleEventsMappings: ModuleType
): OcelChartState[] {
  return modules
    .filter((module) => moduleEventsMappings[module])
    .map((module) => {
      const mapping = moduleEventsMappings[module];
      const relevantEventTypes = Object.keys(mapping);

      // Filter json
      const filteredEvents = (
        ocel?.events?.filter(
          (event) => event.type && relevantEventTypes.includes(event.type)
        ) ?? []
      )
        .sort((a, b) => new Date(a.time).getTime() - new Date(b.time).getTime())
        .reduce((acc, event) => {
          const eventType = mapping[event.type] || event.type;
          if (!acc.includes(eventType)) {
            acc.push(eventType);
          }
          return acc;
        }, []) as string[];

      return {
        module,
        icon: getModuleIcon(module),
        chartData: sequenceToStateChart(filteredEvents),
      };
    });
}
