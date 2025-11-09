import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

interface Article {
  title: string;
  description: string;
  url: string;
  image_url: string;
  published_at: string;
  source: {
    name: string;
    id?: string;
  };
  author?: string;
  content_preview?: string;
}

function NewsCard() {
  const [category, setCategory] = useState('general');

  const { data, isLoading, error } = useQuery({
    queryKey: ['news', category],
    queryFn: async () => {
      const response = await api.get(`/news?category=${category}`);
      return response.data;
    },
  });

  const articles = data?.success && data?.data?.articles 
    ? data.data.articles as Article[]
    : [];

  const categories = [
    { value: 'general', label: 'Geral', color: 'blue' },
    { value: 'business', label: 'Negócios', color: 'purple' },
    { value: 'technology', label: 'Tecnologia', color: 'cyan' },
    { value: 'sports', label: 'Esportes', color: 'green' },
    { value: 'entertainment', label: 'Entretenimento', color: 'pink' },
    { value: 'health', label: 'Saúde', color: 'red' },
    { value: 'science', label: 'Ciência', color: 'orange' },
  ];

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 60) return `Há ${diffMins} min`;
    if (diffHours < 24) return `Há ${diffHours}h`;
    if (diffDays < 7) return `Há ${diffDays} dias`;
    
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'short',
    });
  };

  return (
    <div className="api-section">

      <div className="mb-8">
        <label className="block text-sm font-semibold text-slate-300 mb-4">
          Selecione a Categoria
        </label>
        <div className="flex flex-wrap gap-3">
          {categories.map((cat) => (
            <button
              key={cat.value}
              onClick={() => setCategory(cat.value)}
              className={`
                px-5 py-2.5 rounded-xl font-semibold text-sm
                transition-all duration-300
                ${category === cat.value 
                  ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg shadow-blue-600/30 scale-105' 
                  : 'bg-slate-800/60 text-slate-400 hover:bg-slate-700/60 hover:text-slate-200 hover:scale-105 border border-slate-700/50'
                }
              `}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {isLoading && (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="spinner-modern mb-4"></div>
          <p className="text-slate-400 font-medium">Carregando notícias...</p>
        </div>
      )}

      {error && (
        <div className="p-6 rounded-xl bg-red-500/10 border border-red-500/30 backdrop-blur-sm">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="font-bold text-red-400 mb-1">Erro ao buscar notícias</p>
              <p className="text-sm text-red-300/80">
                {error instanceof Error ? error.message : 'Verifique se a API Key está configurada corretamente'}
              </p>
            </div>
          </div>
        </div>
      )}


      {!isLoading && !error && articles.length > 0 && (
        <div className="space-y-4">
          <p className="text-slate-400 text-sm mb-6">
            <span className="font-bold text-white text-lg">{articles.length}</span> notícias encontradas
          </p>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            {articles.slice(0, 10).map((article, index) => (
              <a
                key={index}
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="news-card group"
              >
                <div className="flex gap-5 p-5">

                  {article.image_url && (
                    <div className="relative w-32 h-32 flex-shrink-0 rounded-xl overflow-hidden">
                      <img
                        src={article.image_url}
                        alt={article.title}
                        className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                        onError={(e) => {
                          e.currentTarget.parentElement!.style.display = 'none';
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                    </div>
                  )}
                  

                  <div className="flex-1 min-w-0 flex flex-col">
                    <h3 className="font-bold text-slate-100 line-clamp-2 mb-2.5 group-hover:text-blue-400 transition-colors text-lg leading-snug">
                      {article.title}
                    </h3>
                    
                    {article.description && (
                      <p className="text-sm text-slate-400 line-clamp-2 mb-4 leading-relaxed">
                        {article.description}
                      </p>
                    )}
                    

                    <div className="mt-auto flex items-center gap-3 text-xs">
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-semibold">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                        {article.source.name}
                      </span>
                      <span className="text-slate-500 flex items-center gap-1.5">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {formatDate(article.published_at)}
                      </span>
                    </div>
                  </div>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {!isLoading && !error && articles.length === 0 && (
        <div className="text-center py-20">
          <div className="mx-auto w-20 h-20 mb-6 rounded-2xl bg-gradient-to-br from-red-600/20 to-pink-600/20 border border-red-500/30 flex items-center justify-center">
            <svg className="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
          </div>
          <p className="text-slate-400 text-lg font-medium">
            Nenhuma notícia encontrada para esta categoria
          </p>
        </div>
      )}
    </div>
  );
}

export default NewsCard;
