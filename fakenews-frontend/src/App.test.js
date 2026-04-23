import { render, screen } from '@testing-library/react';
import App from './App';

test('renders analyze news heading', () => {
  render(<App />);
  const heading = screen.getByText(/analyze news article/i);
  expect(heading).toBeInTheDocument();
});
