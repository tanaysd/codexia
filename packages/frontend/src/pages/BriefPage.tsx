import React from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function BriefPage(){
  const claims = [
    { id: "CLM-1001", reason: "Modifier 59 missing", risk: 0.72, eta: 4 },
    { id: "CLM-1002", reason: "Dx/CPT mismatch", risk: 0.45, eta: 6 },
    { id: "CLM-1003", reason: "Coverage expired", risk: 0.83, eta: 5 },
  ];
  
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Morning Brief</h1>
          <p className="text-slate-600 mt-1">Prioritized by impact and urgency</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">Load Sample</Button>
          <Button>New</Button>
        </div>
      </div>

      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Today's Queue</h2>
            <p className="text-sm text-slate-600">{claims.length} items</p>
          </div>
          <Badge variant="success" className="px-3 py-1">
            100% Ready
          </Badge>
        </div>

        <div className="space-y-4">
          {claims.map(c=>(
            <div key={c.id} className="bg-white rounded-lg border border-slate-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-semibold text-slate-900 text-lg mb-1">{c.id}</div>
                  <div className="text-slate-600">{c.reason} · ETA {c.eta}m</div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    c.risk > 0.7 ? 'bg-red-100 text-red-700' :
                    c.risk > 0.5 ? 'bg-yellow-100 text-yellow-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {Math.round(c.risk*100)}% Risk
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}