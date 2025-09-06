import { version } from './index';

test('version is 1.0', () => {
  expect(version()).toBe('1.0');
});
