import { version } from '@codexia/contracts';

export function render(): string {
  return `Frontend ${version()}`;
}
