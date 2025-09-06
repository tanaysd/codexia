const BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

async function j<T>(r: Response): Promise<T> {
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return (await r.json()) as T;
}

export async function postAssess(claim: any) {
  return j(fetch(`${BASE}/v1/assess`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(claim)
  }));
}

export async function postPlan(claim: any, assessment: any) {
  return j(fetch(`${BASE}/v1/plan`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ claim, assessment })
  }));
}

export async function postAct(claim: any, plan: any, assessment?: any) {
  return j(fetch(`${BASE}/v1/act`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ claim, plan, assessment })
  }));
}

export async function getBrief(userId: string, date: string) {
  const u = new URL(`${BASE}/v1/brief`);
  u.searchParams.set('user_id', userId);
  u.searchParams.set('date', date);
  return j(fetch(u.toString()));
}
