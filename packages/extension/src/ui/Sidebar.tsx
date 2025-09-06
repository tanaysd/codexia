import React, { useState } from 'react';
import { extractClaimFromDom } from '../lib/extract';
import { postAssess, postPlan, postAct } from '../lib/api';
import { AssessmentResult, PlanResult, ActResult } from '../lib/types';
import './styles.css';

export const Sidebar: React.FC = () => {
  const [claim, setClaim] = useState<any | null>(() => extractClaimFromDom());
  const [pasted, setPasted] = useState('');
  const [assessment, setAssessment] = useState<AssessmentResult | null>(null);
  const [plan, setPlan] = useState<PlanResult | null>(null);
  const [act, setAct] = useState<ActResult | null>(null);

  const usePasted = () => {
    try { setClaim(JSON.parse(pasted)); } catch { alert('Invalid JSON'); }
  };

  const handleAssess = async () => {
    if (!claim) return;
    const res = await postAssess(claim);
    setAssessment(res);
  };

  const handlePlan = async () => {
    if (!claim || !assessment) return;
    const res = await postPlan(claim, assessment);
    setPlan(res);
  };

  const handleAct = async () => {
    if (!claim || !plan) return;
    const res = await postAct(claim, plan.plans[0], assessment);
    setAct(res);
  };

  return (
    <div className="codexia-sidebar">
      <div className="codexia-card">
        <h3>Claim</h3>
        {claim ? <div>Extracted ✓</div> : (
          <>
            <textarea value={pasted} onChange={e => setPasted(e.target.value)} />
            <button onClick={usePasted}>Use Pasted</button>
          </>
        )}
      </div>

      <div className="codexia-card">
        <h3>Assessment</h3>
        {!assessment && <button disabled={!claim} onClick={handleAssess}>Assess</button>}
        {assessment && (
          <>
            <div>Risk: {assessment.risk.toFixed(2)}</div>
            <div className="bar"><div className="bar-fill" style={{ width: `${assessment.risk * 100}%` }}></div></div>
            <div>
              {assessment.drivers.map((d, i) => (
                <span key={i} className="badge">{d.label}</span>
              ))}
            </div>
            <ul>
              {assessment.evidence.map((e, i) => (
                <li key={i}>{e.source} · {e.clause_id}</li>
              ))}
            </ul>
          </>
        )}
      </div>

      <div className="codexia-card">
        <h3>Plan / Act</h3>
        {!plan && <button disabled={!assessment} onClick={handlePlan}>Plan</button>}
        {plan && !act && (
          <>
            <ul>
              {plan.plans.map((p, i) => (
                <li key={i}>{p.type}</li>
              ))}
            </ul>
            <button onClick={handleAct}>Apply Fix</button>
          </>
        )}
        {act && (
          <>
            {act.artifactType === 'corrected_claim' && (
              <>
                <pre>{JSON.stringify(act.payload, null, 2)}</pre>
                <a href={URL.createObjectURL(new Blob([JSON.stringify(act.payload, null, 2)], { type: 'application/json' }))} download="claim.json">Download JSON</a>
              </>
            )}
            {act.artifactType === 'appeal_markdown' && (
              <>
                <pre>{String(act.payload)}</pre>
                <a href={URL.createObjectURL(new Blob([String(act.payload)], { type: 'text/markdown' }))} download="appeal.md">Download .md</a>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
