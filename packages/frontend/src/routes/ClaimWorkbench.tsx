import React, { createContext, useEffect, useMemo, useState } from 'react';
import ClaimEditor from '../components/ClaimEditor';
import AssessmentView from '../components/AssessmentView';
import PlanChooser from '../components/PlanChooser';
import ArtifactViewer from '../components/ArtifactViewer';
import { postAssess, postPlan, postAct } from '../lib/api';
import { save, list } from '../lib/storage';
import { AssessmentResult, PlanResult, ActResult, PlanOption } from '../lib/types';

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
      <div className="p-4">
        {showRecent && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center" onClick={() => setShowRecent(false)}>
            <div className="bg-white p-4">
              {list().map((c, i) => (
                <button
                  key={i}
                  onClick={() => {
                    setClaimText(JSON.stringify(c, null, 2));
                    setShowRecent(false);
                  }}
                  className="block w-full text-left"
                >
                  {JSON.stringify(c).slice(0, 60)}...
                </button>
              ))}
            </div>
          </div>
        )}
        <div className="grid md:grid-cols-2 gap-4">
          <ClaimEditor text={claimText} setText={setClaimText} onAssess={handleAssess} />
          <div className="flex flex-col gap-4">
            <AssessmentView onPlan={handlePlan} />
            <PlanChooser onAct={handleAct} />
            <ArtifactViewer />
          </div>
        </div>
      </div>
    </WorkbenchContext.Provider>
  );
}
