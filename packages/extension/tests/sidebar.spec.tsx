import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Sidebar from '../src/ui/Sidebar';

const assessRes = { risk: 0.72, drivers: [{ label: 'upcoding' }], evidence: [{ source: 'policy', clause_id: '123' }] };
const planRes = { plans: [ { type: 'recoding', actions: [{ line: 0, addModifier: '59' }], rationale: '...' }, { type: 'appeal', actions: [] } ] };
const actRes = { artifactType: 'corrected_claim', payload: { lines: [ { modifiers: ['59'] } ] } };

beforeEach(() => {
  document.body.innerHTML = '<script id="codexia-claim" type="application/json">{"id":"X"}</script>';
  vi.spyOn(globalThis, 'fetch').mockImplementation((input: RequestInfo) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/v1/assess')) return Promise.resolve(new Response(JSON.stringify(assessRes)));
    if (url.endsWith('/v1/plan')) return Promise.resolve(new Response(JSON.stringify(planRes)));
    if (url.endsWith('/v1/act')) return Promise.resolve(new Response(JSON.stringify(actRes)));
    return Promise.reject(new Error('unknown url'));
  });
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('Sidebar', () => {
  it('assess plan act flow', async () => {
    const user = userEvent.setup();
    render(<Sidebar />);

    await user.click(screen.getByText('Assess'));
    await screen.findByText(/Risk/);
    expect(screen.getByText('upcoding')).toBeInTheDocument();

    await user.click(screen.getByText('Plan'));
    await user.click(screen.getByText('Apply Fix'));
    await screen.findByText(/"59"/);
  });
});
