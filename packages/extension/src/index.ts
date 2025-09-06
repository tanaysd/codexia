import { version } from '@codexia/contracts';

export function show(): string {
  return `Extension ${version()}`;
}
