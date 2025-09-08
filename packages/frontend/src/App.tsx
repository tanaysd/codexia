import React from "react";
import { Link, Outlet, createBrowserRouter, RouterProvider } from "react-router-dom";
import { Calendar, ClipboardList, Brain, TrendingUp, MessageCircle, Heart, Shield, Target } from "lucide-react";
import { BriefPage } from "./pages/BriefPage";
import { WorkbenchPage } from "./pages/WorkbenchPage";
import { PersonalizationPage } from "./pages/PersonalizationPage";
import { ChatPage } from "./pages/ChatPage";
import { AboutPage } from "./pages/AboutPage";
import { PreventionPage } from "./pages/PreventionPage";
import { TrainingGymPage } from "./pages/TrainingGymPage";

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="h-full grid grid-cols-[260px_1fr]">
      <aside className="bg-slate-900 text-white p-6 space-y-6">
        <div className="text-2xl font-bold tracking-tight">Codexia</div>
        <nav className="space-y-2">
          <Link to="/brief" className="flex items-center gap-2 hover:text-slate-300 py-2 px-2 rounded transition-colors">
            <Calendar size={18}/> Morning Brief
          </Link>
          <Link to="/chat" className="flex items-center gap-2 hover:text-slate-300 py-2 px-2 rounded transition-colors">
            <MessageCircle size={18}/> Chat with Alex
            <span className="ml-auto bg-green-500 text-white text-xs px-2 py-0.5 rounded-full">🔥</span>
          </Link>
          <Link to="/training" className="flex items-center gap-2 hover:text-slate-300 py-2 px-2 rounded transition-colors">
            <Target size={18}/> Training Gym
            <span className="ml-auto bg-purple-500 text-white text-xs px-2 py-0.5 rounded-full">NEW</span>
          </Link>
          <Link to="/workbench" className="flex items-center gap-2 hover:text-slate-300 py-2 px-2 rounded transition-colors">
            <ClipboardList size={18}/> Workbench
            <span className="ml-auto bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">BETA</span>
          </Link>
          <Link to="/prevention" className="flex items-center gap-2 hover:text-slate-300 py-2 px-2 rounded transition-colors">
            <Shield size={18}/> Denial Prevention
            <span className="ml-auto bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">💰</span>
          </Link>
          <Link to="/insights" className="flex items-center gap-2 hover:text-slate-300 py-2 px-2 rounded transition-colors">
            <Brain size={18}/> AI Insights
            <span className="ml-auto bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">New</span>
          </Link>
        </nav>
        
        {/* ROI Impact Card */}
        <div className="mt-8 p-4 bg-gradient-to-r from-green-800 to-emerald-800 rounded-lg border border-green-700">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-4 h-4 text-green-300" />
            <span className="text-sm font-medium text-green-300">Q1 2024 Impact</span>
          </div>
          <div className="text-lg font-bold text-white mb-1">$2.8M Saved</div>
          <p className="text-xs text-green-200 mb-3">
            1,247 denials prevented • 2,847% ROI
          </p>
          <Link to="/prevention" className="text-xs text-green-300 hover:text-green-200 underline">
            View full report →
          </Link>
        </div>
        
        {/* Why We Built This */}
        <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
          <div className="flex items-center gap-2 mb-2">
            <Heart className="w-4 h-4 text-red-400" />
            <span className="text-sm font-medium text-red-400">Why We Built This</span>
          </div>
          <p className="text-xs text-slate-300 mb-3">
            Built by RCM experts, for RCM experts. We believe you deserve AI that amplifies your expertise.
          </p>
          <Link to="/about" className="text-xs text-blue-400 hover:text-blue-300 underline">
            Read our story →
          </Link>
        </div>
      </aside>
      <main className="bg-gray-50 overflow-y-auto">{children}</main>
    </div>
  );
}

const router = createBrowserRouter([
  { path: "/", element: <Shell><ChatPage/></Shell> },
  { path: "/brief", element: <Shell><BriefPage/></Shell> },
  { path: "/workbench", element: <Shell><WorkbenchPage/></Shell> },
  { path: "/chat", element: <Shell><ChatPage/></Shell> },
  { path: "/training", element: <Shell><TrainingGymPage/></Shell> },
  { path: "/prevention", element: <Shell><PreventionPage/></Shell> },
  { path: "/insights", element: <Shell><PersonalizationPage/></Shell> },
  { path: "/about", element: <Shell><AboutPage/></Shell> }
]);

export default function App() { 
  return <RouterProvider router={router}/>; 
}