import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import WeatherForm from '../../frontend/src/components/WeatherForm';
import { QueryClient, QueryClientProvider } from 'react-query';

jest.mock('../../frontend/src/api', () => ({
  getCities: jest.fn((query) =>
    Promise.resolve(query ? ['Amsterdam', 'Athens'] : [])
  ),
  getWeather: jest.fn((city) =>
    Promise.resolve({
      city,
      temperature: 18,
      wind_speed: 4,
      timestamp: '2025-05-30T15:00:00Z'
    })
  )
}));

const queryClient = new QueryClient();

describe('WeatherForm Component', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('shows suggestions and displays weather card', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <WeatherForm />
      </QueryClientProvider>
    );

    const input = screen.getByPlaceholderText('Enter city');
    fireEvent.change(input, { target: { value: 'A' } });

    const suggestion = await screen.findByText('Amsterdam');
    expect(suggestion).toBeInTheDocument();

    fireEvent.click(suggestion);
    expect(input.value).toBe('Amsterdam');

    const button = screen.getByText('Search');
    fireEvent.click(button);

    await waitFor(() =>
      expect(screen.getByText(/Temperature:/)).toBeInTheDocument()
    );
    expect(screen.getByText(/18°C/)).toBeInTheDocument();
  });
});
