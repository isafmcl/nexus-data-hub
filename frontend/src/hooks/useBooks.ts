import { useQuery } from '@tanstack/react-query'
import { api } from '@/services/api'

export function useBooks(query: string, limit = 10) {
  return useQuery({
    queryKey: ['books', query, limit],
    queryFn: async () => {
      if (!query) return { success: true, total: 0, books: [] }
      const res = await api.get('/books/search', { params: { q: query, limit } })
      return res
    },
    enabled: !!query,
  })
}
