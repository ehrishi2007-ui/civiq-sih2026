import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ProfileWizard from './pages/ProfileWizard';
import Dashboard from './pages/Dashboard';
import SchemeDetail from './pages/SchemeDetail';
import AskChat from './pages/AskChat';
import MythBuster from './pages/MythBuster';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<ProfileWizard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/scheme/:id" element={<SchemeDetail />} />
          <Route path="/ask" element={<AskChat />} />
          <Route path="/myths" element={<MythBuster />} />
        </Routes>
      </main>
    </div>
  );
}
