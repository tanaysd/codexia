import { describe, it, expect } from 'vitest';
import { extractClaimFromDom } from '../src/lib/extract';

describe('extractClaimFromDom', () => {
  it('returns claim from script tag', () => {
    const html = '<script id="codexia-claim" type="application/json">{"claimId":"CLM-1"}</script>';
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const claim = extractClaimFromDom(doc);
    expect(claim?.claimId).toBe('CLM-1');
  });

  it('returns null on invalid JSON', () => {
    const html = '<script id="codexia-claim" type="application/json">{bad json}</script>';
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const claim = extractClaimFromDom(doc);
    expect(claim).toBeNull();
  });
});
