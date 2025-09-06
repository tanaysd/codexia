import { version } from '@codexia/contracts';

export function start(): string {
  return `Backend ${version()}`;
}
