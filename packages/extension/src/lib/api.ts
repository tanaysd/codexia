const BASE = (globalThis as any).VITE_API_BASE || "http://localhost:8000";
async function j<T>(r: Response): Promise<T> { if (!r.ok) throw new Error(`${r.status} ${r.statusText}`); return r.json() as Promise<T>; }
export async function postAssess(claim: any){ return j(fetch(`${BASE}/v1/assess`, {method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(claim)})); }
export async function postPlan(claim: any, assessment: any){ return j(fetch(`${BASE}/v1/plan`, {method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({claim,assessment})})); }
export async function postAct(claim: any, plan: any, assessment?: any){ return j(fetch(`${BASE}/v1/act`, {method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({claim,plan,assessment})})); }
