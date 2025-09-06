export function extractClaimFromDom(doc: Document = document): any | null {
  const script = doc.querySelector('script#codexia-claim[type="application/json"]') as HTMLScriptElement | null;
  if (script?.textContent) {
    try { return JSON.parse(script.textContent); } catch { /* fallthrough */ }
  }
  const pre = doc.querySelector('pre#codexia-claim');
  if (pre?.textContent) {
    try { return JSON.parse(pre.textContent); } catch { /* fallthrough */ }
  }
  return null;
}
