import { show } from './index';

test('show returns extension version', () => {
  expect(show()).toBe('Extension 1.0');
});
