import type { OCEL_Json_content } from "../services";

export function getStateChartData(
  ocel: OCEL_Json_content,
  eventMap: Record<string, string>
): { states: string[]; transitions: { from: string; to: string }[] } {
  // 1. Filter events by relevant types in eventMap
  const events = Object.values(ocel.events || {}).filter((e: any) =>
    Object.keys(eventMap).includes(e.event_type)
  );

  // 2. Map events to states, group by object, and remove repetition
  const stateMap: Record<string, string[]> = {};
  events.forEach((ev: any) => {
    (ev.omap || []).forEach((objId: string) => {
      if (!stateMap[objId]) stateMap[objId] = [];
      const state = eventMap[ev.event_type] || ev.event_type;
      if (stateMap[objId][stateMap[objId].length - 1] !== state) {
        stateMap[objId].push(state);
      }
    });
  });

  // 3. Collect unique states and transitions
  const states = Array.from(new Set(Object.values(stateMap).flat()));
  const transitions: { from: string; to: string }[] = [];
  Object.values(stateMap).forEach((seq) => {
    for (let i = 1; i < seq.length; ++i) {
      const edge = { from: seq[i - 1], to: seq[i] };
      if (!transitions.some((t) => t.from === edge.from && t.to === edge.to)) {
        transitions.push(edge);
      }
    }
  });
  return { states, transitions };
}
