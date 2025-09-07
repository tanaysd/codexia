import { useContext } from 'react';
import { WorkbenchContext } from '../routes/ClaimWorkbench';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

interface Props {
  onPlan: () => void;
}

export default function AssessmentView({ onPlan }: Props) {
  const { assessment } = useContext(WorkbenchContext);
  
  if (!assessment) {
    return (
      <div className="h-full flex flex-col">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Assessment</h3>
        <div className="flex-1 flex items-center justify-center text-slate-500">
          No assessment available. Please assess a claim first.
        </div>
      </div>
    );
  }

  const riskPercentage = Math.round(assessment.risk * 100);
  const getRiskVariant = (risk: number) => {
    if (risk >= 70) return 'destructive';
    if (risk >= 40) return 'warning';
    return 'success';
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-slate-900">Assessment</h3>
        <Badge variant={getRiskVariant(riskPercentage)}>
          Risk: {riskPercentage}%
        </Badge>
      </div>
      
      <div className="flex-1">
        <div className="mb-4">
          <h4 className="font-medium text-slate-700 mb-2">Key Issues</h4>
          <ul className="space-y-2">
            {assessment.drivers.slice(0, 3).map((d, i) => (
              <li key={i} className="text-sm text-slate-600 flex items-start">
                <span className="inline-block w-1.5 h-1.5 bg-slate-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                {d.issue}
              </li>
            ))}
          </ul>
        </div>

        <details className="mb-4">
          <summary className="font-medium text-slate-700 cursor-pointer hover:text-slate-900">
            Evidence ({assessment.evidence.length} items)
          </summary>
          <div className="mt-2 space-y-2 pl-4">
            {assessment.evidence.map((e, i) => (
              <div key={i} className="text-sm border-l-2 border-slate-200 pl-3">
                <div className="font-medium text-slate-600">
                  {e.source}:{e.clauseId}
                </div>
                <div className="text-slate-500">
                  {e.snippet}
                </div>
              </div>
            ))}
          </div>
        </details>
      </div>

      <Button onClick={onPlan} className="w-full">
        Create Plan
      </Button>
    </div>
  );
}
