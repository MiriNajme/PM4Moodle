/* eslint-disable @typescript-eslint/strict-boolean-expressions */
import * as React from "react";

import { cn } from "../../utils/utils";
import { Button } from "./button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "./command";
import { Popover, PopoverContent, PopoverTrigger } from "./popover";
import { RxChevronUp, RxCross2 } from "react-icons/rx";
import { PopoverPortal } from "@radix-ui/react-popover";

interface ComboboxProps {
  options: { value: string; label: string | React.FC }[];
  onValueChange: (value: string[]) => unknown;
  value: string[];
  name?: string;
  id?: string;
  disabled?: boolean;
  title?: string;
  placeholder?: string;
}

export function Combobox({
  options,
  onValueChange,
  value,
  name,
  id,
  disabled,
  title,
  placeholder,
}: ComboboxProps) {
  const [open, setOpen] = React.useState(false);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      {/* Label support */}
      {id && (
        <input
          type='text'
          id={id}
          className='sr-only'
          aria-hidden='true'
          tabIndex={-1}
          readOnly
          value={value.join(", ")}
        />
      )}

      <PopoverTrigger asChild disabled={disabled}>
        <div
          id={id}
          role='combobox'
          aria-expanded={open}
          aria-disabled={disabled}
          tabIndex={0}
          onClick={() => setOpen(!open)}
          className={cn(
            "w-full border border-gray-300 rounded-md bg-white px-3 py-2 flex flex-wrap items-start gap-1 focus:outline-none focus:ring-2 focus:ring-indigo-500",
            disabled && "opacity-50 cursor-not-allowed"
          )}
        >
          {value.length > 0 ? (
            value.map((val) => {
              const option = options.find((o) => o.value === val);
              return (
                <span
                  key={val}
                  className='flex items-center bg-indigo-100  text-indigo-700 rounded px-2 py-0.5 text-xs'
                >
                  {option?.label ?? val}
                  <button
                    type='button'
                    onClick={(e) => {
                      e.stopPropagation();
                      onValueChange(value.filter((v) => v !== val));
                    }}
                    className='ml-1'
                    tabIndex={-1}
                  >
                    <RxCross2 className='h-3 w-3' />
                  </button>
                </span>
              );
            })
          ) : (
            <span className='text-gray-400'>
              {placeholder || name || "Select"}
            </span>
          )}
          <span className='ml-auto flex items-center gap-1'>
            <RxChevronUp
              className={cn(
                "h-4 w-4 transition-transform",
                open && "rotate-180"
              )}
            />
          </span>
        </div>
      </PopoverTrigger>

      <PopoverPortal>
        <PopoverContent
          className='w-full p-0 max-h-[40vh] overflow-auto z-50 bg-white border border-gray-200 shadow-xl rounded-md'
          side='bottom'
          align='start'
        >
          <Command>
            <CommandInput placeholder='Search...' />
            <CommandEmpty>No options found.</CommandEmpty>
            <CommandGroup>
              {options.map((o) => {
                const isSelected = value.includes(o.value);
                return (
                  <CommandItem
                    key={o.value}
                    value={o.value}
                    className={cn(
                      "cursor-pointer flex items-center gap-2 px-3 py-2",
                      isSelected ? "bg-indigo-50 text-indigo-700" : ""
                    )}
                    onSelect={() => {
                      const isSelected = value.includes(o.value);
                      const newValue = isSelected
                        ? value.filter((v) => v !== o.value)
                        : [...value, o.value];
                      onValueChange(newValue);
                    }}
                  >
                    <span
                      className={cn(
                        "inline-block h-4 w-4 border rounded-sm border-gray-400 flex items-center justify-center",
                        value.includes(o.value) ? "bg-indigo-600" : "bg-white"
                      )}
                    >
                      {value.includes(o.value) && (
                        <div className='h-2 w-2 bg-white rounded-sm' />
                      )}
                    </span>
                    {typeof o.label === "string" ? o.label : <o.label />}
                  </CommandItem>
                );
              })}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </PopoverPortal>
    </Popover>
  );
}
