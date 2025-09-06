import { useContext } from 'react';
import { WorkbenchContext } from '../routes/ClaimWorkbench';

interface Props {
  onPlan: () => void;
}

export default function AssessmentView({ onPlan }: Props) {
  const { assessment } = useContext(WorkbenchContext);
  if (!assessment) return null;
  return (
    <div>
      <h3>Assessment</h3>
      <div>Risk: {Math.round(assessment.risk * 100)}%</div>
      <ul>
        {assessment.drivers.slice(0, 3).map((d, i) => (
          <li key={i}>{d.issue}</li>
        ))}
      </ul>
      <details>
        <summary>Evidence</summary>
        <ul>
          {assessment.evidence.map((e, i) => (
            <li key={i}>
              {e.source}:{e.clauseId} {e.snippet}
            </li>
          ))}
        </ul>
      </details>
      <button onClick={onPlan}>Plan</button>
    </div>
  );
}
