import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/services/api'

const BooksSearch: React.FC = () => {
  const [query, setQuery] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  const { data, isLoading, error } = useQuery({
    queryKey: ['books', searchQuery],
    queryFn: async () => {
      if (!searchQuery) return { success: true, total: 0, books: [] }
      return await api.get('/books/search', { params: { q: searchQuery, limit: 12 } })
    },
    enabled: !!searchQuery,
  })

  const handleSearch = () => {
    if (query.trim()) {
      setSearchQuery(query.trim())
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const raw = data && typeof data === 'object' && 'data' in data ? (data as any).data : data
  const books = raw?.books || []

  return (
    <div className="api-section">
      <div className="mb-8">
        <label className="block text-sm font-semibold text-slate-300 mb-4">
          Busque por título, autor ou ISBN
        </label>
        <div className="flex gap-4">
          <input
            className="input-modern flex-1"
            placeholder="Ex: Harry Potter, 1984, Stephen King..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button
            onClick={handleSearch}
            disabled={!query.trim() || isLoading}
            className="btn-modern-primary flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Buscando...
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Buscar
              </>
            )}
          </button>
        </div>
      </div>

      {isLoading && (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="spinner-modern mb-4"></div>
          <p className="text-slate-400 font-medium">Procurando livros...</p>
        </div>
      )}

      {error && (
        <div className="p-6 rounded-xl bg-red-500/10 border border-red-500/30 backdrop-blur-sm">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="font-bold text-red-400">Erro ao buscar livros</p>
            </div>
          </div>
        </div>
      )}

      {books.length > 0 && !isLoading && (
        <div>
          <p className="text-slate-400 text-sm mb-6">
            <span className="font-bold text-white text-lg">{books.length}</span> livros encontrados
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {books.map((book: any) => (
              <div
                key={book.key}
                className="book-card group"
              >
                <div className="flex gap-4">
                  {book.cover_url ? (
                    <div className="relative w-20 h-28 flex-shrink-0 rounded-lg overflow-hidden shadow-lg">
                      <img
                        src={book.cover_url}
                        alt={book.title}
                        className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent"></div>
                    </div>
                  ) : (
                    <div className="w-20 h-28 flex-shrink-0 rounded-lg bg-gradient-to-br from-purple-600/30 to-blue-600/30 flex items-center justify-center text-white font-bold text-xs border border-purple-500/30">
                      <svg className="w-10 h-10 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                    </div>
                  )}
                  
                  <div className="flex-1 min-w-0 flex flex-col">
                    <h4 className="font-bold text-slate-100 line-clamp-2 mb-2 group-hover:text-blue-400 transition-colors leading-snug">
                      {book.title}
                    </h4>
                    
                    {book.author_name && book.author_name.length > 0 && (
                      <p className="text-sm text-slate-400 line-clamp-1 mb-2 flex items-center gap-1.5">
                        <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        <span className="truncate">{book.author_name.slice(0, 2).join(', ')}</span>
                      </p>
                    )}
                    
                    {book.first_publish_year && (
                      <div className="mt-auto">
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs font-semibold">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          {book.first_publish_year}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {!searchQuery && !isLoading && (
        <div className="text-center py-20">
          <div className="mx-auto w-20 h-20 mb-6 rounded-2xl bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-blue-500/30 flex items-center justify-center">
            <svg className="w-10 h-10 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <p className="text-slate-400 text-lg font-medium mb-2">
            Busque por milhões de livros
          </p>
          <p className="text-slate-500 text-sm">
            Pesquise por título, autor ou ISBN na OpenLibrary
          </p>
        </div>
      )}

      {searchQuery && books.length === 0 && !isLoading && !error && (
        <div className="text-center py-20">
          <div className="mx-auto w-20 h-20 mb-6 rounded-2xl bg-gradient-to-br from-slate-600/20 to-slate-500/20 border border-slate-500/30 flex items-center justify-center">
            <svg className="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <p className="text-slate-400 text-lg font-medium mb-2">
            Nenhum livro encontrado
          </p>
          <p className="text-slate-500 text-sm">
            Tente pesquisar com outros termos para "{searchQuery}"
          </p>
        </div>
      )}
    </div>
  )
}

export default BooksSearch
