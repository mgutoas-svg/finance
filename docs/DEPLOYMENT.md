# 🚀 Guia de Deployment - Sistema de Gestão Financeira

## Índice
1. [Setup Local (Desenvolvimento)](#setup-local)
2. [Deploy Backend (Render/Railway)](#deploy-backend)
3. [Deploy Frontend (Vercel)](#deploy-frontend)
4. [Setup Supabase](#setup-supabase)
5. [Troubleshooting](#troubleshooting)

---

## Setup Local

### Pré-requisitos
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose (opcional)
- Git

### Opção 1: Com Docker Compose (Recomendado)

```bash
# Clone o repositório
git clone seu-repo
cd gestao-financeira

# Inicie os serviços
docker-compose up -d

# Acesse
# Frontend: http://localhost:5173
# Backend: http://localhost:8000/docs
# API Docs: http://localhost:8000/redoc
```

### Opção 2: Manual

#### Backend
```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis
cp .env.example .env
# Edite .env com suas credenciais

# Rodar migrations (se necessário)
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis
cp .env.example .env
# VITE_API_URL=http://localhost:8000

# Rodar dev server
npm run dev
```

---

## Deploy Backend

### Opção 1: Render.com (Recomendado)

#### Passo 1: Criar Projeto no Render
1. Acesse https://render.com
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: gestao-financeira-backend
   - **Environment**: Docker
   - **Branch**: main
   - **Auto-deploy**: Yes

#### Passo 2: Configurar Variáveis
No dashboard do Render, vá em "Environment":

```
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
SECRET_KEY=sua-chave-super-segura-random-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=https://seu-frontend.vercel.app,https://seu-dominio.com
DEBUG=false
```

#### Passo 3: Deploy Automático
Push para main triggers deploy automático

### Opção 2: Railway.app

1. Acesse https://railway.app
2. Crie novo projeto
3. Conecte repositório GitHub
4. Configure variáveis (mesmas do Render)
5. Deploy automático

### Opção 3: Vercel (Serverless)

Se usar Vercel para backend também:

```bash
# Instalar Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

---

## Deploy Frontend (Vercel)

### Passo 1: Conectar Repositório

1. Acesse https://vercel.com
2. Clique "Import Project"
3. Conecte seu repositório GitHub
4. Configure:
   - **Project name**: gestao-financeira
   - **Framework preset**: Vite
   - **Root directory**: ./frontend

### Passo 2: Variáveis de Ambiente

No settings do projeto, configure:

```
VITE_API_URL=https://seu-backend-url.com
VITE_SUPABASE_URL=https://seu-projeto.supabase.co
VITE_SUPABASE_ANON_KEY=sua-chave-publica-supabase
```

### Passo 3: Deploy

Push para main faz deploy automático

```bash
git push origin main
```

---

## Setup Supabase

### Passo 1: Criar Projeto

1. Acesse https://supabase.com
2. Clique "New Project"
3. Preencha:
   - **Project name**: gestao-financeira
   - **Database password**: gere uma senha forte
   - **Region**: Escolha a mais próxima
4. Aguarde criação (~2 min)

### Passo 2: Obter Credenciais

No menu "Settings" → "API":

```
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_ANON_KEY=[sua-chave-publica]
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
```

### Passo 3: Executar Schema

1. Abra "SQL Editor"
2. Clique "New Query"
3. Cole conteúdo de `database/schema.sql`
4. Clique "Run"
5. Pronto! Tabelas criadas

### Passo 4: Habilitar RLS (Segurança)

```sql
-- No SQL Editor do Supabase
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Criar policies
CREATE POLICY "Users can view their own data" ON transactions
  FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own data" ON transactions
  FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);
```

---

## Configurar Domínio Customizado

### No Vercel (Frontend)

1. Dashboard → Projeto → "Domains"
2. Adicione seu domínio
3. Configure DNS:
   ```
   A Record: 76.76.19.165
   ```
4. Aponte com seu registrador

### No Render (Backend)

1. Dashboard → Projeto → "Settings"
2. "Domains" → Add Custom Domain
3. Configure DNS conforme instruções

---

## Monitoramento & Logs

### Backend (Render/Railway)
- Logs em tempo real no dashboard
- Alertas de erro automáticos
- Métricas de performance

### Frontend (Vercel)
- Analytics integrado
- Logs de build
- Performance monitoring

### Database (Supabase)
- Query Performance
- Backup automático (diário)
- Replication monitoring

---

## Troubleshooting

### Erro: "Database connection failed"

```bash
# Verificar DATABASE_URL
echo $DATABASE_URL

# Testar conexão
psql $DATABASE_URL -c "SELECT 1;"

# Re-criar Dockerfile
docker build -t backend .
```

### Erro: "CORS error"

```bash
# Verificar CORS_ORIGINS no backend
# Deve incluir: https://seu-frontend.vercel.app

# Restart backend depois de atualizar
```

### Erro: "Token expired"

```bash
# Verificar JWT_EXPIRATION_HOURS
# Padrão: 24 horas

# Aumentar se necessário:
# JWT_EXPIRATION_HOURS=48
```

### Erro: "Upload failed"

```bash
# Verificar MAX_UPLOAD_SIZE_MB (padrão: 10)

# Aumentar se necessário:
# MAX_UPLOAD_SIZE_MB=50

# Restart backend
```

---

## Checklist de Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados inicializado (schema.sql executado)
- [ ] Usuário padrão criado (admin@financeiro.local)
- [ ] CORS configurado
- [ ] HTTPS habilitado
- [ ] Domínio apontando
- [ ] SSL certificate válido
- [ ] Backups configurados
- [ ] Monitoramento ativo
- [ ] Logs sendo coletados

---

## Rollback

### Se algo der errado:

```bash
# Render/Railway: Revert to previous deployment
# No dashboard → Deployments → Selecione versão anterior

# Vercel: Revert deployment
# Deployments → Clique em deployment anterior → Promote
```

---

## Performance Tips

1. **Frontend**
   - Ativar code splitting
   - Lazy load components
   - Cache headers corretos

2. **Backend**
   - Usar connection pooling
   - Cache queries frequentes
   - Indexar campos de busca

3. **Database**
   - Vacuum regulamente
   - Analyze query plans
   - Backup incremental

---

## Suporte

Para problemas:

1. Verificar logs (Render/Vercel dashboard)
2. Testar localmente com Docker
3. Verificar variáveis de ambiente
4. Validar credenciais do banco
5. Consultar documentação oficial

**Contato**: [seu-email] ou abra uma issue no GitHub
