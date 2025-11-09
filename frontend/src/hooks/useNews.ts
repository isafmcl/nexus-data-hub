import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

export const useNews = (category: string = 'general') => {
  return useQuery({
    queryKey: ['news', category],
    queryFn: async () => {
      const response = await api.get(`/news?category=${category}`);
      return response.data;
    },
  });
};
