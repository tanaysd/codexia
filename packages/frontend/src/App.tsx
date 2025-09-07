import React from "react";
import { Link, Outlet, createBrowserRouter, RouterProvider } from "react-router-dom";
import { Calendar, ClipboardList } from "lucide-react";
import { BriefPage } from "./pages/BriefPage";
import { WorkbenchPage } from "./pages/WorkbenchPage";

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="h-full grid grid-cols-[260px_1fr]">
      <aside className="bg-slate-900 text-white p-6 space-y-6">
        <div className="text-2xl font-bold tracking-tight">Codexia</div>
        <nav className="space-y-2">
          <Link to="/brief" className="flex items-center gap-2 hover:text-slate-300"><Calendar size={18}/> Morning Brief</Link>
          <Link to="/workbench" className="flex items-center gap-2 hover:text-slate-300"><ClipboardList size={18}/> Workbench</Link>
        </nav>
      </aside>
      <main className="bg-bg p-8 overflow-y-auto">{children}</main>
    </div>
  );
}

const router = createBrowserRouter([
  { path: "/", element: <Shell><BriefPage/></Shell> },
  { path: "/brief", element: <Shell><BriefPage/></Shell> },
  { path: "/workbench", element: <Shell><WorkbenchPage/></Shell> }
]);

export default function App() { 
  return <RouterProvider router={router}/>; 
}