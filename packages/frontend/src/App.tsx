import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ClaimWorkbench from './routes/ClaimWorkbench';
import MorningBrief from './routes/MorningBrief';
import Header from './components/Header';

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<ClaimWorkbench />} />
        <Route path="/brief" element={<MorningBrief />} />
      </Routes>
    </BrowserRouter>
  );
}
