import React, { useState } from "react";
import { Button, Dialog, Flex } from "@radix-ui/themes";
import { useAppContext } from "../context/useAppContext";
import { Funnel } from "./icons/Funnel";
import { Combobox } from "./ui/combobox";
import { Label } from "./ui/label";

const TableFilterDialog = React.memo(() => {
  const { pivot, setTableFilters } = useAppContext();
  const [selectedEvents, setSelectedEvents] = useState<string[]>([]);
  const [selectedObjects, setSelectedObjects] = useState<string[]>([]);

  const setFilters = () => {
    setTableFilters({
      eventTypes: selectedEvents,
      objectTypes: selectedObjects,
    });
  };
  
  const resetFilters = () => {
    setSelectedEvents([]);
    setSelectedObjects([]);
    setTableFilters({
      eventTypes: [],
      objectTypes: [],
    });
  };

  return (
    <Dialog.Root>
      <Dialog.Trigger>
        <Button
          color='gray'
          variant='ghost'
          title='Filter table data'
          className='!absolute !right-2 !top-2 cursor-pointer'
        >
          <Funnel />
        </Button>
      </Dialog.Trigger>

      <Dialog.Content minWidth='600px' maxWidth='50vw'>
        <Dialog.Title>Select filters</Dialog.Title>
        <Dialog.Description size='2' mb='4'></Dialog.Description>

        <div className='flex flex-col gap-6'>
          <div>
            <Label className='block mb-2'>Select Events:</Label>
            <Combobox
              id='event-select'
              placeholder='Choose Event(s)'
              value={selectedEvents}
              onValueChange={setSelectedEvents}
              options={(pivot?.eventTypes ?? []).sort().map((event) => ({
                value: event,
                label: event,
              }))}
            />
          </div>

          <div>
            <Label className='block mb-2'>Select Objects:</Label>
            <Combobox
              id='object-select'
              placeholder='Choose object(s)'
              value={selectedObjects}
              onValueChange={setSelectedObjects}
              options={(pivot?.objectTypes ?? []).sort().map((objType) => ({
                value: objType,
                label: objType,
              }))}
            />
          </div>
        </div>

        <Flex gap='3' mt='8' justify='end'>
          <Dialog.Close>
            <Button variant='soft' color='gray'>
              Close
            </Button>
          </Dialog.Close>
          <Dialog.Close>
            <Button variant='soft' color='gray' onClick={resetFilters}>
              Reset
            </Button>
          </Dialog.Close>
          <Dialog.Close>
            <Button onClick={setFilters}>Set</Button>
          </Dialog.Close>
        </Flex>
      </Dialog.Content>
    </Dialog.Root>
  );
});

export default TableFilterDialog;
