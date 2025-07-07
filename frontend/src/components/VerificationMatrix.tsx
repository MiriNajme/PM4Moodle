import React, { useState } from "react";
import { useAppContext } from "../context/useAppContext";
import clsx from "clsx";
import Spinner from "./ui/Spinner";
import { Text } from "@radix-ui/themes";

const OcelVerificationMatrix = React.memo(() => {
  const { pivot, isLoadingContent } = useAppContext();
  const [hovered, setHovered] = useState<{
    row: number | null;
    col: number | null;
  }>({
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

  if (!pivot || !pivot.objectTypes || !pivot.eventTypes) {
    return (
      <Text className='text-center text-gray-500'>
        No data available to display.
      </Text>
    );
  }
  return (
    <div className='overflow-x-auto'>
      <Text as='div' weight='bold' className='mb-2'>
        Verification Matrix (Object counts per event)
      </Text>
      <div className='my-4 max-h-[600px] overflow-auto border border-gray-200 rounded-lg'>
        {" "}
        <table>
          <thead>
            <tr>
              <th className='bg-white border-b border-r p-2 text-left sticky top-0 left-0 min-w-[140px]'>
                Event \ Object
              </th>
              {pivot.objectTypes.map((objType, colIdx) => (
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
            {pivot.eventTypes.map((eventType, rowIdx) => (
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
                {pivot.objectTypes.map((objType, colIdx) => (
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
