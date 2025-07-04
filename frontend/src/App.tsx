// import { Routes, Route, Link } from 'react-router-dom'
// import Home from './components/Home'
// import Extractor from './components/Extractor'

// export default function App() {
//   return (
//     <div className="min-h-screen bg-gray-100">
//       <nav className="bg-white shadow p-4 flex justify-between">
//         <Link to="/" className="text-blue-600 font-bold">Home</Link>
//         <Link to="/extract" className="text-blue-600">Extract OCEL</Link>
//       </nav>
//       <main className="p-6">
//         <Routes>
//           <Route path="/" element={<Home />} />
//           <Route path="/extract" element={<Extractor />} />
//         </Routes>
//       </main>
//     </div>
//   )
// }

import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Extractor from "./components/Extractor";
import ImagePreview from "./components/ImagePreview";
import JsonPreview from "./components/JsonPreview";

export default function App() {
  return (
    <div className='w-full min-h-screen'>
      <main className='p-6'>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/extract' element={<Extractor />} />
          <Route path='/preview/image' element={<ImagePreview />} />
          <Route path='/preview/json' element={<JsonPreview />} />
        </Routes>
      </main>
    </div>
  );
}
