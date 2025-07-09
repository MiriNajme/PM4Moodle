import React, { useMemo } from "react";
import { Tabs, Text } from "@radix-ui/themes";
import { useAppContext } from "../context/useAppContext";
import { StateChart } from "./StateChart";
import { ocelToFullRelationStateChart } from "../utils/ocelToStateChart";

export const VerificationStateChart: React.FC = () => {
  const { jsonContent, selectedModules, modules } = useAppContext();

  const moduleCharts = useMemo(() => {
    if (!jsonContent || !selectedModules) return [];

    return ocelToFullRelationStateChart(jsonContent, selectedModules, modules);
  }, [jsonContent, selectedModules, modules]);

  if (!jsonContent)
    return (
      <Text className='text-center text-gray-500'>
        No extracted log found. Run extraction first.
      </Text>
    );

  return (
    <div className='w-full'>
      <Tabs.Root>
        <Tabs.List className='mb-4'>
          {moduleCharts.map(({ module, icon }) => (
            <Tabs.Trigger key={module} value={module}>
              <span className='flex items-center gap-2'>
                <span className='text-2xl'>{icon}</span>
                <span className='capitalize'>{module}</span>
              </span>
            </Tabs.Trigger>
          ))}
        </Tabs.List>

        <div className='flex flex-col gap-6 max-h-[60vh] overflow-y-auto'>
          {moduleCharts.map(({ module, chartData }) => (
            <Tabs.Content key={module} value={module}>
              <div className='p-4 flex flex-col gap-2'>
                <div className='w-full h-[500px] flex items-center justify-center'>
                  {chartData &&
                  chartData.states &&
                  chartData.states.length > 0 ? (
                    <StateChart chartData={chartData} />
                  ) : (
                    <span className='text-gray-400'>
                      No state chart data available.
                    </span>
                  )}
                </div>
              </div>
            </Tabs.Content>
          ))}
        </div>
      </Tabs.Root>
    </div>
  );
};
