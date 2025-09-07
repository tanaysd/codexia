import React from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Search, Download, Play, AlertTriangle } from "lucide-react";

export function WorkbenchPage(){
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold text-ink">Claim Workbench</h1>
        <p className="text-subink mt-2">Assess, plan, and act on medical claims with AI-powered insights</p>
      </header>
      
      <div className="grid grid-cols-2 gap-8 max-w-7xl">
        <Card className="h-fit">
          <CardHeader className="bg-gradient-to-r from-emerald-50 to-teal-50 rounded-t-xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-brand" />
                <div className="font-semibold text-ink">Claim Editor</div>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">
                  <FileText className="w-4 h-4 mr-1" />
                  Format JSON
                </Button>
                <Button variant="outline" size="sm">Load Sample</Button>
                <Button size="sm" className="bg-brand hover:bg-brand2">
                  <Search className="w-4 h-4 mr-1" />
                  Assess Claim
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <textarea 
              className="w-full h-96 font-mono text-sm border border-border rounded-lg p-4 bg-slate-50 focus:ring-2 focus:ring-brand focus:border-transparent resize-none" 
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
              <p className="text-xs text-subink flex items-center gap-1">
                <Play className="w-3 h-3" />
                Press ⌘/Ctrl+Enter to assess
              </p>
              <div className="text-xs text-success">Valid JSON ✓</div>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader className="bg-gradient-to-r from-orange-50 to-red-50 rounded-t-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-warn" />
                  <div className="font-semibold text-ink">Assessment Results</div>
                </div>
                <Badge variant="danger" className="text-sm px-3 py-1">
                  <AlertTriangle className="w-3 h-3 mr-1" />
                  High Risk 72%
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="font-medium text-ink mb-2">Key Issues Identified</div>
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <div className="font-medium text-red-800">Modifier 59 Missing</div>
                    <div className="text-sm text-red-600 mt-1">
                      Required modifier not found on line 1. This may result in claim denial.
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-sm text-subink">
                    <strong>Evidence:</strong> UHC-LCD-123 §3b requires modifier 59 for this procedure combination.
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-t-xl">
              <div className="font-semibold text-ink">Recommended Actions</div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="border border-border rounded-lg p-4 bg-white hover:bg-slate-50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-ink">Add Modifier 59</div>
                    <div className="text-sm text-subink">Quick fix - add required modifier to procedure</div>
                  </div>
                  <Badge variant="success" className="text-xs">Recommended</Badge>
                </div>
              </div>
              <div className="border border-border rounded-lg p-4 bg-white hover:bg-slate-50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-ink">Prepare Appeal Letter</div>
                    <div className="text-sm text-subink">Generate Level 1 appeal documentation</div>
                  </div>
                  <Badge variant="neutral" className="text-xs">Alternative</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-t-xl">
              <div className="flex items-center justify-between">
                <div className="font-semibold text-ink">Generated Artifact</div>
                <Badge variant="success" className="text-xs">Ready</Badge>
              </div>
            </CardHeader>
            <CardContent>
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
              <Button size="sm" className="w-full bg-success hover:bg-green-600">
                <Download className="w-4 h-4 mr-1" />
                Download Corrected Claim
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}