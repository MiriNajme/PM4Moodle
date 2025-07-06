import React, { useState } from "react";
import { useAppContext } from "../context/useAppContext";
import clsx from "clsx";
import Spinner from "./ui/Spinner";
import { Table, Text } from "@radix-ui/themes";

const OcelPivotTable = React.memo(() => {
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
      <div className='my-4'>
        <Table.Root variant='surface' size='2'>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeaderCell className='border-b p-2 text-left sticky top-0 left-0 z-30 bg-white'>
                Event \ Object
              </Table.ColumnHeaderCell>
              {pivot.objectTypes.map((objType, colIdx) => (
                <Table.ColumnHeaderCell
                  key={objType}
                  className={clsx(
                    "border-b p-2 sticky top-0 z-20 bg-white text-center min-w-[120px]",
                    hovered.col === colIdx ? "!bg-blue-100" : ""
                  )}
                >
                  {objType}
                </Table.ColumnHeaderCell>
              ))}
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {pivot.eventTypes.map((eventType, rowIdx) => (
              <Table.Row
                key={eventType}
                className={clsx(
                  rowIdx % 2 === 1 ? "bg-gray-50" : "",
                  hovered.col !== null && hovered.row === rowIdx
                    ? "!bg-blue-50"
                    : ""
                )}
              >
                <Table.RowHeaderCell
                  className={clsx(
                    "border-b p-2 font-semibold sticky left-0 z-10 bg-white min-w-[140px]",
                    rowIdx % 2 === 1 ? "bg-gray-50" : "",
                    hovered.row === rowIdx ? "!bg-blue-100" : ""
                  )}
                >
                  {eventType}
                </Table.RowHeaderCell>
                {pivot.objectTypes.map((objType, colIdx) => (
                  <Table.Cell
                    key={objType}
                    className={clsx(
                      "border-b p-2 text-center cursor-pointer",
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
                  </Table.Cell>
                ))}
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      </div>
    </div>
  );
});

export default OcelPivotTable;
