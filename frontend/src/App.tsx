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
