import React from "react";
import { Tabs, Text } from "@radix-ui/themes";
import { useAppContext } from "../context/useAppContext";
import Spinner from "./ui/Spinner";
import OcelVerificationCardinality from "./Cardinality";
import OcelVerificationFrequency from "./Frequency";
import TableFilterDialog from "./TableFilterDialog";

const OcelVerificationMatrix = React.memo(() => {
  const { pivot, isLoadingContent } = useAppContext();

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

  return (
    <div className='w-full'>
      <Tabs.Root defaultValue='frequency'>
        <Tabs.List className='relative mb-4'>
          <Tabs.Trigger value='frequency'>
            <span>Frequency</span>
          </Tabs.Trigger>
          <Tabs.Trigger value='cardinality'>
            <span>Cardinality</span>
          </Tabs.Trigger>

          <TableFilterDialog />
        </Tabs.List>

        <div className='flex flex-col gap-6'>
          <Tabs.Content value='frequency'>
            <OcelVerificationFrequency />
          </Tabs.Content>
          <Tabs.Content value='cardinality'>
            <OcelVerificationCardinality />
          </Tabs.Content>
        </div>
      </Tabs.Root>
    </div>
  );
});

export default OcelVerificationMatrix;
