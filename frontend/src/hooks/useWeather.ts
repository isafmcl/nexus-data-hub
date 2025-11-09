import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

export const useWeather = (city: string) => {
  return useQuery({
    queryKey: ['weather', city],
    queryFn: async () => {
      if (!city) return null;
      const response = await api.get(`/weather?city=${city}`);
      return response.data;
    },
    enabled: !!city,
  });
};
