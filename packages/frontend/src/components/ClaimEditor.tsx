import { useToast } from '../lib/ui';
import React from 'react';

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
    <div>
      <h3>Claim</h3>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={20}
        style={{ width: '100%' }}
      />
      <div className="flex flex-wrap gap-2 mt-2">
        <button onClick={format}>Format JSON</button>
        <button onClick={onAssess}>Assess (⌘/Ctrl+Enter)</button>
        <button onClick={() => load('mod-59')}>Load Sample: mod-59</button>
        <button onClick={() => load('dx-incompat')}>Load Sample: dx-incompat</button>
      </div>
    </div>
  );
}
