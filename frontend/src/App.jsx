import React from 'react';
import WeatherForm from './components/WeatherForm';
import StatsList from './components/StatsList';
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="max-w-xl mx-auto mt-10">
        <WeatherForm />
        <StatsList />
      </div>
    </QueryClientProvider>
  );
}