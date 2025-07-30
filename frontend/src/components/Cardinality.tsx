import React, { useState } from "react";
import { Text } from "@radix-ui/themes";
import clsx from "clsx";
import { useAppContext } from "../context/useAppContext";
import Spinner from "./ui/Spinner";
import type { Cardinality } from "../utils/pivot";

type RowColType = {
  row: number | null;
  col: number | null;
};

const groupEventTypesByPostfix = (eventTypes: string[]) => {
  const groups: Record<string, string[]> = {};
  eventTypes.forEach((eventType) => {
    const parts = eventType.split("_");
    const postfix = parts.length > 1 ? parts[parts.length - 1] : eventType;
    if (!groups[postfix]) groups[postfix] = [];
    groups[postfix].push(eventType);
  });
  return Object.values(groups).flat();
};

const formatCardinality = (cardinality: Cardinality) => {
  if (!cardinality || (!cardinality.min && !cardinality.max)) return "-";
  return `${cardinality.min}:${cardinality.max}`;
};

const OcelVerificationCardinality = React.memo(() => {
  const { pivot, isLoadingContent } = useAppContext();
  const [hovered, setHovered] = useState<RowColType>({
    row: null,
    col: null,
  });

  if (isLoadingContent) {
    return (
      <div className='flex justify-center items-center h-full pt-10'>
        <Spinner className='w-20 h-20 fill-blue-400' />
      </div>
    );
  }

  if (!pivot || !pivot.objectTypes?.length || !pivot.eventTypes?.length) {
    return (
      <Text className='text-center text-gray-500'>
        No data available to display.
      </Text>
    );
  }

  const filteredObjectTypes = pivot.objectTypes.filter((objType) =>
    pivot.eventTypes.some(
      (eventType) =>
        pivot.cardinality[eventType][objType].min > 0 ||
        pivot.cardinality[eventType][objType].max > 0
    )
  );

  let filteredEventTypes = pivot.eventTypes.filter((eventType) =>
    filteredObjectTypes.some(
      (objType) =>
        pivot.cardinality[eventType][objType].min > 0 ||
        pivot.cardinality[eventType][objType].max > 0
    )
  );

  filteredEventTypes = groupEventTypesByPostfix(filteredEventTypes);

  return (
    <div className='overflow-x-auto'>
      <Text>Verification Matrix (Cardinality)</Text>
      <div className='mt-4 max-h-[57dvh] overflow-auto border border-gray-200 rounded-lg'>
        <table className='w-full'>
          <thead>
            <tr>
              <th className='bg-white border-b border-r p-2 text-left sticky top-0 left-0 min-w-[140px]'>
                Event \ Object
              </th>
              {filteredObjectTypes.map((objType, colIdx) => (
                <th
                  key={objType}
                  className={clsx(
                    "bg-gray-100 border-b p-2 sticky top-0 z-20 text-center min-w-[100px]",
                    hovered.col === colIdx ? "!bg-blue-100" : ""
                  )}
                >
                  {objType}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredEventTypes.map((eventType, rowIdx) => (
              <tr
                key={eventType}
                className={clsx(
                  rowIdx % 2 === 1 ? "bg-gray-50" : "",
                  hovered.col !== null && hovered.row === rowIdx
                    ? "!bg-blue-50"
                    : ""
                )}
              >
                <td
                  className={clsx(
                    "bg-gray-100 border-b border-r p-2 font-semibold sticky left-0 z-20 border-gray-100 border-r-gray-500",
                    rowIdx % 2 === 1 ? "bg-gray-200" : "",
                    hovered.row === rowIdx ? "!bg-blue-100" : ""
                  )}
                >
                  {eventType}
                </td>
                {filteredObjectTypes.map((objType, colIdx) => (
                  <td
                    key={objType}
                    className={clsx(
                      "border-b border-gray-100 p-2 text-center cursor-pointer",
                      hovered.row === rowIdx || hovered.col === colIdx
                        ? "!bg-blue-100"
                        : "",
                      hovered.row === rowIdx && hovered.col === colIdx
                        ? "!bg-blue-300"
                        : ""
                    )}
                    onMouseEnter={() =>
                      setHovered({ row: rowIdx, col: colIdx })
                    }
                    onMouseLeave={() => setHovered({ row: null, col: null })}
                  >
                    {formatCardinality(pivot.cardinality[eventType][objType])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
});

export default OcelVerificationCardinality;
