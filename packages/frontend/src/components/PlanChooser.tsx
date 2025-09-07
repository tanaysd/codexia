import { useContext, useEffect, useState } from 'react';
import { WorkbenchContext } from '../routes/ClaimWorkbench';
import { PlanOption } from '../lib/types';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

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

  if (!plan) {
    return (
      <div className="h-full flex flex-col">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Plan</h3>
        <div className="flex-1 flex items-center justify-center text-slate-500">
          No plan available. Please create an assessment first.
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-slate-900">Plan</h3>
        <Badge variant="outline">{plan.plans.length} options</Badge>
      </div>
      
      <div className="flex-1 space-y-3 mb-4">
        {plan.plans.map((p) => (
          <label
            key={p.type}
            className={`block p-4 border rounded-lg cursor-pointer transition-colors ${
              selected?.type === p.type
                ? 'border-slate-400 bg-slate-50'
                : 'border-slate-200 hover:border-slate-300'
            }`}
          >
            <div className="flex items-start">
              <input
                type="radio"
                name="plan"
                checked={selected?.type === p.type}
                onChange={() => setSelected(p)}
                className="mt-1 mr-3"
              />
              <div className="flex-1">
                <div className="font-medium text-slate-900 mb-1">{p.type}</div>
                <div className="text-sm text-slate-600 mb-2">{p.rationale}</div>
                
                {p.actions.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-2">
                    {p.actions.map((a, i) => (
                      <Badge key={i} variant="outline" className="text-xs">
                        {a.addModifier && `Add: ${a.addModifier}`}
                        {a.replaceDx && `Replace: ${a.replaceDx}`}
                      </Badge>
                    ))}
                  </div>
                )}
                
                {p.citation && (
                  <div className="text-xs text-slate-500 italic">{p.citation}</div>
                )}
              </div>
            </div>
          </label>
        ))}
      </div>

      <Button 
        onClick={() => selected && onAct(selected)} 
        disabled={!selected}
        className="w-full"
      >
        Execute Plan (⌘/Ctrl+Shift+Enter)
      </Button>
    </div>
  );
}
