import React, { createContext, useEffect, useMemo, useState } from 'react';
import ClaimEditor from '../components/ClaimEditor';
import AssessmentView from '../components/AssessmentView';
import PlanChooser from '../components/PlanChooser';
import ArtifactViewer from '../components/ArtifactViewer';
import { postAssess, postPlan, postAct } from '../lib/api';
import { save, list } from '../lib/storage';
import { AssessmentResult, PlanResult, ActResult, PlanOption } from '../lib/types';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';

interface Ctx {
  assessment: AssessmentResult | null;
  plan: PlanResult | null;
  artifact: ActResult | null;
  setAssessment: (a: AssessmentResult | null) => void;
  setPlan: (p: PlanResult | null) => void;
  setArtifact: (a: ActResult | null) => void;
}

export const WorkbenchContext = createContext<Ctx>({
  assessment: null,
  plan: null,
  artifact: null,
  setAssessment: () => {},
  setPlan: () => {},
  setArtifact: () => {}
});

export default function ClaimWorkbench() {
  const [claimText, setClaimText] = useState('{}');
  const [assessment, setAssessment] = useState<AssessmentResult | null>(null);
  const [plan, setPlan] = useState<PlanResult | null>(null);
  const [artifact, setArtifact] = useState<ActResult | null>(null);
  const [showRecent, setShowRecent] = useState(false);

  const claim = useMemo(() => {
    try {
      return JSON.parse(claimText);
    } catch {
      return null;
    }
  }, [claimText]);

  async function handleAssess() {
    if (!claim) return;
    const res = await postAssess(claim);
    setAssessment(res);
    save(claim);
    setPlan(null);
    setArtifact(null);
  }

  async function handlePlan() {
    if (!claim || !assessment) return;
    const res = await postPlan(claim, assessment);
    setPlan(res);
    setArtifact(null);
  }

  async function handleAct(p: PlanOption) {
    if (!claim) return;
    const res = await postAct(claim, p, assessment);
    setArtifact(res);
  }

  useEffect(() => {
    function key(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleAssess();
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter' && e.shiftKey) {
        e.preventDefault();
        if (plan && plan.plans[0]) handleAct(plan.plans[0]);
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setShowRecent(true);
      }
    }
    window.addEventListener('keydown', key);
    return () => window.removeEventListener('keydown', key);
  }, [assessment, plan, claim]);

  return (
    <WorkbenchContext.Provider value={{ assessment, plan, artifact, setAssessment, setPlan, setArtifact }}>
      <div className="flex-1 flex flex-col bg-slate-50">
        <div className="border-b border-slate-200 bg-white px-6 py-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-900">Claim Workbench</h2>
          <Button onClick={handleAssess} disabled={!claim}>
            Assess Claim
          </Button>
        </div>
        
        <div className="flex-1 p-6">
          <div className="grid grid-cols-2 gap-6 h-full">
            <Card className="h-full">
              <CardContent className="h-full">
                <ClaimEditor text={claimText} setText={setClaimText} onAssess={handleAssess} />
              </CardContent>
            </Card>
            
            <div className="flex flex-col gap-6 h-full">
              <Card>
                <CardContent>
                  <AssessmentView onPlan={handlePlan} />
                </CardContent>
              </Card>
              
              <Card>
                <CardContent>
                  <PlanChooser onAct={handleAct} />
                </CardContent>
              </Card>
              
              <Card className="flex-1">
                <CardContent className="h-full">
                  <ArtifactViewer />
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
        
        {showRecent && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowRecent(false)}>
            <Card className="max-w-md w-full m-4">
              <CardContent>
                <h3 className="text-lg font-semibold mb-4">Recent Claims</h3>
                <div className="space-y-2">
                  {list().map((c, i) => (
                    <button
                      key={i}
                      onClick={() => {
                        setClaimText(JSON.stringify(c, null, 2));
                        setShowRecent(false);
                      }}
                      className="block w-full text-left p-3 rounded-md border border-slate-200 hover:bg-slate-50 transition-colors"
                    >
                      <div className="font-medium truncate">
                        {JSON.stringify(c).slice(0, 60)}...
                      </div>
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </WorkbenchContext.Provider>
  );
}
