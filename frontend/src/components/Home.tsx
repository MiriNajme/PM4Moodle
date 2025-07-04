import React, { useCallback, useEffect, useState } from "react";
import {
  getModules,
  runExtraction,
  type ExtractionResponse,
} from "../services";
import { Button, Text, Heading, Separator, Callout } from "@radix-ui/themes";
import { Label } from "./ui/label";
import Spinner from "./ui/Spinner";
import { Combobox } from "./ui/combobox";
import { ImageButton } from "./ui/ImageButton";
import { useNavigate } from "react-router-dom";
import { GrDocument } from "react-icons/gr";
import { HiPhoto } from "react-icons/hi2";
import { InfoCircledIcon } from "@radix-ui/react-icons";

const Home = React.memo(() => {
  const navigate = useNavigate();
  const [modules, setModules] = useState<Record<string, string[]>>({});
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [selectedEvents, setSelectedEvents] = useState<string[]>([]);
  const [isWorking, setIsWorking] = useState(false);
  const [result, setResult] = useState<ExtractionResponse | null>(null);

  const handleExtraction = useCallback(async () => {
    setIsWorking(true);
    setResult(null); // Reset result before starting extraction
    try {
      const request: Record<string, string[]> = {};

      if (selectedModules && selectedModules.length > 0) {
        selectedModules.forEach((module) => {
          request[module] = selectedEvents
            .filter((event) => event.startsWith(module))
            .map((event) => event.split("__")[1]);
        });
      }

      const response = await runExtraction(request);
      setResult(response);
    } catch (error) {
      console.error("Error during extraction:", error);
      alert("An error occurred during extraction.");
    } finally {
      setIsWorking(false);
    }
  }, [selectedModules, selectedEvents]);

  useEffect(() => {
    const fetchModules = async () => {
      const resp = await getModules();
      setModules(resp);
    };
    fetchModules();
  }, []);

  return (
    <div className='max-w-4xl mx-auto'>
      <div className='min-h-screen flex justify-center py-10 px-6'>
        <div className='w-full max-w-3xl bg-white shadow-xl rounded-xl p-8'>
          <Heading as='h1' size='6' className='text-center mb-6'>
            Moodle OCEL Extraction
          </Heading>
          <Text align='center' className='mb-4'>
            Select modules and their events to generate your OCEL and OCDFG
            outputs.
          </Text>
          <Separator className='mb-6' />

          <div className='flex flex-col gap-6'>
            <div>
              <Label className='block mb-2'>Select Modules:</Label>
              <Combobox
                id='module-select'
                placeholder='Choose module(s)'
                value={selectedModules}
                onValueChange={(newModules) => {
                  setSelectedModules(newModules.sort());
                  // Remove any events that belong to unselected modules
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
                  (modules[module] || []).sort().map((event) => ({
                    value: `${module}__${event}`,
                    label: `${module} → ${event}`,
                  }))
                )}
              />
            </div>

            <div className='flex justify-end items-center gap-6'>
              {isWorking && (
                <Callout.Root color='blue'>
                  <Callout.Icon>
                    <InfoCircledIcon />
                  </Callout.Icon>
                  <Callout.Text>
                    Processing and generating the files might takes couple of
                    minutes.
                  </Callout.Text>
                </Callout.Root>
              )}
              <Button
                disabled={isWorking}
                onClick={handleExtraction}
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

            {result && (
              <div className='w-full flex gap-4 border-lg border-2 border-gray-100 shadow p-4 rounded-lg mt-6'>
                <ImageButton
                  buttonText='DFG Diagram'
                  title='View DFG Diagram'
                  description='Click to view the generated DFG diagram.'
                  imageUrl={result.image_url}
                  buttonIcon={<HiPhoto width='16' height='16' />}
                  onClick={() =>
                    navigate(`./preview/image/?url=${result.image_url}`)
                  }
                />
                <ImageButton
                  buttonText='OCEL JSON'
                  title='View JSON Output'
                  description='Click to view the generated JSON output.'
                  imageUrl={result.json_url}
                  buttonIcon={<GrDocument width='16' height='16' />}
                  onClick={() =>
                    navigate(`./preview/json/?url=${result.json_url}`)
                  }
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
});

export default Home;
