import { NavLink } from 'react-router-dom';

export default function Header() {
  return (
    <header className="p-2 border-b flex justify-between items-center">
      <div className="flex items-center gap-4">
        <img src="/logo.svg" alt="logo" className="h-6" />
        <nav className="flex gap-4">
          <NavLink to="/" end>Workbench</NavLink>
          <NavLink to="/brief">Morning Brief</NavLink>
        </nav>
      </div>
      <div className="flex gap-2">
        <button>New</button>
        <button>Load Sample</button>
        <button>Save</button>
      </div>
    </header>
  );
}
