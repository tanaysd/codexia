import React, { useState } from "react";
import { FileText, Search, Download, Play, AlertTriangle, Zap, Users, Clock, Target, TrendingUp, Settings } from "lucide-react";

export function WorkbenchPage(){
  const [smartRoutingEnabled, setSmartRoutingEnabled] = useState(true);
  
  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto space-y-8">
        <header>
          <h1 className="text-3xl font-semibold text-gray-900">Claim Workbench</h1>
          <p className="text-gray-600 mt-2">Assess, plan, and act on medical claims with AI-powered insights</p>
        </header>

      {/* Smart Routing Beta Banner */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-semibold text-gray-900">Smart Routing</h3>
                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full font-medium">BETA</span>
              </div>
              <p className="text-sm text-gray-600">AI automatically routes claims to the best specialist based on expertise and workload</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="text-sm font-medium text-gray-900">15% faster processing</div>
              <div className="text-xs text-gray-600">with smart routing enabled</div>
            </div>
            <button 
              onClick={() => setSmartRoutingEnabled(!smartRoutingEnabled)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                smartRoutingEnabled ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                smartRoutingEnabled ? 'translate-x-6' : 'translate-x-1'
              }`} />
            </button>
          </div>
        </div>
        
        {smartRoutingEnabled && (
          <div className="mt-4 grid grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4 border border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <Users className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-gray-900">Expertise Matching</span>
              </div>
              <div className="text-xs text-gray-600">Routes modifier issues to Sarah (95% accuracy)</div>
            </div>
            <div className="bg-white rounded-lg p-4 border border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-gray-900">Workload Balancing</span>
              </div>
              <div className="text-xs text-gray-600">Prevents overload, maintains quality</div>
            </div>
            <div className="bg-white rounded-lg p-4 border border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <Target className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-gray-900">Priority Handling</span>
              </div>
              <div className="text-xs text-gray-600">High-value claims get priority routing</div>
            </div>
          </div>
        )}
      </div>
      
      <div className="grid grid-cols-2 gap-8">
        <div className="bg-white rounded-xl border border-gray-200 h-fit">
          <div className="bg-gradient-to-r from-emerald-50 to-teal-50 rounded-t-xl p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-green-600" />
                <div className="font-semibold text-gray-900">Claim Editor</div>
              </div>
              <div className="flex gap-2">
                <button className="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50 flex items-center gap-1">
                  <FileText className="w-4 h-4" />
                  Format JSON
                </button>
                <button className="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50">Load Sample</button>
                <button className="px-3 py-1 bg-green-600 text-white rounded-md text-sm hover:bg-green-700 flex items-center gap-1">
                  <Search className="w-4 h-4" />
                  Assess Claim
                </button>
              </div>
            </div>
          </div>
          <div className="p-6">
            <textarea 
              className="w-full h-96 font-mono text-sm border border-gray-300 rounded-lg p-4 bg-slate-50 focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none" 
              defaultValue={`{
  "claimId": "CLM-1001",
  "patientId": "PAT-12345",
  "serviceDate": "2024-03-15",
  "procedures": [
    {
      "code": "99213",
      "description": "Office visit",
      "modifiers": []
    }
  ],
  "diagnosis": [
    {
      "code": "M79.3",
      "description": "Panniculitis"
    }
  ]
}`} 
            />
            <div className="flex items-center justify-between mt-4">
              <p className="text-xs text-gray-600 flex items-center gap-1">
                <Play className="w-3 h-3" />
                Press ⌘/Ctrl+Enter to assess
              </p>
              <div className="text-xs text-green-600">Valid JSON ✓</div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-gray-200">
            <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-t-xl p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-orange-600" />
                  <div className="font-semibold text-gray-900">Assessment Results</div>
                </div>
                <span className="bg-red-100 text-red-700 text-sm px-3 py-1 rounded-full font-medium flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3" />
                  High Risk 72%
                </span>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <div>
                  <div className="font-medium text-gray-900 mb-2">Key Issues Identified</div>
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <div className="font-medium text-red-800">Modifier 59 Missing</div>
                    <div className="text-sm text-red-600 mt-1">
                      Required modifier not found on line 1. This may result in claim denial.
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">
                    <strong>Evidence:</strong> UHC-LCD-123 §3b requires modifier 59 for this procedure combination.
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200">
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-t-xl p-6">
              <div className="font-semibold text-gray-900">Recommended Actions</div>
            </div>
            <div className="p-6 space-y-3">
              <div className="border border-gray-200 rounded-lg p-4 bg-white hover:bg-slate-50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">Add Modifier 59</div>
                    <div className="text-sm text-gray-600">Quick fix - add required modifier to procedure</div>
                  </div>
                  <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full font-medium">Recommended</span>
                </div>
              </div>
              <div className="border border-gray-200 rounded-lg p-4 bg-white hover:bg-slate-50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">Prepare Appeal Letter</div>
                    <div className="text-sm text-gray-600">Generate Level 1 appeal documentation</div>
                  </div>
                  <span className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-full font-medium">Alternative</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200">
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-t-xl p-6">
              <div className="flex items-center justify-between">
                <div className="font-semibold text-gray-900">Generated Artifact</div>
                <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full font-medium">Ready</span>
              </div>
            </div>
            <div className="p-6">
              <div className="bg-slate-100 rounded-lg p-4 mb-4">
                <pre className="text-xs overflow-x-auto font-mono">{`{
  "claimId": "CLM-1001",
  "correctedProcedures": [
    {
      "code": "99213",
      "description": "Office visit",
      "modifiers": ["59"]
    }
  ],
  "changeLog": [
    "Added modifier 59 to procedure 99213"
  ]
}`}</pre>
              </div>
              <button className="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center justify-center gap-2">
                <Download className="w-4 h-4" />
                Download Corrected Claim
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Smart Routing Dashboard */}
      {smartRoutingEnabled && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Live Routing Dashboard</h2>
            <div className="flex items-center gap-2 text-sm text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              Smart routing active
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Team Performance */}
            <div className="bg-white rounded-xl border border-gray-200">
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-t-xl p-6">
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                  <h3 className="font-semibold text-gray-900">Team Performance</h3>
                </div>
              </div>
              <div className="p-6 space-y-3">
                <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                  <div>
                    <div className="font-medium text-gray-900">Sarah Chen</div>
                    <div className="text-sm text-gray-600">Modifier Expert</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-green-700">23 claims</div>
                    <div className="text-xs text-gray-500">95% accuracy</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <div>
                    <div className="font-medium text-gray-900">Marcus Lee</div>
                    <div className="text-sm text-gray-600">Appeals Specialist</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-blue-700">18 claims</div>
                    <div className="text-xs text-gray-500">92% accuracy</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                  <div>
                    <div className="font-medium text-gray-900">Alex Kim</div>
                    <div className="text-sm text-gray-600">Complex Cases</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-purple-700">15 claims</div>
                    <div className="text-xs text-gray-500">97% accuracy</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Routing Actions */}
            <div className="bg-white rounded-xl border border-gray-200">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-t-xl p-6">
                <div className="flex items-center gap-2">
                  <Zap className="w-5 h-5 text-blue-600" />
                  <h3 className="font-semibold text-gray-900">Recent Routing</h3>
                </div>
              </div>
              <div className="p-6 space-y-3">
                <div className="border-l-4 border-green-500 pl-3">
                  <div className="text-sm font-medium text-gray-900">CLM-1087 → Sarah Chen</div>
                  <div className="text-xs text-gray-600">Modifier 59 issue • 2 min ago</div>
                  <div className="text-xs text-green-600">✓ 97% match confidence</div>
                </div>
                <div className="border-l-4 border-blue-500 pl-3">
                  <div className="text-sm font-medium text-gray-900">CLM-1092 → Marcus Lee</div>
                  <div className="text-xs text-gray-600">UHC appeal ready • 5 min ago</div>
                  <div className="text-xs text-blue-600">✓ 94% match confidence</div>
                </div>
                <div className="border-l-4 border-purple-500 pl-3">
                  <div className="text-sm font-medium text-gray-900">CLM-1095 → Alex Kim</div>
                  <div className="text-xs text-gray-600">Complex dx/cpt • 8 min ago</div>
                  <div className="text-xs text-purple-600">✓ 91% match confidence</div>
                </div>
                <div className="border-l-4 border-orange-500 pl-3">
                  <div className="text-sm font-medium text-gray-900">CLM-1098 → Sarah Chen</div>
                  <div className="text-xs text-gray-600">Bundling error • 12 min ago</div>
                  <div className="text-xs text-orange-600">✓ 89% match confidence</div>
                </div>
              </div>
            </div>

            {/* Routing Analytics */}
            <div className="bg-white rounded-xl border border-gray-200">
              <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-t-xl p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Target className="w-5 h-5 text-orange-600" />
                    <h3 className="font-semibold text-gray-900">Routing Impact</h3>
                  </div>
                  <Settings className="w-4 h-4 text-gray-400 cursor-pointer hover:text-gray-600" />
                </div>
              </div>
              <div className="p-6 space-y-4">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-700">15%</div>
                  <div className="text-sm text-gray-600">Faster Processing</div>
                  <div className="text-xs text-green-600">vs manual routing</div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <div className="font-bold text-blue-700">94.2%</div>
                    <div className="text-xs text-gray-600">Accuracy</div>
                  </div>
                  <div className="text-center p-3 bg-purple-50 rounded-lg">
                    <div className="font-bold text-purple-700">127</div>
                    <div className="text-xs text-gray-600">Routed Today</div>
                  </div>
                </div>
                <div className="p-3 bg-yellow-50 rounded-lg">
                  <div className="text-sm font-medium text-gray-900">Next Optimization</div>
                  <div className="text-xs text-gray-600">Batch similar payer types for 8% gain</div>
                </div>
              </div>
            </div>
          </div>

          {/* Routing Queue */}
          <div className="bg-white rounded-xl border border-gray-200">
            <div className="bg-gradient-to-r from-slate-50 to-gray-50 rounded-t-xl p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-gray-600" />
                  <h3 className="font-semibold text-gray-900">Smart Routing Queue</h3>
                </div>
                <span className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-full font-medium">47 claims pending</span>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                      <AlertTriangle className="w-4 h-4 text-red-600" />
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">CLM-1099 • High Priority</div>
                      <div className="text-sm text-gray-600">$47K claim • Modifier issue • UHC</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium text-blue-600">→ Sarah Chen</div>
                    <div className="text-xs text-gray-500">97% match • ETA 3min</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                      <Clock className="w-4 h-4 text-yellow-600" />
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">CLM-1100 • Appeal Ready</div>
                      <div className="text-sm text-gray-600">$23K claim • Complex case • Aetna</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium text-purple-600">→ Alex Kim</div>
                    <div className="text-xs text-gray-500">94% match • ETA 8min</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <FileText className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">CLM-1101 • Standard Review</div>
                      <div className="text-sm text-gray-600">$12K claim • Routine check • BCBS</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium text-blue-600">→ Marcus Lee</div>
                    <div className="text-xs text-gray-500">89% match • ETA 5min</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}