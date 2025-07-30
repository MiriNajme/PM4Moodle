import type { OcelJsonContent } from "../services";

export type Matrix<T> = Record<string, Record<string, T>>;

export interface Cardinality {
  min: number;
  max: number;
}

export interface OcelPivotTable {
  objectTypes: string[];
  eventTypes: string[];
  matrix: Matrix<number>;
  cardinality: Matrix<Cardinality>;
}

export function buildPivotTable(ocelData: OcelJsonContent): OcelPivotTable {
  const objectTypes = ocelData.objectTypes.map((o) => o.name);
  const eventTypes = ocelData.eventTypes.map((e) => e.name);

  const objectIdToType: Record<string, string> = {};
  ocelData.objects.forEach((obj: any) => {
    objectIdToType[obj.id] = obj.type;
  });

  const matrix: Matrix<number> = {};
  const cardinality: Matrix<Cardinality> = {};
  const defaultObjTypeCount: Matrix<number> = {};

  for (const eType of eventTypes) {
    matrix[eType] = {};
    cardinality[eType] = {};
    defaultObjTypeCount[eType] = {};

    for (const oType of objectTypes) {
      matrix[eType][oType] = 0;
      cardinality[eType][oType] = { min: Infinity, max: -Infinity };
      defaultObjTypeCount[eType][oType] = 0;
    }
  }

  for (const event of ocelData.events) {
    const eType = event.type;
    if (!eType || !matrix[eType]) continue;

    const objTypeCount: Record<string, number> = {
      ...defaultObjTypeCount[eType],
    };

    for (const relationship of event.relationships || []) {
      const objType = objectIdToType[relationship.objectId];
      if (!objType) continue;

      if (matrix[eType][objType] !== undefined) {
        matrix[eType][objType]++;
      }

      objTypeCount[objType] = (objTypeCount[objType] || 0) + 1;
    }

    for (const objType of Object.keys(objTypeCount)) {
      const count = objTypeCount[objType] || 0;
      const { min, max } = cardinality[eType][objType];

      cardinality[eType][objType].min = Math.min(min, count);
      cardinality[eType][objType].max = Math.max(max, count);
    }
  }

  for (const eType of eventTypes) {
    for (const oType of objectTypes) {
      if (cardinality[eType][oType].min === Infinity) {
        cardinality[eType][oType].min = 0;
      }
      if (cardinality[eType][oType].max === -Infinity) {
        cardinality[eType][oType].max = 0;
      }
    }
  }

  return { objectTypes, eventTypes, matrix, cardinality };
}
