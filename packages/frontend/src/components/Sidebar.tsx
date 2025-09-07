import React from 'react';
import { NavLink } from 'react-router-dom';
import { Calendar, Clipboard } from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white p-6">
      <h1 className="text-xl font-bold mb-6">Codexia</h1>
      <nav className="space-y-3">
        <NavLink 
          to="/brief" 
          className={({ isActive }) => 
            `flex items-center gap-2 transition-colors ${
              isActive ? 'text-white' : 'text-slate-300 hover:text-white'
            }`
          }
        >
          <Calendar size={18} /> Morning Brief
        </NavLink>
        <NavLink 
          to="/" 
          end
          className={({ isActive }) => 
            `flex items-center gap-2 transition-colors ${
              isActive ? 'text-white' : 'text-slate-300 hover:text-white'
            }`
          }
        >
          <Clipboard size={18} /> Workbench
        </NavLink>
      </nav>
    </aside>
  );
}