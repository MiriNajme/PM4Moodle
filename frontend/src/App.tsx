import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ImagePreview from "./pages/ImagePreview";
import JsonPreview from "./pages/JsonPreview";
import { AppProvider } from "./context/AppContext";

export default function App() {
  return (
    <AppProvider>
      <div className='w-full min-h-screen box-border'>
        <main>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/preview/image' element={<ImagePreview />} />
            <Route path='/preview/json' element={<JsonPreview />} />
          </Routes>
        </main>
      </div>
    </AppProvider>
  );
}
