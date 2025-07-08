import React, { useMemo } from "react";
import { StateChart } from "./StateChart";
import { useAppContext } from "../context/useAppContext";

// Define the state mappings for supported modules
const stateMappings: Record<string, Record<string, string>> = {
  assign: {
    create_assign: "created",
    update_assign: "updated",
    submit_group_assign: "submitted",
  },
  url: {
    create_url: "created",
    update_url: "updated",
    view_url: "viewed",
    delete_url: "deleted",
  },
  // Add more modules here as needed
};

const sequenceToStateChart = (states: string[]) => {
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
};

export const VerificationStateChart: React.FC = () => {
  const { jsonContent, selectedModules } = useAppContext();

  // Build chart data for each selected module
  const moduleCharts = useMemo(() => {
    if (!jsonContent || !selectedModules) return [];

    return selectedModules
      .filter((module) => stateMappings[module])
      .map((module) => {
        const mapping = stateMappings[module];
        const relevantEventTypes = Object.keys(mapping);

        // Filter json
        const filteredEvents = (
          jsonContent?.events?.filter(
            (event) => event.type && relevantEventTypes.includes(event.type)
          ) ?? []
        )
          .sort(
            (a, b) => new Date(a.time).getTime() - new Date(b.time).getTime()
          )
          .reduce((acc, event) => {
            const eventType = mapping[event.type] || event.type;
            if (!acc.includes(eventType)) {
              acc.push(eventType);
            }
            return acc;
          }, []) as string[];

        // const chartData = getStateChartData(filteredEvents, mapping);
        // Debug: log chartData for each module
        // console.log(`chartData for module "${module}":`, chartData);
        return {
          module,
          icon: module === "assign" ? "📄" : module === "url" ? "🔗" : "📦",
          chartData: sequenceToStateChart(filteredEvents),
        };
      });
  }, [jsonContent, selectedModules]);

  console.log("moduleCharts:", moduleCharts);

  if (!jsonContent)
    return (
      <div className='text-gray-500 text-center py-8'>
        No extracted log found. Run extraction first.
      </div>
    );

  return (
    <div className='p-6 bg-gray-50 min-h-[60vh]'>
      <h2 className='text-2xl font-semibold mb-4 text-center'>
        Module State Charts
      </h2>
      <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
        {moduleCharts.map(({ module, icon, chartData }) => (
          <div
            key={module}
            className='bg-white rounded-2xl shadow-md p-4 flex flex-col items-center'
          >
            <div className='flex items-center mb-2'>
              <span className='text-2xl mr-2'>{icon}</span>
              <span className='text-lg font-bold capitalize'>
                {module} Module
              </span>
            </div>
            <div className='w-full h-64 flex items-center justify-center'>
              {chartData && chartData.states && chartData.states.length > 0 ? (
                <StateChart chartData={chartData} />
              ) : (
                <span className='text-gray-400'>
                  No state chart data available.
                </span>
              )}
            </div>
            {/* <div className='flex flex-wrap gap-2 justify-center mt-3'>
              {chartData &&
                chartData.states &&
                chartData.states.length > 0 &&
                chartData.states.map((state) => (
                  <span
                    key={state}
                    className='bg-blue-100 text-blue-900 rounded-full px-3 py-1 text-sm font-semibold'
                  >
                    {state}
                  </span>
                ))}
            </div> */}
          </div>
        ))}
      </div>
    </div>
  );
};
