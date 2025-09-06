import { useContext, useEffect, useState } from 'react';
import { WorkbenchContext } from '../routes/ClaimWorkbench';
import { PlanOption } from '../lib/types';

interface Props {
  onAct: (plan: PlanOption) => void;
}

export default function PlanChooser({ onAct }: Props) {
  const { plan } = useContext(WorkbenchContext);
  const [selected, setSelected] = useState<PlanOption | null>(null);

  useEffect(() => {
    if (plan && plan.plans.length > 0) {
      setSelected(plan.plans[0]);
    }
  }, [plan]);

  if (!plan) return null;

  return (
    <div>
      <h3>Plan</h3>
      {plan.plans.map((p) => (
        <label key={p.type} style={{ display: 'block', border: '1px solid #ddd', padding: '8px', marginBottom: '4px' }}>
          <input type="radio" name="plan" checked={selected?.type === p.type} onChange={() => setSelected(p)} />{' '}
          <strong>{p.type}</strong> - {p.rationale}
          <div>
            {p.actions.map((a, i) => (
              <span key={i}>
                {a.addModifier ? `addModifier:${a.addModifier}` : ''}
                {a.replaceDx ? ` replaceDx:${a.replaceDx}` : ''}
              </span>
            ))}
          </div>
          {p.citation && <small>{p.citation}</small>}
        </label>
      ))}
      <button onClick={() => selected && onAct(selected)}>Act (⌘/Ctrl+Shift+Enter)</button>
    </div>
  );
}
