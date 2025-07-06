import type { OCEL_Json_content } from "../services";

export interface OCEL_Pivot_Table {
  objectTypes: string[];
  eventTypes: string[];
  matrix: Record<string, Record<string, number>>;
}

export function buildPivotTable(ocelData: OCEL_Json_content): OCEL_Pivot_Table {
  const objectTypes = ocelData.objectTypes.map((o) => o.name).sort();
  const eventTypes = ocelData.eventTypes.map((e) => e.name).sort();

  // Build a lookup for object id -> object type
  const objectIdToType: Record<string, string> = {};
  ocelData.objects.forEach((obj: any) => {
    objectIdToType[obj.id] = obj.type;
  });

  // Initialize matrix: eventType x objectType
  const matrix: Record<string, Record<string, number>> = {};
  for (const eType of eventTypes) {
    matrix[eType] = {};
    for (const oType of objectTypes) {
      matrix[eType][oType] = 0;
    }
  }

  for (const event of ocelData.events) {
    const eType = event.type;
    if (!eType || !matrix[eType]) continue;

    if (event.relationships && event.relationships?.length > 0) {
      for (const relationship of event.relationships) {
        const objType = objectIdToType[relationship.objectId];
        if (objType) {
          if (matrix[eType][objType] !== undefined) {
            matrix[eType][objType]++;
          }
        }
      }
    }
  }

  return { objectTypes, eventTypes, matrix };
}
