import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ClaimWorkbench from './routes/ClaimWorkbench';
import MorningBrief from './routes/MorningBrief';
import Sidebar from './components/Sidebar';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-50 font-sans">
        <Sidebar />
        <div className="flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<ClaimWorkbench />} />
            <Route path="/brief" element={<MorningBrief />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
