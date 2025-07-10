import React from "react";
import { Button, Text, Callout } from "@radix-ui/themes";
import { Label } from "./ui/label";
import Spinner from "./ui/Spinner";
import { Combobox } from "./ui/combobox";
import { ImageButton } from "./ui/ImageButton";
import { ExclamationTriangleIcon } from "@radix-ui/react-icons";
import { useAppContext } from "../context/useAppContext";

const Extractor = React.memo(() => {
  const {
    selectedModules,
    selectedEvents,
    modules,
    jsonUrl,
    imageUrl,
    isLoading,
    isWorking,
    setSelectedEvents,
    setSelectedModules,
    handleExtraction,
  } = useAppContext();

  if (isLoading) {
    return (
      <div className='flex justify-center items-center h-full pt-10'>
        <Spinner className='w-20 h-20 fill-blue-400' />
      </div>
    );
  }

  return (
    <div className='flex flex-col mt-4 gap-8'>
      <Text className='mb-4'>
        Select modules and their events to generate your OCEL and OCDFG outputs.
      </Text>

      <div className='flex flex-col gap-6'>
        <div>
          <Label className='block mb-2'>Select Modules:</Label>
          <Combobox
            id='module-select'
            placeholder='Choose module(s)'
            value={selectedModules}
            onValueChange={(newModules) => {
              setSelectedModules(newModules.sort());
              setSelectedEvents((prevEvents) =>
                prevEvents.filter((eventValue) => {
                  const module = eventValue.split("__")[0];
                  return newModules.includes(module);
                })
              );
            }}
            options={Object.keys(modules).map((module) => ({
              value: module,
              label: module,
            }))}
          />
        </div>

        <div>
          <Label className='block mb-2'>Select Events:</Label>
          <Combobox
            id='event-select'
            placeholder='Choose event(s)'
            value={selectedEvents}
            onValueChange={setSelectedEvents}
            options={selectedModules.flatMap((module) =>
              Object.keys(modules[module] ?? [])
                .sort()
                .map((event) => ({
                  value: `${module}__${event}`,
                  label: `${module} → ${event}`,
                }))
            )}
          />
        </div>

        <div className='flex justify-end items-center gap-6'>
          <Button
            disabled={isWorking}
            onClick={() => handleExtraction()}
            className='cursor-pointer'
            variant='solid'
            highContrast
          >
            {isWorking ? (
              <>
                <Spinner className='mr-2' /> Processing...
              </>
            ) : (
              "Run Extraction"
            )}
          </Button>
        </div>
        <div>
          {isWorking && (
            <Callout.Root color='blue' variant='surface' role='alert'>
              <Callout.Icon>
                <Spinner className='w-8 h-8 fill-blue-800' />
              </Callout.Icon>
              <Callout.Text>
                Processing and generating the files might takes couple of
                minutes.
              </Callout.Text>
            </Callout.Root>
          )}
        </div>

        {jsonUrl && !imageUrl && (
          <div className='w-full flex gap-4 p-4 rounded-lg mt-6'>
            <Callout.Root color='red' variant='surface' role='alert'>
              <Callout.Icon>
                <ExclamationTriangleIcon />
              </Callout.Icon>
              <Callout.Text>
                The selected event(s) do(es)n't exist.
              </Callout.Text>
            </Callout.Root>
          </div>
        )}
        {imageUrl && (
          <div className='w-full flex justify-between gap-4 p-4 rounded-lg mt-6'>
            <ImageButton
              title='View DFG Diagram'
              description='Click to view the generated DFG diagram.'
              imageUrl={imageUrl ?? ""}
              isJson={false}
              onClick={() =>
                window.open(`./preview/image?url=${encodeURIComponent(imageUrl || "")}`, "_blank")
              }
            />
            <ImageButton
              title='View JSON Output'
              description='Click to view the generated JSON output.'
              imageUrl={jsonUrl ?? ""}
              isJson={true}
              onClick={() =>
                window.open(`./preview/json?url=${encodeURIComponent(jsonUrl || "")}`, "_blank")
              }
            />
          </div>
        )}
      </div>
    </div>
  );
});

export default Extractor;
