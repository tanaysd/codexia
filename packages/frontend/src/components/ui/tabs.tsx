import * as React from "react";
import { cn } from "./utils";

export function Tabs({ value, onChange, items }: {
  value: string;
  onChange: (v: string) => void;
  items: { key: string; label: string; icon?: React.ReactNode }[]
}) {
  return (
    <div className="flex gap-3 flex-wrap">
      {items.map(it => (
        <button key={it.key} onClick={() => onChange(it.key)}
          className={cn("h-10 px-4 rounded-lg border border-border bg-white text-slate-700 shadow-soft hover:bg-slate-50 flex items-center gap-2",
            value === it.key && "bg-brand text-white border-transparent hover:opacity-95")}>
          {it.icon}{it.label}
        </button>
      ))}
    </div>
  );
}