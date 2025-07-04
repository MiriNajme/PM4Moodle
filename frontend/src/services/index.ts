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

export const getModules = async (): Promise<Record<string, string[]>> => {
  try {
    const response = await axios.get<Record<string, string[]>>(
      `${BASE_URL}/modules`
    );
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
