import { start } from './index';

test('start returns backend version', () => {
  expect(start()).toBe('Backend 1.0');
});
