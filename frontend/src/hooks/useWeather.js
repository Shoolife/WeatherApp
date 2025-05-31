import { useQuery } from '@tanstack/react-query';
import { getWeather } from '../api';

export const useWeather = (city) => {
  return useQuery({
    queryKey: ['weather', city],
    queryFn: () => getWeather(city),
    enabled: !!city,
    retry: (failureCount, error) => {
      if (error?.response?.status === 404) return false;
      return failureCount < 2;
    },
    retryDelay: 1000,
    staleTime: 5 * 60 * 1000,
    onError: (error) => {
      console.warn('Ошибка при получении погоды:', error?.message);
    },
  });
};
