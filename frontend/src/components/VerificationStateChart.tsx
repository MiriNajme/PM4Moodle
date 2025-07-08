import React, { useMemo } from "react";
import { Text } from "@radix-ui/themes";
import { useAppContext } from "../context/useAppContext";
import { StateChart } from "./StateChart";
import { ocelToStateChart } from "../utils/ocelToStateChart";

export const VerificationStateChart: React.FC = () => {
  const { jsonContent, selectedModules, modules } = useAppContext();

  const moduleCharts = useMemo(() => {
    if (!jsonContent || !selectedModules) return [];

    return ocelToStateChart(jsonContent, selectedModules, modules);
  }, [jsonContent, selectedModules, modules]);

  if (!jsonContent)
    return (
      <Text className='text-center text-gray-500'>
        No extracted log found. Run extraction first.
      </Text>
    );

  return (
    <div className='overflow-x-auto flex flex-col gap-4'>
      <Text className='mb-4'>Modules State Chart Diagrams</Text>
      <div className='flex flex-col gap-6 max-h-[60vh] overflow-y-auto'>
        {moduleCharts.map(({ module, icon, chartData }) => (
          <div
            key={module}
            className='rounded-2xl shadow-md p-4 flex flex-col gap-2 border border-gray-200'
          >
            <div className='flex items-center mb-2 gap-2'>
              <span className='text-2xl'>{icon}</span>
              <span className='text-lg font-bold capitalize'>
                {module} Module
              </span>
            </div>
            <div className='w-full h-48 flex items-center justify-center'>
              {chartData && chartData.states && chartData.states.length > 0 ? (
                <StateChart chartData={chartData} />
              ) : (
                <span className='text-gray-400'>
                  No state chart data available.
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
