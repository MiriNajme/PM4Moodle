import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Extractor() {
  const [modules, setModules] = useState<string[]>([])

  useEffect(() => {
    axios.get('/api/modules')  // your Flask endpoint
      .then(res => setModules(res.data))
      .catch(err => console.error('Failed to load modules', err))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Available Modules</h2>
      <ul className="list-disc pl-5">
        {modules.map((mod, idx) => (
          <li key={idx}>{mod}</li>
        ))}
      </ul>
    </div>
  )
}
