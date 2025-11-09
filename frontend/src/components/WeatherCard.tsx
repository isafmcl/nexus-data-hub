import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

interface WeatherData {
  location: {
    city: string;
    country: string;
    coordinates: {
      lat: number;
      lon: number;
    };
  };
  current: {
    temperature: number;
    feels_like: number;
    humidity: number;
    pressure: number;
    description: string;
    icon: string;
  };
  wind?: {
    speed: number;
    direction?: number;
  };
  clouds: {
    coverage: number;
  };
  visibility: number;
  timestamp: number;
}

function WeatherCard() {
  const [city, setCity] = useState('');
  const [searchCity, setSearchCity] = useState('');

  const { data, isLoading, error } = useQuery({
    queryKey: ['weather', searchCity],
    queryFn: async () => {
      if (!searchCity) return null;
      const response = await api.get(`/weather?city=${searchCity}`);
      return response.data;
    },
    enabled: !!searchCity,
  });

  const handleSearch = () => {
    if (city.trim()) {
      setSearchCity(city.trim());
    }
  };

  const weatherData = data?.success && data?.data 
    ? data.data as WeatherData 
    : null;

  return (
    <div className="api-section">
      <div className="mb-8">
        <label className="block text-sm font-semibold text-slate-300 mb-4">
          Digite o nome da cidade
        </label>
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Ex: São Paulo, Tokyo, London..."
            className="input-modern flex-1"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button
            onClick={handleSearch}
            disabled={!city.trim() || isLoading}
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
              <p className="font-bold text-red-400 mb-1">Erro ao buscar previsão</p>
              <p className="text-sm text-red-300/80">
                {error instanceof Error ? error.message : 'Verifique se a API Key está configurada corretamente'}
              </p>
            </div>
          </div>
        </div>
      )}


      {weatherData && (
        <div className="space-y-6">
  
          <div className="relative p-8 rounded-2xl bg-gradient-to-br from-sky-500/20 via-blue-500/15 to-cyan-500/20 border border-sky-500/30 backdrop-blur-sm overflow-hidden">

            <div className="absolute top-0 right-0 w-40 h-40 bg-blue-400/10 rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-40 h-40 bg-cyan-400/10 rounded-full blur-3xl"></div>
            
            <div className="relative">
 
              <div className="text-center mb-6">
                <h3 className="text-3xl font-extrabold text-white mb-2 flex items-center justify-center gap-2">
                  <svg className="w-7 h-7 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {weatherData.location.city}, {weatherData.location.country}
                </h3>
              </div>
              

              <div className="flex items-center justify-center gap-6 mb-6">
                {weatherData.current.icon && (
                  <div className="relative">
                    <div className="absolute inset-0 bg-blue-400/20 rounded-full blur-2xl"></div>
                    <img 
                      src={`https://openweathermap.org/img/wn/${weatherData.current.icon}@4x.png`}
                      alt={weatherData.current.description}
                      className="relative w-32 h-32 drop-shadow-2xl"
                    />
                  </div>
                )}
                <div className="text-center">
                  <p className="text-7xl font-black text-white mb-2">
                    {Math.round(weatherData.current.temperature)}°
                  </p>
                  <p className="text-xl text-blue-200 font-semibold capitalize">
                    {weatherData.current.description}
                  </p>
                </div>
              </div>
            </div>
          </div>


          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">

            <div className="weather-stat">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p className="text-sm text-slate-400 font-medium">Sensação</p>
              </div>
              <p className="text-3xl font-bold text-white">{Math.round(weatherData.current.feels_like)}°C</p>
            </div>


            <div className="weather-stat">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
                </svg>
                <p className="text-sm text-slate-400 font-medium">Umidade</p>
              </div>
              <p className="text-3xl font-bold text-white">{weatherData.current.humidity}%</p>
            </div>


            <div className="weather-stat">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
                <p className="text-sm text-slate-400 font-medium">Vento</p>
              </div>
              <p className="text-3xl font-bold text-white">{weatherData.wind?.speed || 0} <span className="text-lg text-slate-400">m/s</span></p>
            </div>


            <div className="weather-stat">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <p className="text-sm text-slate-400 font-medium">Pressão</p>
              </div>
              <p className="text-3xl font-bold text-white">{weatherData.current.pressure} <span className="text-lg text-slate-400">hPa</span></p>
            </div>
          </div>
        </div>
      )}

  
      {!searchCity && !isLoading && !error && (
        <div className="text-center py-20">
          <div className="mx-auto w-20 h-20 mb-6 rounded-2xl bg-gradient-to-br from-sky-600/20 to-blue-600/20 border border-sky-500/30 flex items-center justify-center">
            <svg className="w-10 h-10 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
            </svg>
          </div>
          <p className="text-slate-400 text-lg font-medium mb-2">
            Digite o nome de uma cidade
          </p>
          <p className="text-slate-500 text-sm">
            Veja a previsão do tempo em tempo real de qualquer lugar do mundo
          </p>
        </div>
      )}
    </div>
  );
}

export default WeatherCard;
