import * as React from "react";
import { cn } from "./utils";

type V = "neutral" | "success" | "warn" | "danger";

const map: Record<V, string> = {
  neutral: "bg-slate-100 text-slate-700",
  success: "bg-emerald-100 text-emerald-700",
  warn: "bg-amber-100 text-amber-700",
  danger: "bg-red-100 text-red-700"
};

export const Badge = ({ variant = "neutral", className, ...p }: { variant?: V } & React.HTMLAttributes<HTMLSpanElement>) =>
  <span className={cn("inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold", map[variant], className)} {...p} />;