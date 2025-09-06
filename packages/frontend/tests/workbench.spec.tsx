import { render, screen, fireEvent } from '@testing-library/react';
import ClaimWorkbench from '../src/routes/ClaimWorkbench';
import { vi } from 'vitest';

vi.mock('../src/lib/api', () => ({
  postAssess: vi.fn(async () => ({
    risk: 0.7,
    drivers: [{ issue: 'mismatch', contribution: 0.5 }],
    evidence: [{ source: 's', clauseId: 'c1', snippet: 'evidence' }]
  })),
  postPlan: vi.fn(async () => ({
    plans: [
      { type: 'Recoding', rationale: 'Add 59', actions: [{ addModifier: '59' }] },
      { type: 'Appeal', rationale: 'Appeal', actions: [] }
    ]
  })),
  postAct: vi.fn(async () => ({
    artifactType: 'corrected_claim',
    correctedClaim: { lines: [{ modifiers: ['-59'] }] }
  }))
}));

const mockClaim = { lines: [{ modifiers: [] }] };

test('workbench flow', async () => {
  render(<ClaimWorkbench />);
  const textarea = screen.getByRole('textbox');
  fireEvent.change(textarea, { target: { value: JSON.stringify(mockClaim) } });

  fireEvent.click(screen.getByText(/Assess/));
  await screen.findByText(/Risk/);
  expect(screen.getByText('mismatch')).toBeInTheDocument();

  fireEvent.click(screen.getByText('Plan'));
  await screen.findByText('Recoding');
  await screen.findByText('Appeal');

  fireEvent.click(screen.getByText(/Act/));
  await screen.findByText((content) => content.includes('-59'));
});
