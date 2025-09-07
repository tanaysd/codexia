import { useContext } from 'react';
import { WorkbenchContext } from '../routes/ClaimWorkbench';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

export default function ArtifactViewer() {
  const { artifact } = useContext(WorkbenchContext);
  
  if (!artifact) {
    return (
      <div className="h-full flex flex-col">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Artifact</h3>
        <div className="flex-1 flex items-center justify-center text-slate-500">
          No artifact generated yet. Execute a plan to generate artifacts.
        </div>
      </div>
    );
  }

  const downloadFile = (content: string, filename: string, type: string) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (artifact.artifactType === 'corrected_claim' && artifact.correctedClaim) {
    const text = JSON.stringify(artifact.correctedClaim, null, 2);
    
    return (
      <div className="h-full flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-900">Artifact</h3>
          <Badge variant="success">Corrected Claim</Badge>
        </div>
        
        <div className="flex-1 mb-4 overflow-hidden">
          <pre className="h-full overflow-auto p-4 bg-slate-50 border border-slate-200 rounded-md text-sm font-mono">
            {text}
          </pre>
        </div>
        
        <Button 
          onClick={() => downloadFile(text, 'corrected-claim.json', 'application/json')}
          className="w-full"
        >
          Download JSON
        </Button>
      </div>
    );
  }

  if (artifact.artifactType === 'appeal_letter' && artifact.appealLetter) {
    const text = artifact.appealLetter;
    
    return (
      <div className="h-full flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-900">Artifact</h3>
          <Badge variant="success">Appeal Letter</Badge>
        </div>
        
        <div className="flex-1 mb-4 overflow-hidden">
          <pre className="h-full overflow-auto p-4 bg-slate-50 border border-slate-200 rounded-md text-sm whitespace-pre-wrap">
            {text}
          </pre>
        </div>
        
        <Button 
          onClick={() => downloadFile(text, 'appeal.md', 'text/markdown')}
          className="w-full"
        >
          Download Markdown
        </Button>
      </div>
    );
  }
  
  return null;
}
