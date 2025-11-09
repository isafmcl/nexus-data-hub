import React, { useState } from 'react'
import { useCep } from '@/hooks/useCep'

const CepCard: React.FC = () => {
  const [cepInput, setCepInput] = useState('')
  const [searchCep, setSearchCep] = useState<string | undefined>()
  
  const { data, isLoading, error } = useCep(searchCep)
  const cepData = (data && typeof data === 'object' && 'data' in data) ? data.data : data

  const handleSearch = () => {
    if (cepInput.trim()) {
      setSearchCep(cepInput.replace(/\D/g, ''))
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }


  const formatCep = (value: string) => {
    const numbers = value.replace(/\D/g, '')
    if (numbers.length <= 5) return numbers
    return `${numbers.slice(0, 5)}-${numbers.slice(5, 8)}`
  }

  const handleCepChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatCep(e.target.value)
    setCepInput(formatted)
  }

  return (
    <div className="api-section">
      <div className="mb-8">
        <label className="block text-sm font-semibold text-slate-300 mb-4">
          Digite um CEP brasileiro
        </label>
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Ex: 01001-000 ou 01001000"
            value={cepInput}
            onChange={handleCepChange}
            onKeyPress={handleKeyPress}
            className="input-modern flex-1"
            maxLength={9}
          />
          <button
            onClick={handleSearch}
            disabled={!cepInput.trim() || isLoading}
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

      {error && (
        <div className="p-6 rounded-xl bg-red-500/10 border border-red-500/30 backdrop-blur-sm">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="font-bold text-red-400 mb-1">CEP não encontrado</p>
              <p className="text-sm text-red-300/80">
                Verifique se o CEP está correto e tente novamente
              </p>
            </div>
          </div>
        </div>
      )}


      {cepData && !isLoading && (
        <div className="relative p-8 rounded-2xl bg-gradient-to-br from-green-500/20 via-emerald-500/15 to-teal-500/20 border border-green-500/30 backdrop-blur-sm overflow-hidden">
          <div className="absolute top-0 right-0 w-40 h-40 bg-green-400/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-40 h-40 bg-teal-400/10 rounded-full blur-3xl"></div>
          
          <div className="relative space-y-5">
            <div className="flex items-center gap-3 pb-4 border-b border-green-500/20">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-600 to-teal-600 flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-green-300 font-medium">CEP Encontrado</p>
                <p className="text-2xl font-black text-white">{cepData.cep}</p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {cepData.street && (
                <div className="col-span-full">
                  <div className="flex items-center gap-2 mb-2">
                    <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                    </svg>
                    <span className="text-sm text-green-300 font-semibold">Logradouro</span>
                  </div>
                  <p className="text-white text-lg font-medium pl-7">{cepData.street}</p>
                </div>
              )}
              
              {cepData.neighborhood && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <svg className="w-5 h-5 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <span className="text-sm text-teal-300 font-semibold">Bairro</span>
                  </div>
                  <p className="text-white font-medium pl-7">{cepData.neighborhood}</p>
                </div>
              )}
              
              {cepData.city && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <svg className="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                    </svg>
                    <span className="text-sm text-cyan-300 font-semibold">Cidade</span>
                  </div>
                  <p className="text-white font-medium pl-7">{cepData.city}</p>
                </div>
              )}
              
              {cepData.state && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
                    </svg>
                    <span className="text-sm text-blue-300 font-semibold">Estado</span>
                  </div>
                  <p className="text-white font-medium pl-7">{cepData.state}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {!cepData && !isLoading && !error && (
        <div className="text-center py-20">
          <div className="mx-auto w-20 h-20 mb-6 rounded-2xl bg-gradient-to-br from-green-600/20 to-emerald-600/20 border border-green-500/30 flex items-center justify-center">
            <svg className="w-10 h-10 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <p className="text-slate-400 text-lg font-medium mb-2">
            Digite um CEP para consultar
          </p>
          <p className="text-slate-500 text-sm">
            Busque endereços completos em todo o Brasil com a ViaCEP API
          </p>
        </div>
      )}
    </div>
  )
}

export default CepCard
