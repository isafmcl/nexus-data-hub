import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'

export function useWorldBank() {
  return useQuery({
    queryKey: ['worldbank', 'countries'],
    queryFn: async () => {
      const res = await api.get('/worldbank/countries?per_page=100')
      return res.data
    },
    staleTime: 1000 * 60 * 60, 
  })
}

export default useWorldBank
