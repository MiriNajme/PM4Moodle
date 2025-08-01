import React, {
  createContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
} from "react";
import {
  getCourses,
  getModules,
  runExtraction,
  type CourseModel,
  type ExtractionRequest,
  type ModuleType,
  type OcelJsonContent,
} from "../services";
import { buildPivotTable, type OcelPivotTable } from "../utils/pivot";

type AppContextType = {
  modules: ModuleType;
  jsonUrl: string | null;
  imageUrl: string | null;
  jsonContent: OcelJsonContent | null;
  pivot: OcelPivotTable | null;
  isLoading: boolean;
  isLoadingContent: boolean;
  isWorking: boolean;
  courses: CourseModel[];
  selectedCourses: string[];
  setSelectedCourses: React.Dispatch<React.SetStateAction<string[]>>;
  selectedModules: string[];
  setSelectedModules: React.Dispatch<React.SetStateAction<string[]>>;
  selectedEvents: string[];
  setSelectedEvents: React.Dispatch<React.SetStateAction<string[]>>;
  tableFilters: { eventTypes: string[]; objectTypes: string[] };
  setTableFilters: React.Dispatch<
    React.SetStateAction<{ eventTypes: string[]; objectTypes: string[] }>
  >;
  handleExtraction: () => Promise<void>;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

const AppProvider = ({ children }: { children: React.ReactNode }) => {
  const [jsonUrl, setJsonUrl] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [courses, setCourses] = useState<CourseModel[]>([]);
  const [modules, setModules] = useState<ModuleType>({});
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [selectedEvents, setSelectedEvents] = useState<string[]>([]);
  const [tableFilters, setTableFilters] = useState<{
    eventTypes: string[];
    objectTypes: string[];
  }>({
    eventTypes: [],
    objectTypes: [],
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isLoadingContent, setIsLoadingContent] = useState<boolean>(false);
  const [isWorking, setIsWorking] = useState(false);
  const [jsonContent, setJsonContent] = useState<OcelJsonContent | null>(null);

  const pivot = useMemo(
    () =>
      jsonContent
        ? buildPivotTable(jsonContent)
        : { objectTypes: [], eventTypes: [], matrix: {}, cardinality: {} },
    [jsonContent]
  );

  const handleExtraction = useCallback(async () => {
    setIsWorking(true);
    setJsonUrl(null);
    setImageUrl(null);
    setJsonContent(null);
    setTableFilters({ eventTypes: [], objectTypes: [] });

    try {
      const request: ExtractionRequest = {
        courses: selectedCourses.map(id => +id),
        modules: {},
      };

      if (selectedModules && selectedModules.length > 0) {
        selectedModules.forEach((module) => {
          if (selectedEvents && selectedEvents.length > 0) {
            request.modules[module] = selectedEvents
              .filter((event) => event.startsWith(module))
              .map((event) => event.split("__")[1]);
          } else {
            request.modules[module] = Object.keys(modules[module] ?? {}) ?? [];
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
  }, [selectedModules, selectedEvents, modules, selectedCourses]);

  useEffect(() => {
    if (!jsonUrl) return;

    setIsLoadingContent(true);
    setJsonContent(null);
    setTableFilters({ eventTypes: [], objectTypes: [] });

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
      const courseResp = await getCourses();
      console.log("Courses fetched:", courseResp);
      setCourses(courseResp);
      setIsLoading(false);
    };
    fetchModules();
  }, []);

  return (
    <AppContext.Provider
      value={{
        modules,
        courses,
        isLoading,
        isLoadingContent,
        isWorking,
        jsonUrl,
        imageUrl,
        jsonContent,
        pivot,
        selectedCourses,
        setSelectedCourses,
        selectedModules,
        setSelectedModules,
        selectedEvents,
        setSelectedEvents,
        tableFilters,
        setTableFilters,
        handleExtraction,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export { AppContext, AppProvider };
