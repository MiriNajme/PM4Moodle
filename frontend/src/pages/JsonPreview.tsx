import { JsonEditor as Editor } from "jsoneditor-react";
import "jsoneditor-react/es/editor.min.css";
import Ajv from "ajv";
import { useAppContext } from "../context/useAppContext";

const ajv = new Ajv({ allErrors: true, verbose: true });

export default function JsonPreview() {
  const { jsonUrl, jsonContent, isLoadingContent } = useAppContext();

  if (!jsonUrl) {
    return <div className='text-gray-500'>No URL provided.</div>;
  }
  if (isLoadingContent) {
    return <div className='text-gray-500'>Loading...</div>;
  }

  if (!jsonContent || Object.keys(jsonContent).length === 0) {
    return <div className='text-gray-500'>No data to display.</div>;
  }

  return (
    <div className='w-full min-h-[95dvh] bg-gray-50 py-10 px-6 rounded-lg shadow-xl overflow-auto'>
      <Editor
        value={jsonContent}
        ajv={ajv}
        search={true}
        theme='ace/theme/github'
      />
    </div>
  );
}
