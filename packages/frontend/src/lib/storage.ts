const KEY = 'recentClaims';

export function list(): any[] {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '[]');
  } catch {
    return [];
  }
}

export function save(claim: any) {
  const arr = list();
  const str = JSON.stringify(claim);
  const filtered = arr.filter((c) => JSON.stringify(c) !== str);
  filtered.unshift(claim);
  localStorage.setItem(KEY, JSON.stringify(filtered.slice(0, 5)));
}

export function get(i: number) {
  return list()[i];
}
