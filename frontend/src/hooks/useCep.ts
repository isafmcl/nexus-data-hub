import { useQuery } from '@tanstack/react-query'
import { get } from '../services/api'

export function useCep(cep?: string) {
  return useQuery({
    queryKey: ['cep', cep],
    queryFn: async () => {
      const res = await get(`/cep/${cep}`)
      return res
    },
    enabled: !!cep,
    staleTime: 1000 * 60 * 60, 
  })
}

export default useCep
