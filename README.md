# 💰 Sistema de Gestão Financeira Pessoal

Sistema completo de análise financeira pessoal com importação de dados, análise de gastos e gestão de metas.

## 🎯 Funcionalidades

- ✅ Importação de dados (CSV, PDF, Excel)
- ✅ Consolidação financeira (receita, despesa, lucro/prejuízo)
- ✅ Análise por categorias com alertas
- ✅ Gestão de metas (diária, semanal, mensal)
- ✅ Plano de ação para atingir metas
- ✅ Geração de relatórios em PDF
- ✅ Autenticação segura (JWT)
- ✅ Dashboard interativo com gráficos

## 🏗️ Stack Técnico

- **Frontend**: React 18 + Vite + TailwindCSS
- **Backend**: Python FastAPI
- **Database**: Supabase (PostgreSQL)
- **Deploy**: Vercel (frontend) + Render/Fly (backend)
- **Auth**: JWT + Supabase Auth

## 📁 Estrutura do Projeto

```
gestao-financeira/
├── backend/                 # API Python FastAPI
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│   └── docker-compose.yml
│
├── frontend/                # React + Vite
│   ├── src/
│   ├── package.json
│   ├── .env.example
│   └── vite.config.js
│
├── database/
│   └── schema.sql           # PostgreSQL schema
│
└── docs/
    └── DEPLOYMENT.md        # Guia de deploy
```

## 🚀 Quick Start (Desenvolvimento Local)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou: venv\Scripts\activate (Windows)
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
# Acessa: http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
# Acessa: http://localhost:5173
```

## 🔐 Autenticação

**Usuário padrão:**
- Email: `admin@financeiro.local`
- Senha: `SenhaTemporaria123!`

⚠️ **Altere a senha no primeiro acesso!**

## 📊 API Principal Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/login` | Fazer login |
| POST | `/api/auth/change-password` | Alterar senha |
| GET | `/api/transactions` | Listar lançamentos |
| POST | `/api/transactions/import` | Importar arquivo |
| GET | `/api/analytics/summary` | Resumo financeiro |
| GET | `/api/goals` | Listar metas |
| POST | `/api/reports/pdf` | Gerar relatório PDF |

## 🔧 Variáveis de Ambiente

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=sua-chave-secreta-jwt
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:5173,https://seu-frontend.vercel.app
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://seu-project.supabase.co
VITE_SUPABASE_ANON_KEY=sua-chave-publica
```

## 📚 Documentação Completa

Ver `docs/DEPLOYMENT.md` para:
- Setup Supabase
- Deploy Vercel
- Deploy Backend
- Configuração de domínio
- Troubleshooting

## 🤝 Contribuindo

1. Clone o repositório
2. Crie uma branch (`git checkout -b feature/sua-feature`)
3. Commit suas mudanças (`git commit -am 'Add feature'`)
4. Push para a branch (`git push origin feature/sua-feature`)
5. Abra um Pull Request

## 📄 Licença

MIT

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
