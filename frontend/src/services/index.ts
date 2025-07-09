import axios from "axios";
const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";

export const getObjects = async (): Promise<string[]> => {
  try {
    const response = await axios.get<string[]>(`${BASE_URL}/objects`);
    return response.data;
  } catch (error) {
    console.error("Error running analysis:", error);
    throw error;
  }
};

export const getEventTypes = async (): Promise<string[]> => {
  try {
    const response = await axios.get<string[]>(`${BASE_URL}/event-types`);
    return response.data;
  } catch (error) {
    console.error("Error running analysis:", error);
    throw error;
  }
};

export type ModuleType = Record<string, Record<string, string>>;

export const getModules = async (): Promise<ModuleType> => {
  try {
    const response = await axios.get<ModuleType>(`${BASE_URL}/modules`);
    return response.data;
  } catch (error) {
    console.error("Error running analysis:", error);
    throw error;
  }
};

export type ExtractionRequest = Record<string, string[]>;
export type ExtractionResponse = {
  image_url: string;
  json_url: string;
};

export const runExtraction = async (data: ExtractionRequest) => {
  try {
    const response = await axios.post<ExtractionResponse>(
      `${BASE_URL}/run-extraction`,
      data
    );

    return response.data;
  } catch (error) {
    console.error("Error running analysis:", error);
    throw error;
  }
};

export type DbConfigModel = {
  host: string;
  port: number;
  user: string;
  password: string;
  db_name: string;
};

export const getDbConfig = async () => {
  try {
    const response = await axios.get<DbConfigModel>(
      `${BASE_URL}/get-db-config`
    );
    return response.data;
  } catch (error) {
    console.error("Error to get db config:", error);
    throw error;
  }
};

export const saveDbConfig = async (data: DbConfigModel) => {
  try {
    await axios.post(`${BASE_URL}/set-db-config`, data);
  } catch (error) {
    console.error("Error to set db config:", error);
    throw error;
  }
};

export type OcelTypesModel = {
  name: string;
  attributes: any[];
};

export type OcelRelationshipsModel = {
  objectId: string;
  qualifier: string;
  from?: string;
  to?: string;
};

export type OcelObjectsModel = {
  id: string;
  type: string;
  attributes: any[];
  relationships: OcelRelationshipsModel[];
};

export type OcelEventModel = {
  id: string;
  type: string;
  time: string;
  attributes: any[];
  relationships: OcelRelationshipsModel[];
};

export type OcelJsonContent = {
  objectTypes: OcelTypesModel[];
  eventTypes: OcelTypesModel[];
  objects: OcelObjectsModel[];
  events: OcelEventModel[];
};
