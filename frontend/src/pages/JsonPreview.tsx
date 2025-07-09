import { useEffect, useState } from "react";
import { JsonEditor as Editor } from "jsoneditor-react";
import "jsoneditor-react/es/editor.min.css";
import Ajv from "ajv";
import Spinner from "../components/ui/Spinner";

const ajv = new Ajv({ allErrors: true, verbose: true });

export default function JsonPreview() {
  const [jsonContent, setJsonContent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const urlParams = new URLSearchParams(window.location.search);
  const jsonUrl = urlParams.get("url") || "";

  useEffect(() => {
    if (jsonUrl && !jsonContent) {
      setIsLoading(true);
      fetch(jsonUrl)
        .then((response) => response.json())
        .then((data) => {
          setJsonContent(data);
          setIsLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching JSON from URL:", error);
          setIsLoading(false);
        });
    }
  }, [jsonUrl, jsonContent]);

  if (!jsonUrl) {
    return <div className='text-gray-500'>No URL provided.</div>;
  }
  if (isLoading) {
    return (
      <div className='flex justify-center items-center h-full pt-10'>
        <Spinner className='w-20 h-20 fill-blue-400' />
      </div>
    );
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
