import { useQuery } from '@tanstack/react-query'
import { api } from '@/services/api'

export function useCountries() {
  return useQuery({
    queryKey: ['countries'],
    queryFn: async () => {
      const res = await api.get('/countries/')
      return res
    },
    staleTime: 1000 * 60 * 60,
  })
}
