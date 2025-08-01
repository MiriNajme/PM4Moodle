import React, { useState } from "react";
import * as Tabs from "@radix-ui/react-tabs";
import Extractor from "../components/Extractor.tsx";
import MoodleHeading from "../components/MoodleHeading.tsx";
import OcelVerificationMatrix from "../components/VerificationMatrix.tsx";
import { VerificationStateChart } from "../components/VerificationStateChart.tsx";
import { useAppContext } from "../context/useAppContext.ts";
import Spinner from "../components/ui/Spinner.tsx";

const Home = React.memo(() => {
  const [activeTab, setActiveTab] = useState<string>("extraction");
  const { isLoading } = useAppContext();

  if (isLoading) {
    return (
      <div className='flex justify-center items-center h-full pt-10'>
        <Spinner className='w-20 h-20 fill-blue-400' />
      </div>
    );
  }

  return (
    <div className='w-full mx-auto lg:max-w-2/3'>
      <div className='min-h-screen flex justify-center py-4 px-1'>
        <div className='w-full bg-white shadow-xl rounded-xl p-8'>
          <MoodleHeading />
          <Tabs.Root
            defaultValue='extraction'
            value={activeTab}
            onValueChange={setActiveTab}
          >
            <Tabs.List className='flex gap-4 mb-2' color='orange'>
              <Tabs.Trigger
                value='extraction'
                className='px-4 py-2 font-semibold transition-colors rounded-none relative
                  data-[state=active]:border-b-2 data-[state=active]:border-orange-300 data-[state=active]:text-blue-950
                  data-[state=active]:shadow-md'
              >
                Extraction
              </Tabs.Trigger>
              <Tabs.Trigger
                value='verification'
                className='px-4 py-2 font-semibold transition-colors rounded-none relative
                  data-[state=active]:border-b-2 data-[state=active]:border-orange-300 data-[state=active]:text-blue-950
                  data-[state=active]:shadow-md'
              >
                Verification matrix
              </Tabs.Trigger>
              <Tabs.Trigger
                value='statechart'
                className='px-4 py-2 font-semibold transition-colors rounded-none relative
                  data-[state=active]:border-b-2 data-[state=active]:border-orange-300 data-[state=active]:text-blue-950
                  data-[state=active]:shadow-md'
              >
                State Chart Diagram
              </Tabs.Trigger>
            </Tabs.List>
            <div
              className='w-full h-1 mb-2 rounded-full'
              style={{
                background:
                  "linear-gradient(90deg, #012846 0%, #6366f1 40%, #f59e42 100%)",
                boxShadow: "0 2px 8px 0 rgba(99,102,241,0.15)",
              }}
            />
            <Tabs.Content value='extraction'>
              <Extractor />
            </Tabs.Content>
            <Tabs.Content value='verification'>
              <OcelVerificationMatrix />
            </Tabs.Content>
            <Tabs.Content value='statechart'>
              <VerificationStateChart />
            </Tabs.Content>
          </Tabs.Root>
        </div>
      </div>
    </div>
  );
});

export default Home;
