# 📋 Guia Completo de Deploy - Sistema de Finanças Pessoais

## 🎯 Objetivos
- Deploy do Frontend no **Vercel**
- Deploy do Backend no **Render**
- Banco de Dados **Supabase** (PostgreSQL)
- CI/CD automático com **GitHub Actions**

---

## 1️⃣ Preparação Inicial

### 1.1 Conectar GitHub
```bash
# Certifique-se que o repositório está no GitHub
git remote -v
# Se não estiver:
git remote add origin https://github.com/mgutoas-svg/finance.git
```

### 1.2 Criar Conta Supabase
1. Acesse [supabase.com](https://supabase.com)
2. Faça login/registre-se
3. Clique em "New Project"
4. Preencha:
   - **Project name**: `finance-personal`
   - **Database password**: Gere uma senha forte (anote-a!)
   - **Region**: Escolha a mais próxima (ex: `us-east-1` ou `sa-east-1`)
5. Aguarde o projeto ser criado

### 1.3 Configurar Banco de Dados no Supabase
1. Na dashboard do projeto, vá para **SQL Editor**
2. Clique em **New Query**
3. Cole o conteúdo do arquivo `database/schema.sql`
4. Execute a query

### 1.4 Obter Credenciais Supabase
1. Vá para **Project Settings** → **Database**
2. Copie:
   - **Connection String** (será usada como `DATABASE_URL`)
   - **Direct URL** (para backup)
3. Vá para **Settings** → **API**
4. Copie:
   - **Project URL** (será `VITE_SUPABASE_URL`)
   - **Anon Public Key** (será `VITE_SUPABASE_ANON_KEY`)
   - **Service Role Key** (será `SUPABASE_SERVICE_ROLE_KEY`)

---

## 2️⃣ Deploy Frontend no Vercel

### 2.1 Conectar Vercel ao GitHub
1. Acesse [vercel.com](https://vercel.com)
2. Faça login com GitHub
3. Clique em **Add New Project**
4. Selecione o repositório `finance`
5. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (automático)
   - **Output Directory**: `dist` (automático)

### 2.2 Configurar Variáveis de Ambiente

No Vercel, vá para **Settings** → **Environment Variables** e adicione:

```
VITE_API_URL=https://finance-api.render.com
VITE_SUPABASE_URL=https://[seu-projeto].supabase.co
VITE_SUPABASE_ANON_KEY=[sua-anon-key]
```

> **Nota**: A `VITE_API_URL` será alterada após fazer o deploy do backend

### 2.3 Fazer Deploy
- O deployment acontece automaticamente quando você fizer push para `main`
- Você verá a URL do seu frontend (ex: `https://finance-personal.vercel.app`)

---

## 3️⃣ Deploy Backend no Render

### 3.1 Conectar Render ao GitHub
1. Acesse [render.com](https://render.com)
2. Faça login/registre-se
3. Clique em **New +** → **Web Service**
4. Selecione o repositório `finance`
5. Configure:
   - **Name**: `finance-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Root Directory**: `/` (raiz do projeto)

### 3.2 Configurar Variáveis de Ambiente

Clique em **Environment** e adicione:

```
DATABASE_URL=postgresql://[user]:[password]@[host]:5432/[database]
SECRET_KEY=[gere uma chave segura com 32+ caracteres]
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
REFRESH_TOKEN_EXPIRATION_DAYS=7
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
CORS_ORIGINS=https://finance-personal.vercel.app,http://localhost:5173
SUPABASE_URL=https://[seu-projeto].supabase.co
SUPABASE_KEY=[sua-service-role-key]
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=[seu-email]
SMTP_PASSWORD=[sua-senha-app]
MAX_UPLOAD_SIZE_MB=10
ALLOWED_FILE_TYPES=csv,pdf,xlsx
LOG_LEVEL=INFO
```

### 3.3 Fazer Deploy
- Clique em **Deploy**
- Aguarde o build completar
- Você receberá uma URL (ex: `https://finance-api.render.com`)

### 3.4 Atualizar Frontend
1. Volte ao Vercel
2. Vá para **Settings** → **Environment Variables**
3. Atualize `VITE_API_URL` com a URL do Render
4. Faça deploy novamente ou aguarde re-deployment automático

---

## 4️⃣ Configurar CI/CD (GitHub Actions)

### 4.1 Criar Workflow
Crie o arquivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy Frontend
        run: |
          echo "Frontend deployed to Vercel (automático)"
      
      - name: Deploy Backend
        run: |
          echo "Backend deployed to Render (automático)"
```

---

## 5️⃣ Verificações Finais

### 5.1 Testar Autenticação
```bash
curl -X POST https://finance-api.render.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@financeiro.local","password":"SenhaTemporaria123!"}'
```

### 5.2 Testar Conexão Frontend-Backend
1. Acesse `https://finance-personal.vercel.app`
2. Tente fazer login
3. Verifique o Network no DevTools se as requisições estão indo para o backend correto

### 5.3 Testar Banco de Dados
1. Na dashboard Supabase, vá para **SQL Editor**
2. Execute:
```sql
SELECT * FROM users LIMIT 1;
```

---

## 6️⃣ Monitoramento e Manutenção

### 6.1 Logs
- **Frontend**: Vercel → **Deployments** → clique em um deployment → **Logs**
- **Backend**: Render → **Logs**
- **Banco**: Supabase → **Logs**

### 6.2 Variáveis de Ambiente
- Qualquer mudança em `.env` deve ser feita na dashboard do serviço
- Não faça commit de arquivos `.env` reais

### 6.3 Backups
- Supabase faz backups automáticos
- Para backup manual: Dashboard Supabase → **Backups**

---

## 7️⃣ Troubleshooting

### Erro 500 no Backend
1. Verifique se `DATABASE_URL` está correto
2. Verifique se o schema foi executado no Supabase
3. Veja os logs do Render

### Erro CORS
1. Verifique `CORS_ORIGINS` no backend
2. Certifique-se que a URL do Vercel está corretamente configurada
3. Restart o backend no Render

### Erro de Conexão ao Banco
1. Verifique se o IP do Render está permitido no Supabase
2. Supabase permite apenas conexões da rede interna por padrão
3. Vá para **Project Settings** → **Database** → **Connection pooling** e use a connection string com pooling

---

## 8️⃣ URLs Finais

Após tudo configurado:
- **Frontend**: `https://finance-personal.vercel.app`
- **Backend API**: `https://finance-api.render.com`
- **Banco de Dados**: Supabase Cloud
- **Dashboard Supabase**: Você tem acesso na conta

---

## 🚨 Checklist Final

- [ ] Supabase projeto criado
- [ ] Schema executado no banco
- [ ] Credenciais Supabase copiadas
- [ ] Frontend conectado ao Vercel
- [ ] Variáveis de ambiente do Vercel configuradas
- [ ] Backend conectado ao Render
- [ ] Variáveis de ambiente do Render configuradas
- [ ] Banco de dados conectando corretamente
- [ ] Autenticação funcionando
- [ ] Frontend comunicando com backend
- [ ] CI/CD configurado (opcional)

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs de cada serviço
2. Valide as variáveis de ambiente
3. Teste as conexões individualmente
4. Abra uma issue no repositório

