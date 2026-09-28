# 🏗️ Arquitetura do Sistema

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (React/Vite)                       │
│                     Running on Vercel                           │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                            │
│                  Running on Render/Railway                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Database (Supabase/PostgreSQL)                 │
│              Managed PostgreSQL + Authentication                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Backend (Python FastAPI)

### Estrutura de Pastas

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point FastAPI
│   ├── config.py            # Configurações globais
│   ├── database.py          # Conexão com DB
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas (validação)
│   ├── security.py          # JWT, autenticação
│   ├── crud.py              # Operações DB
│   │
│   ├── routes/              # Endpoints da API
│   │   ├── auth.py          # Login, senha, recuperação
│   │   ├── transactions.py  # Lançamentos financeiros
│   │   ├── categories.py    # Categorias
│   │   ├── goals.py         # Metas financeiras
│   │   ├── analytics.py     # Análises e insights
│   │   └── reports.py       # Geração de relatórios
│   │
│   ├── services/            # Lógica de negócio
│   │   ├── file_processor.py     # Processa CSV/PDF/Excel
│   │   ├── data_sanitizer.py     # Remove dados sensíveis
│   │   └── report_generator.py   # Cria PDFs
│   │
│   └── middleware/          # Middlewares
│       ├── logging.py       # Log de requisições
│       └── error_handler.py # Tratamento de erros
│
├── requirements.txt         # Dependências Python
├── .env.example            # Template de variáveis
├── Dockerfile              # Containerização
└── alembic/                # Migrations (opcional)
```

### Stack Técnico

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Framework | FastAPI | 0.104+ |
| Server | Uvicorn | 0.24+ |
| ORM | SQLAlchemy | 2.0+ |
| Database | PostgreSQL | 13+ |
| Auth | JWT + bcrypt | - |
| File Processing | pandas, PyPDF2 | - |
| PDF Generation | ReportLab | 4.0+ |

### Fluxo de Requisição

```
1. Request chega em FastAPI
2. Middleware de logging
3. Validação de token JWT
4. Verificação de permissões
5. Execução da rota
6. CRUD no banco de dados
7. Validação de schema Pydantic
8. Response JSON
```

### Segurança

- **Autenticação**: JWT com refresh token
- **Senha**: Bcrypt com salt
- **Validação**: Pydantic models
- **SQL Injection**: SQLAlchemy ORM parameterizado
- **CORS**: Whitelist de origens
- **Rate Limiting**: Implementável com middleware
- **Sanitização**: DataSanitizer remove dados sensíveis

---

## Frontend (React + Vite)

### Estrutura de Pastas

```
frontend/
├── src/
│   ├── main.jsx             # Entry point
│   ├── App.jsx              # Router principal
│   ├── index.css            # Estilos globais
│   │
│   ├── pages/               # Pages (route level)
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── TransactionsPage.jsx
│   │   ├── CategoriesPage.jsx
│   │   ├── GoalsPage.jsx
│   │   ├── AnalyticsPage.jsx
│   │   └── SettingsPage.jsx
│   │
│   ├── components/          # Componentes reutilizáveis
│   │   ├── Layout.jsx       # Sidebar + Header
│   │   ├── PrivateRoute.jsx # Protected routes
│   │   └── common/          # Componentes comuns
│   │       ├── Card.jsx
│   │       ├── Modal.jsx
│   │       └── LoadingSpinner.jsx
│   │
│   ├── store/               # Zustand stores
│   │   ├── authStore.js     # Estado de autenticação
│   │   └── financialStore.js # Estado financeiro
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.js
│   │   └── useFinancial.js
│   │
│   ├── services/            # Serviços HTTP
│   │   ├── api.js           # Axios instance
│   │   └── apiClient.js     # Funções de API
│   │
│   └── utils/               # Utilidades
│       ├── formatters.js    # Formatar moeda, datas
│       └── validators.js    # Validação de inputs
│
├── public/                  # Arquivos estáticos
├── index.html              # HTML template
├── vite.config.js          # Configuração Vite
├── tailwind.config.js      # Configuração TailwindCSS
├── package.json            # Dependências
├── .env.example            # Template de variáveis
└── vercel.json             # Configuração Vercel
```

### Stack Técnico

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Framework | React | 18+ |
| Builder | Vite | 5+ |
| CSS | TailwindCSS | 3+ |
| Router | React Router | 6+ |
| State | Zustand | 4+ |
| HTTP | Axios | 1.6+ |
| Charts | Recharts | 2+ |
| Icons | Lucide React | - |
| Notifications | React Hot Toast | 2+ |

### State Management (Zustand)

```
authStore
├── user
├── token
├── refreshToken
├── isAuthenticated
└── methods: login, logout, changePassword

financialStore
├── transactions
├── categories
├── goals
├── summary
├── categoryAnalysis
├── recommendations
└── methods: fetch*, create*, update*, delete*
```

### Fluxo de Autenticação

```
1. Usuário acessa /login
2. Entra credenciais
3. Requisição POST /api/auth/login
4. Backend retorna access_token + refresh_token
5. Zustand armazena tokens (localStorage)
6. Usuario é redirecionado para /
7. PrivateRoute verifica isAuthenticated
8. Autoriza acesso aos componentes
```

---

## Database (Supabase/PostgreSQL)

### Schema de Dados

```
users
├── id (PK)
├── email (UNIQUE)
├── hashed_password
├── full_name
├── recovery_email
├── is_active
├── created_at
└── updated_at

categories
├── id (PK)
├── user_id (FK)
├── name
├── description
├── is_custom
├── ideal_percentage
├── alert_percentage
└── created_at

