import React, { useState } from "react";
import { Text } from "@radix-ui/themes";
import clsx from "clsx";
import { useAppContext } from "../context/useAppContext";
import Spinner from "./ui/Spinner";

type RowColType = {
  row: number | null;
  col: number | null;
};

const groupEventTypesByPostfix = (eventTypes: string[]) => {
  // Group event types by postfix (after last underscore)
  const groups: Record<string, string[]> = {};
  eventTypes.forEach((eventType) => {
    const parts = eventType.split("_");
    const postfix = parts.length > 1 ? parts[parts.length - 1] : eventType;
    if (!groups[postfix]) groups[postfix] = [];
    groups[postfix].push(eventType);
  });
  // Flatten grouped event types, preserving group order
  return Object.values(groups).flat();
};

const OcelVerificationMatrix = React.memo(() => {
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

  // Filter objectTypes to only those with at least one non-falsy value in the matrix
  const filteredObjectTypes = pivot.objectTypes.filter((objType) =>
    pivot.eventTypes.some((eventType) => pivot.matrix[eventType][objType])
  );

  // Filter eventTypes to only those with at least one non-falsy value in the filtered columns
  let filteredEventTypes = pivot.eventTypes.filter((eventType) =>
    filteredObjectTypes.some((objType) => pivot.matrix[eventType][objType])
  );

  // Group filteredEventTypes by postfix
  filteredEventTypes = groupEventTypesByPostfix(filteredEventTypes);

  return (
    <div className='overflow-x-auto'>
      <Text className='mb-4'>
        Verification Matrix (Object counts per event)
      </Text>
      <div className='my-4 max-h-[60dvh] overflow-auto border border-gray-200 rounded-lg'>
        <table>
          <thead>
            <tr>
              <th className='bg-white border-b border-r p-2 text-left sticky top-0 left-0 min-w-[140px]'>
                Event \ Object
              </th>
              {filteredObjectTypes.map((objType, colIdx) => (
                <th
                  key={objType}
                  className={clsx(
                    "bg-gray-100 border-b p-2 sticky top-0 z-20 text-center min-w-[120px]",
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
                    "bg-gray-100 border-b border-r p-2 font-semibold sticky left-0 z-20 min-w-[140px] border-gray-100 border-r-gray-500",
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
                    {pivot.matrix[eventType][objType] || "-"}
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

export default OcelVerificationMatrix;
