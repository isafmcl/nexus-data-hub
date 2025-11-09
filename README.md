# Nexus Data Hub

Plataforma inteligente de integração com APIs públicas. Explore dados de livros, endereços, países, clima, notícias e economia global em um só lugar.

## Tecnologias

### Backend
- Python 3.13
- FastAPI
- Redis (cache)
- Structlog (logs estruturados)

### Frontend
- React 18
- TypeScript
- TailwindCSS
- Vite
- React Query

## APIs Integradas

1. **OpenWeather** - Previsão do tempo em tempo real
2. **NewsAPI** - Notícias globais por categoria
3. **REST Countries** - Informações de 250+ países
4. **ViaCEP** - Consulta de CEPs brasileiros
5. **OpenLibrary** - Busca de milhões de livros
6. **World Bank** - Indicadores econômicos globais

## Estrutura do Projeto

```
nexus-data-hub/
├── backend/           # API FastAPI
│   ├── src/
│   │   ├── api/      # Routers e controllers
│   │   ├── core/     # Configurações
│   │   └── utils/    # Utilidades (cache, logs, http)
│   └── requirements.txt
├── frontend/          # React App
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   └── package.json
└── infra/            # Docker compose e configs
```

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na pasta `infra/`:

```properties
OPENWEATHER_API_KEY=sua_chave_aqui
NEWSAPI_KEY=sua_chave_aqui
AWESOME_API_KEY=sua_chave_aqui
APP_SECRET=seu_secret_aqui
ENVIRONMENT=production
DEBUG=false
CACHE_ENABLED=true
REDIS_HOST=redis
REDIS_PORT=6379
APP_NAME=Nexus Data Hub
```

### APIs que requerem chave

- OpenWeather: https://openweathermap.org/api
- NewsAPI: https://newsapi.org/

## Executar com Docker

```bash
cd infra
docker-compose up -d
```

Acesse:
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Executar em Desenvolvimento

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Funcionalidades

### Busca de Livros
Pesquise por título, autor ou ISBN na base da OpenLibrary com milhões de livros disponíveis.

### Consulta de CEP
Encontre endereços completos no Brasil através do CEP usando a API ViaCEP.

### Dados de Países
Explore informações detalhadas de mais de 250 países incluindo capital, população, bandeira e região.

### Previsão do Tempo
Consulte o clima atual e previsões de qualquer cidade do mundo.

### Notícias Globais
Acesse as últimas notícias por categoria: negócios, tecnologia, esportes, saúde e mais.

### Dados Econômicos
Visualize indicadores econômicos de países através do World Bank.

## Cache e Performance

O sistema utiliza Redis para cache de requisições, reduzindo latência e melhorando performance:
- Weather: 30 minutos
- News: 30 minutos
- Countries: 24 horas
- CEP: 24 horas
- Books: 1 hora
- World Bank: 1 hora