transactions
├── id (PK)
├── user_id (FK)
├── category_id (FK)
├── description
├── amount
├── transaction_date (INDEX)
├── transaction_type
├── source
├── notes
├── created_at
└── updated_at

goals
├── id (PK)
├── user_id (FK)
├── title
├── description
├── target_amount
├── current_amount
├── frequency
├── due_date
├── status
├── created_at
└── updated_at

file_uploads
├── id (PK)
├── user_id (FK)
├── filename
├── file_type
├── status
├── records_imported
├── error_message
└── uploaded_at

audit_logs
├── id (PK)
├── user_id (FK)
├── action
├── resource_type
├── resource_id
├── old_values (JSON)
├── new_values (JSON)
├── ip_address
├── user_agent
└── created_at (INDEX)
```

### Indexes

```sql
-- Performance indexes
idx_users_email
idx_transactions_user_id
idx_transactions_category_id
idx_transactions_date
idx_categories_user_id
idx_goals_user_id
idx_audit_logs_user_id
idx_audit_logs_created_at
```

---

## Fluxo de Dados - Importação

```
┌─────────────────────┐
│  Usuário faz upload │
│  (CSV/PDF/Excel)    │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│  Frontend valida tipo arquivo│
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Envia para /api/transactions │
│         /import              │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ FileProcessor processa arquivo│
│ (CSV/PDF/Excel)              │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ DataSanitizer remove dados   │
│ sensíveis (CPF, endereço)    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Valida com Pydantic schemas  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Salva no Database (CRUD)     │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Retorna resultado ao frontend│
│ (registros importados)       │
└──────────────────────────────┘
```

---

## Fluxo de Dados - Analytics

```
Frontend
   ↓
fetchCategoryAnalysis(token, startDate, endDate)
   ↓
GET /api/analytics/by-category?start_date=...&end_date=...
   ↓
Backend
   ├─ Query transactions no período
   ├─ Agrupa por category_id
   ├─ Calcula totais e percentuais
   ├─ Verifica alertas (>ideal_percentage * 1.2)
   └─ Retorna CategoryAnalysis[]
   ↓
Frontend
   ├─ Armazena em financialStore
   ├─ Renderiza gráficos (Recharts)
   └─ Exibe tabelas analíticas
```

---

## Ciclo de Vida - CRUD Transaction

```
┌─ CREATE ─────────────────────────────────────┐
│ Frontend → POST /api/transactions            │
│ Backend: CRUD.create_transaction()           │
│ DB: INSERT INTO transactions                 │
│ Response: TransactionResponse (com ID)       │
└──────────────────────────────────────────────┘

┌─ READ ───────────────────────────────────────┐
│ Frontend → GET /api/transactions?filters     │
│ Backend: CRUD.get_transactions()             │
│ DB: SELECT * FROM transactions WHERE ...     │
│ Response: List[TransactionResponse]          │
└──────────────────────────────────────────────┘

┌─ UPDATE ─────────────────────────────────────┐
│ Frontend → PUT /api/transactions/{id}        │
│ Backend: CRUD.update_transaction()           │
│ DB: UPDATE transactions SET ... WHERE id=?   │
│ Response: TransactionResponse (atualizado)   │
└──────────────────────────────────────────────┘

┌─ DELETE ─────────────────────────────────────┐
│ Frontend → DELETE /api/transactions/{id}     │
│ Backend: CRUD.delete_transaction()           │
│ DB: DELETE FROM transactions WHERE id=?      │
│ Response: {"message": "deletado"}            │
└──────────────────────────────────────────────┘
```

---

## Camadas e Responsabilidades

```
┌─────────────────────────────────────────┐
│  PRESENTATION (Frontend)                │
│  - Components React                     │
│  - Validação de entrada                 │
│  - Exibição de dados                    │
└────────────┬────────────────────────────┘
             │ JSON via HTTPS
┌────────────▼────────────────────────────┐
│  API LAYER (Backend Routes)             │
│  - Endpoints FastAPI                    │
│  - Validação de requisição              │
│  - Autenticação/Autorização             │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  SERVICE LAYER                          │
│  - Lógica de negócio                    │
│  - Processamento de dados               │
│  - Cálculos e análises                  │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  DATA ACCESS LAYER (CRUD)               │
│  - Operações no banco                   │
│  - Queries otimizadas                   │
│  - Caching (opcional)                   │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  DATABASE LAYER                         │
│  - PostgreSQL                           │
│  - Indexes                              │
│  - Backup & Replication                 │
└─────────────────────────────────────────┘
```

---

## Decisões Arquiteturais

### Por que Zustand em vez de Redux?
- Menor bundle size
- API mais simples
- Sem boilerplate
- Suporta middleware custom

### Por que TailwindCSS?
- Utility-first (desenvolvimento rápido)
- Tamanho pequeno quando otimizado
- Componentes consistentes
- Dark mode suportado

### Por que FastAPI?
- Performance otimizada (async/await)
- Validação automática com Pydantic
- Documentação Swagger automática
- Type hints nativos

### Por que Supabase?
- PostgreSQL gerenciado
- Sem DevOps
- Backup automático
- Authentication integrada
- RLS (Row Level Security)

---

## Próximas Melhorias

- [ ] WebSockets para real-time updates
- [ ] Testes automatizados (pytest, Jest)
- [ ] Caching com Redis
- [ ] Rate limiting
- [ ] Paginação otimizada
- [ ] Busca full-text
- [ ] Integração com Stripe para premium
- [ ] Mobile app (React Native)

---

*Última atualização: 2026-09-28*
