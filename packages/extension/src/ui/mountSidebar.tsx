import React from 'react';
import { createRoot } from 'react-dom/client';
import Sidebar from './Sidebar';

export function mountSidebar() {
  const existing = document.getElementById('codexia-sidebar-root');
  if (existing) {
    existing.remove();
    return;
  }
  const div = document.createElement('div');
  div.id = 'codexia-sidebar-root';
  document.body.appendChild(div);
  const root = createRoot(div);
  root.render(<Sidebar />);
}
