import { useContext } from 'react';
import { WorkbenchContext } from '../routes/ClaimWorkbench';

export default function ArtifactViewer() {
  const { artifact } = useContext(WorkbenchContext);
  if (!artifact) return null;

  if (artifact.artifactType === 'corrected_claim' && artifact.correctedClaim) {
    const text = JSON.stringify(artifact.correctedClaim, null, 2);
    function download() {
      const blob = new Blob([text], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'corrected-claim.json';
      a.click();
      URL.revokeObjectURL(url);
    }
    return (
      <div>
        <h3>Artifact</h3>
        <pre>{text}</pre>
        <button onClick={download}>Download JSON</button>
      </div>
    );
  }

  if (artifact.artifactType === 'appeal_letter' && artifact.appealLetter) {
    const text = artifact.appealLetter;
    function download() {
      const blob = new Blob([text], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'appeal.md';
      a.click();
      URL.revokeObjectURL(url);
    }
    return (
      <div>
        <h3>Artifact</h3>
        <pre>{text}</pre>
        <button onClick={download}>Download .md</button>
      </div>
    );
  }
  return null;
}
