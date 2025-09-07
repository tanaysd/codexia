import { useToast } from '../lib/ui';
import React from 'react';
import { Button } from './ui/button';

const samples: Record<string, any> = {
  'mod-59': { lines: [{ modifiers: [] }] },
  'dx-incompat': { sample: true }
};

interface Props {
  text: string;
  setText: (t: string) => void;
  onAssess: () => void;
}

export default function ClaimEditor({ text, setText, onAssess }: Props) {
  const toast = useToast();

  function format() {
    try {
      setText(JSON.stringify(JSON.parse(text), null, 2));
    } catch {
      toast('Invalid JSON');
    }
  }

  function load(name: string) {
    setText(JSON.stringify(samples[name], null, 2));
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-slate-900">Claim Editor</h3>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={format}>
            Format JSON
          </Button>
          <Button variant="outline" size="sm" onClick={() => load('mod-59')}>
            Sample 1
          </Button>
          <Button variant="outline" size="sm" onClick={() => load('dx-incompat')}>
            Sample 2
          </Button>
        </div>
      </div>
      
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="flex-1 w-full p-4 border border-slate-200 rounded-md font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-slate-400 focus:border-transparent"
        placeholder="Enter claim JSON data here..."
      />
      
      <div className="mt-4 text-sm text-slate-500">
        Use ⌘/Ctrl+Enter to assess the claim
      </div>
    </div>
  );
}
