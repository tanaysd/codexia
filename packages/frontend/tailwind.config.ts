import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./index.html","./src/**/*.{ts,tsx}"],
  theme: {
    container: { center: true, padding: "1.25rem", screens: { "2xl": "1320px" } },
    extend: {
      colors: {
        bg:      "#F6F8FB",         // page background
        card:    "#FFFFFF",
        border:  "#E5E7EB",
        ink:     "#0F172A",         // headings
        subink:  "#475569",         // secondary text
        brand:   "#3B82F6",         // primary
        brand2:  "#2563EB",         // darker
        success: "#10B981",
        warn:    "#F59E0B",
        danger:  "#EF4444"
      },
      boxShadow: {
        card: "0 6px 18px rgba(15, 23, 42, 0.06)",
        soft: "0 1px 2px rgba(0,0,0,0.04), 0 2px 8px rgba(0,0,0,0.06)"
      },
      borderRadius: { xl: "1rem", lg: "0.75rem", md: "0.5rem" }
    }
  },
  plugins: []
} satisfies Config;