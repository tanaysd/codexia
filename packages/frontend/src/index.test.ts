import { render } from './index';

test('render returns frontend version', () => {
  expect(render()).toBe('Frontend 1.0');
});
