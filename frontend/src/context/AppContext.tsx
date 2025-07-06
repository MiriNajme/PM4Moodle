import React, {
  createContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
} from "react";
import { getModules, runExtraction, type OCEL_Json_content } from "../services";
import { buildPivotTable, type OCEL_Pivot_Table } from "../utils/pivot";

type AppContextType = {
  modules: Record<string, string[]>;
  jsonUrl: string | null;
  imageUrl: string | null;
  jsonContent: OCEL_Json_content | null;
  pivot: OCEL_Pivot_Table | null;
  isLoading: boolean;
  isLoadingContent: boolean;
  isWorking: boolean;
  selectedModules: string[];
  setSelectedModules: React.Dispatch<React.SetStateAction<string[]>>;
  selectedEvents: string[];
  setSelectedEvents: React.Dispatch<React.SetStateAction<string[]>>;
  handleExtraction: () => Promise<void>;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

const AppProvider = ({ children }: { children: React.ReactNode }) => {
  const [jsonUrl, setJsonUrl] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [modules, setModules] = useState<Record<string, string[]>>({});
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [selectedEvents, setSelectedEvents] = useState<string[]>([]);

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isLoadingContent, setIsLoadingContent] = useState<boolean>(false);
  const [isWorking, setIsWorking] = useState(false);
  const [jsonContent, setJsonContent] = useState<OCEL_Json_content | null>(
    null
  );

  const pivot = useMemo(
    () =>
      jsonContent
        ? buildPivotTable(jsonContent)
        : { objectTypes: [], eventTypes: [], matrix: {} },
    [jsonContent]
  );

  const handleExtraction = useCallback(async () => {
    setIsWorking(true);
    setJsonUrl(null);
    setImageUrl(null);
    setJsonContent(null);

    try {
      const request: Record<string, string[]> = {};

      if (selectedModules && selectedModules.length > 0) {
        selectedModules.forEach((module) => {
          if (selectedEvents && selectedEvents.length > 0) {
            request[module] = selectedEvents
              .filter((event) => event.startsWith(module))
              .map((event) => event.split("__")[1]);
          } else {
            request[module] = modules[module] || [];
          }
        });
      }

      const response = await runExtraction(request);
      setJsonUrl(response.json_url);
      setImageUrl(response.image_url);
    } catch (error) {
      console.error("Error during extraction:", error);
      alert("An error occurred during extraction.");
    } finally {
      setIsWorking(false);
    }
  }, [selectedModules, selectedEvents, modules]);

  useEffect(() => {
    if (!jsonUrl) return;

    setIsLoadingContent(true);
    setJsonContent(null);
    fetch(jsonUrl)
      .then((response) => response.json())
      .then((data) => setJsonContent(data))
      .catch((error) => console.error("Error fetching JSON:", error))
      .finally(() => setIsLoadingContent(false));
  }, [jsonUrl]);

  useEffect(() => {
    setIsLoading(true);
    const fetchModules = async () => {
      const resp = await getModules();
      setModules(resp);
      setIsLoading(false);
    };
    fetchModules();
  }, []);

  return (
    <AppContext.Provider
      value={{
        modules,
        isLoading,
        isLoadingContent,
        isWorking,
        jsonUrl,
        imageUrl,
        jsonContent,
        pivot,
        selectedModules,
        setSelectedModules,
        selectedEvents,
        setSelectedEvents,
        handleExtraction,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export { AppContext, AppProvider };
