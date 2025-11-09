import React, { useState } from 'react'
import { useWorldBank } from '@/hooks/useWorldBank'

const WorldBankCard: React.FC = () => {
  const { data, isLoading, error } = useWorldBank()
  const [searchTerm, setSearchTerm] = useState('')
  const [showAll, setShowAll] = useState(false)

  const wbData = (data && typeof data === 'object' && 'data' in data) ? data.data : data
  const allCountries = wbData?.countries || []


  const filteredCountries = allCountries.filter((country: any) => 
    country.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    country.region?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    country.income_level?.toLowerCase().includes(searchTerm.toLowerCase())
  )


  const INITIAL_DISPLAY = 6
  const displayedCountries = showAll ? filteredCountries : filteredCountries.slice(0, INITIAL_DISPLAY)
  const hasMore = filteredCountries.length > INITIAL_DISPLAY


  const regions = Array.from(new Set(allCountries.map((c: any) => c.region).filter(Boolean))) as string[]


  if (isLoading) {
    return (
      <div className="api-section">
        <div className="flex flex-col items-center justify-center py-20">
          <div className="spinner-modern mb-4"></div>
          <p className="text-slate-400 font-medium">Carregando dados econômicos...</p>
        </div>
      </div>
    )
  }


  if (error) {
    return (
      <div className="api-section">
        <div className="p-6 rounded-xl bg-red-500/10 border border-red-500/30 backdrop-blur-sm">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="font-bold text-red-400 mb-1">Erro ao buscar dados econômicos</p>
              <p className="text-sm text-red-300/80">
                {error instanceof Error ? error.message : 'Erro desconhecido'}
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="api-section">

      <div className="mb-8">
        <label className="block text-sm font-semibold text-slate-300 mb-4">
          Buscar país ou região
        </label>
        <div className="relative">
          <input
            type="text"
            placeholder="Ex: Brazil, Latin America, Upper middle income..."
            className="input-modern pl-12"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <svg 
            className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>


      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        <div className="p-6 rounded-xl bg-gradient-to-br from-orange-500/10 to-yellow-500/10 border border-orange-500/20">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-orange-500/20 flex items-center justify-center">
              <svg className="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-orange-300 font-medium">Total de Países</p>
              <p className="text-3xl font-black text-white">{allCountries.length}</p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-gradient-to-br from-yellow-500/10 to-amber-500/10 border border-yellow-500/20">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-yellow-500/20 flex items-center justify-center">
              <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-yellow-300 font-medium">Regiões</p>
              <p className="text-3xl font-black text-white">{regions.length}</p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-gradient-to-br from-amber-500/10 to-orange-500/10 border border-amber-500/20">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-amber-500/20 flex items-center justify-center">
              <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-amber-300 font-medium">Filtrados</p>
              <p className="text-3xl font-black text-white">{filteredCountries.length}</p>
            </div>
          </div>
        </div>
      </div>


      {filteredCountries.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {displayedCountries.map((country: any, idx: number) => (
              <div
                key={country.id || idx}
                className="group p-5 rounded-xl bg-gradient-to-br from-slate-800/80 to-slate-900/80 border border-slate-700/50 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg hover:shadow-orange-500/10 hover:border-slate-600/50"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-slate-100 truncate mb-1 group-hover:text-orange-400 transition-colors text-lg">
                      {country.name}
                    </h4>
                    {country.capital_city && (
                      <p className="text-sm text-slate-400 truncate flex items-center gap-1.5">
                        <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {country.capital_city}
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="space-y-2">
                  {country.region && (
                    <div className="flex items-center gap-2">
                      <span className="badge-orange flex items-center gap-1.5">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {country.region}
                      </span>
                    </div>
                  )}
                  
                  {country.income_level && (
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20 text-xs font-semibold">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {country.income_level}
                      </span>
                    </div>
                  )}
                  
                  {country.lending_type && (
                    <div className="text-xs text-slate-500 mt-2">
                      Tipo: {country.lending_type}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {hasMore && (
            <div className="flex justify-center mt-8">
              <button
                onClick={() => setShowAll(!showAll)}
                className="btn-modern-primary group flex items-center gap-2"
              >
                <span>{showAll ? 'Ver menos' : 'Ver mais'}</span>
                <svg 
                  className={`w-5 h-5 transition-transform duration-300 ${showAll ? 'rotate-180' : ''}`}
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-20">
          <div className="mx-auto w-20 h-20 mb-6 rounded-2xl bg-gradient-to-br from-yellow-600/20 to-orange-600/20 border border-yellow-500/30 flex items-center justify-center">
            <svg className="w-10 h-10 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <p className="text-slate-400 text-lg font-medium mb-2">
            Nenhum país encontrado
          </p>
          <p className="text-slate-500 text-sm">
            Tente buscar com outros termos
          </p>
        </div>
      )}
    </div>
  )
}

export default WorldBankCard
