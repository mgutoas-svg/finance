# 🔧 Configuração de Variáveis de Ambiente

## Desenvolvimento Local

### Backend (.env)

Copie `backend/.env.example` para `backend/.env` e configure:

```env
# Database
DATABASE_URL=postgresql://financeiro_user:financeiro_pass@localhost:5432/financeiro_db

# JWT & Security
SECRET_KEY=sua-chave-secreta-super-segura-min-32-caracteres
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
REFRESH_TOKEN_EXPIRATION_DAYS=7

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true  # true apenas em desenvolvimento

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Email (opcional em desenvolvimento)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-app

# File Upload
MAX_UPLOAD_SIZE_MB=10
ALLOWED_FILE_TYPES=csv,pdf,xlsx

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log
```

### Frontend (.env)

Copie `frontend/.env.example` para `frontend/.env` e configure:

```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://seu-projeto.supabase.co
VITE_SUPABASE_ANON_KEY=sua-chave-publica
```

---

## Produção (Vercel + Render + Supabase)

### Supabase - Obter Credenciais

1. Acesse sua dashboard Supabase
2. Vá para **Project Settings** → **Database**
3. Copie a **Connection String**:
   ```
   postgresql://postgres.[projeto]:[password]@db.supabase.co:5432/postgres
   ```
4. Vá para **Settings** → **API**
5. Copie:
   - **Project URL** (ex: `https://projeto.supabase.co`)
   - **Anon Public Key** (para frontend)
   - **Service Role Key** (para backend)

### Frontend (Vercel)

Adicione em **Settings** → **Environment Variables**:

| Variável | Valor | Exemplo |
|----------|-------|---------|
| `VITE_API_URL` | URL do backend Render | `https://finance-api.render.com` |
| `VITE_SUPABASE_URL` | URL do Supabase | `https://projeto.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Chave pública Supabase | `eyJh...` |

**Redeployment:** Qualquer mudança requer re-deployment automático

### Backend (Render)

Adicione em **Environment**:

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `DATABASE_URL` | Connection String Supabase | URL de conexão com banco |
| `SECRET_KEY` | Valor aleatório 32+ caracteres | Chave para assinar JWTs |
| `JWT_ALGORITHM` | `HS256` | Algoritmo de assinatura |
| `JWT_EXPIRATION_HOURS` | `24` | Horas para expiração do token |
| `REFRESH_TOKEN_EXPIRATION_DAYS` | `7` | Dias para refresh token expirar |
| `API_HOST` | `0.0.0.0` | Interface de escuta |
| `API_PORT` | `8000` | Porta (Render ignora isso) |
| `DEBUG` | `false` | Nunca ativar em produção |
| `CORS_ORIGINS` | `https://finance-personal.vercel.app` | URL do frontend |
| `SUPABASE_URL` | URL do Supabase | Para edge functions (opcional) |
| `SUPABASE_KEY` | Service Role Key | Para edge functions (opcional) |
| `SMTP_SERVER` | `smtp.gmail.com` | Servidor de email |
| `SMTP_PORT` | `587` | Porta SMTP |
| `SMTP_EMAIL` | Seu email | Email para enviar |
| `SMTP_PASSWORD` | Senha app Gmail | Gere em Google Account |
| `MAX_UPLOAD_SIZE_MB` | `10` | Tamanho máximo de upload |
| `ALLOWED_FILE_TYPES` | `csv,pdf,xlsx` | Tipos de arquivo permitidos |
| `LOG_LEVEL` | `INFO` | Nível de logging |

**Como Copiar DATABASE_URL para Render:**

1. No Supabase, vá para **Project Settings** → **Database**
2. Clique em **Connection Pooling** (recomendado)
3. Copie a **Connection string** com `session` mode
4. Cole em `DATABASE_URL` no Render

---

## Geração de Chaves Seguras

### SECRET_KEY (Backend)

Gere uma chave aleatória forte:

**Python:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Linux/Mac:**
```bash
openssl rand -base64 32
```

**Windows PowerShell:**
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object {[byte](Get-Random -Maximum 256)}))
```

---

## Variáveis Obrigatórias vs Opcionais

### Backend - Obrigatórias
- `DATABASE_URL` ✅
- `SECRET_KEY` ✅
- `CORS_ORIGINS` ✅

### Backend - Opcionais
- Email/SMTP (para recuperação de senha)
- Supabase (para edge functions)

### Frontend - Obrigatórias
- `VITE_API_URL` ✅
- `VITE_SUPABASE_URL` ✅
- `VITE_SUPABASE_ANON_KEY` ✅

---

## Verificação de Variáveis

Para verificar se as variáveis estão corretas:

### Backend
```bash
# Verifique se backend pode conectar ao banco
curl -X GET http://localhost:8000/health
```

### Frontend
```bash
# Verifique se frontend consegue alcançar backend
# No console do navegador (F12):
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## Segurança

⚠️ **NUNCA FAÇA COMMIT DE ARQUIVOS .env**

✅ Sempre:
- Use `.env.example` como template
- Adicionar `.env` ao `.gitignore`
- Guardar chaves em local seguro (LastPass, 1Password, etc)
- Regenerar `SECRET_KEY` regularmente
- Rotacionar API keys do Supabase periodicamente

---

## Troubleshooting

### Erro: "Invalid DATABASE_URL"
- Verifique a sintaxe: `postgresql://user:pass@host:port/db`
- No Supabase, use Connection Pooling se recomendado
- Teste a conexão: `psql <DATABASE_URL>`

### Erro: "CORS blocked"
- Verifique se `CORS_ORIGINS` inclui a URL do frontend
- Inclua protocolo completo: `https://`, não apenas o domínio

### Erro: "Secret key too short"
- `SECRET_KEY` deve ter NO MÍNIMO 32 caracteres
- Regenere usando os comandos acima

### Erro: "Connection pooling timeout"
- Aumente timeout no Supabase
- Ou use connection string direta sem pooling

