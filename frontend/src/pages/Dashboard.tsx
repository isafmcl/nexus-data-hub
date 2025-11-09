import BooksSearch from '../components/BooksSearch'
import CountriesCard from '../components/CountriesCard'
import CepCard from '../components/CepCard'
import WorldBankCard from '../components/WorldBankCard'
import WeatherCard from '../components/WeatherCard'
import NewsCard from '../components/NewsCard'

const Dashboard = () => {
  const activeTab = 'all';

  return (
    <div className="min-h-screen">
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl floating"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500/20 rounded-full blur-3xl floating" style={{ animationDelay: '2s' }}></div>
        </div>

        <div className="relative px-6 py-12 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="text-center space-y-4">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-600/20 border border-blue-500/30 backdrop-blur-sm">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
                <span className="text-green-400 text-sm font-medium">6 APIs Ativas</span>
              </div>
              
              <h1 className="text-5xl lg:text-6xl font-bold gradient-text">
                Nexus Data Hub
              </h1>
              
              <p className="text-xl text-slate-300 max-w-2xl mx-auto">
                Plataforma inteligente de integração com APIs. 
                Explore dados de livros, endereços, países, clima, notícias e economia global em um só lugar.
              </p>
            </div>
          </div>
        </div>
      </div>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {(activeTab === 'all' || activeTab === 'books') && (
          <section className="mb-12 fade-in stagger-item">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center shadow-lg shadow-blue-600/30">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">Busca de Livros</h2>
                <p className="text-slate-400 text-sm">OpenLibrary API - Milhões de livros disponíveis</p>
              </div>
            </div>
            <BooksSearch />
          </section>
        )}

        {(activeTab === 'all' || activeTab === 'cep') && (
          <section className="mb-12 fade-in stagger-item">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-green-600 to-emerald-600 flex items-center justify-center shadow-lg shadow-green-600/30">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">Consulta de CEP</h2>
                <p className="text-slate-400 text-sm">ViaCEP API - Endereços brasileiros</p>
              </div>
            </div>
            <CepCard />
          </section>
        )}

        {(activeTab === 'all' || activeTab === 'countries') && (
          <section className="mb-12 fade-in stagger-item">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-600/30">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">Dados de Países</h2>
                <p className="text-slate-400 text-sm">REST Countries API - Informações completas de 250+ países</p>
              </div>
            </div>
            <CountriesCard />
          </section>
        )}

        {(activeTab === 'all' || activeTab === 'worldbank') && (
          <section className="mb-12 fade-in stagger-item">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-yellow-600 to-orange-600 flex items-center justify-center shadow-lg shadow-yellow-600/30">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">Dados Econômicos</h2>
                <p className="text-slate-400 text-sm">World Bank API - Indicadores econômicos globais</p>
              </div>
            </div>
            <WorldBankCard />
          </section>
        )}

        {(activeTab === 'all' || activeTab === 'weather') && (
          <section className="mb-12 fade-in stagger-item">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-sky-600 to-blue-600 flex items-center justify-center shadow-lg shadow-sky-600/30">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">Previsão do Tempo</h2>
                <p className="text-slate-400 text-sm">OpenWeather API - Clima em tempo real</p>
              </div>
            </div>
            <WeatherCard />
          </section>
        )}

        {(activeTab === 'all' || activeTab === 'news') && (
          <section className="mb-12 fade-in stagger-item">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-red-600 to-pink-600 flex items-center justify-center shadow-lg shadow-red-600/30">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">Notícias Globais</h2>
                <p className="text-slate-400 text-sm">NewsAPI - Últimas notícias do mundo</p>
              </div>
            </div>
            <NewsCard />
          </section>
        )}
      </main>

      <footer className="border-t border-slate-800/50 backdrop-blur-xl bg-slate-900/50 mt-20">
        <div className="mx-auto max-w-7xl px-6 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-center md:text-left">
              <p className="text-slate-400 text-sm">
                © 2025 Nexus Data Hub. Plataforma de integração de APIs.
              </p>
            </div>
            <div className="flex gap-4 flex-wrap justify-center">
              <div className="stat-badge">
                <span>FastAPI + React</span>
              </div>
              <div className="stat-badge">
                <span>TailwindCSS</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
