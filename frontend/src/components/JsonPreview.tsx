import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { JsonEditor as Editor } from "jsoneditor-react";
import "jsoneditor-react/es/editor.min.css";
import Ajv from "ajv";

const ajv = new Ajv({ allErrors: true, verbose: true });

export default function JsonPreview() {
  const [params] = useSearchParams();
  const url = useMemo(() => params.get("url") ?? "", [params]);

  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!url) return;
    setLoading(true);
    setError(null);
    fetch(url)
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
        return res.json();
      })
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [url]);

  if (!url) {
    return <div className='text-gray-500'>No URL provided.</div>;
  }
  if (loading) {
    return <div className='text-gray-500'>Loading...</div>;
  }
  if (error) {
    return <div className='text-red-500'>Error: {error}</div>;
  }
  if (!data) {
    return <div className='text-gray-500'>No data to display.</div>;
  }

  return (
    <div className='w-full min-h-[95dvh] bg-gray-50 py-10 px-6 rounded-lg shadow-xl overflow-auto'>
      <Editor value={data} ajv={ajv} search={true} theme='ace/theme/github' />
    </div>
  );
}
