import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export type RowColType = {
  row: number | null;
  col: number | null;
};

export function groupEventTypesByPostfix(eventTypes: string[]) {
  const groups: Record<string, string[]> = {};
  eventTypes.forEach((eventType) => {
    const parts = eventType.split("_");
    const postfix = parts.length > 1 ? parts[parts.length - 1] : eventType;
    if (!groups[postfix]) groups[postfix] = [];
    groups[postfix].push(eventType);
  });
  return Object.values(groups).flat();
};
