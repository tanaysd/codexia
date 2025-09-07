import React from "react";

export function BriefPage(){
  const claims = [
    { id: "CLM-1001", reason: "Modifier 59 missing", risk: 0.72, eta: 4 },
    { id: "CLM-1002", reason: "Dx/CPT mismatch", risk: 0.45, eta: 6 },
    { id: "CLM-1003", reason: "Coverage expired", risk: 0.83, eta: 5 },
  ];
  
  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-4xl">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Morning Brief</h1>
            <p className="text-gray-600 mt-1">Prioritized by impact and urgency</p>
          </div>
          <div className="flex gap-3">
            <button className="px-4 py-2 border border-gray-300 rounded-md bg-white text-gray-700 hover:bg-gray-50">
              Load Sample
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              New
            </button>
          </div>
        </div>

        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Today's Queue</h2>
              <p className="text-sm text-gray-600">{claims.length} items</p>
            </div>
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
              100% Ready
            </span>
          </div>

          <div className="space-y-4">
            {claims.map(c=>(
              <div key={c.id} className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-gray-900 text-lg mb-1">{c.id}</div>
                    <div className="text-gray-600">{c.reason} · ETA {c.eta}m</div>
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
    </div>
  );
}