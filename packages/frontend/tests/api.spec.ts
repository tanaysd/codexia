import { describe, it, expect, beforeEach, vi } from 'vitest';
import { postAssess, postPlan, postAct, getBrief } from '../src/lib/api';

function mock(body: any) {
  return Promise.resolve({
    ok: true,
    status: 200,
    statusText: 'OK',
    json: async () => body
  } as Response);
}

describe('api', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it('postAssess', async () => {
    (fetch as any).mockImplementation(() => mock({ risk: 0.1 }));
    const res = await postAssess({ a: 1 });
    expect(res).toEqual({ risk: 0.1 });
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/v1/assess',
      expect.objectContaining({ method: 'POST', headers: { 'content-type': 'application/json' } })
    );
  });

  it('postPlan', async () => {
    (fetch as any).mockImplementation(() => mock({ plans: [] }));
    const res = await postPlan({}, {});
    expect(res).toEqual({ plans: [] });
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/v1/plan',
      expect.objectContaining({ method: 'POST' })
    );
  });

  it('postAct', async () => {
    (fetch as any).mockImplementation(() => mock({ artifactType: 'corrected_claim' }));
    const res = await postAct({}, {});
    expect(res).toEqual({ artifactType: 'corrected_claim' });
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/v1/act',
      expect.objectContaining({ method: 'POST' })
    );
  });

  it('getBrief', async () => {
    (fetch as any).mockImplementation(() => mock({ highlights: [], queue: [] }));
    const res = await getBrief('u', '2020-01-01');
    expect(res).toEqual({ highlights: [], queue: [] });
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/v1/brief?user_id=u&date=2020-01-01');
  });
});
