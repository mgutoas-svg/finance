# 🎯 Guia de Início - Próximos Passos

Parabéns! Você tem um sistema financeiro completo. Aqui está o que fazer agora:

---

## ✅ Checklist de Configuração

### 1️⃣ Local Development (5 min)

- [ ] Clonar repositório ou inicializar git
- [ ] Navegar para pasta `gestao-financeira`
- [ ] Executar `docker-compose up -d`
- [ ] Aguardar 30 segundos
- [ ] Testar acesso: http://localhost:5173
- [ ] Fazer login com credenciais padrão

```bash
# Quick commands
cd gestao-financeira
docker-compose up -d
# Aguarde 30s
# Abra http://localhost:5173
```

### 2️⃣ Git & GitHub (10 min)

- [ ] Criar repositório no GitHub
- [ ] Clonar este projeto
- [ ] Remover `.git` antigo (se houver)
- [ ] Inicializar novo git
- [ ] Fazer primeiro commit
- [ ] Push para main

```bash
# Em caso de novo repositório
cd gestao-financeira
rm -rf .git  # se existir

git init
git add .
git commit -m "Initial project structure"
git branch -M main
git remote add origin https://github.com/seu-usuario/seu-repo.git
git push -u origin main
```

### 3️⃣ Supabase Setup (15 min)

#### 3.1 Criar Projeto
- [ ] Ir para https://supabase.com
- [ ] Clique "New Project"
- [ ] Preencha:
  - **Name**: `gestao-financeira`
  - **Password**: Gere senha forte
  - **Region**: Próxima de você
- [ ] Clique "Create new project"
- [ ] Aguarde criação (~2 min)

#### 3.2 Obter Credenciais
- [ ] Vá em "Settings" → "API"
- [ ] Copie:
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
- [ ] Vá em "Database" → "Connection Pooling"
- [ ] Copie `CONNECTION_STRING`

#### 3.3 Executar Schema
- [ ] Vá em "SQL Editor" → "New Query"
- [ ] Cole conteúdo de `database/schema.sql`
- [ ] Clique "Run"
- [ ] Verifique se tabelas foram criadas

```sql
-- Copie tudo de database/schema.sql
-- E execute no SQL Editor do Supabase
```

#### 3.4 Armazenar Credenciais
- [ ] Salvar em local seguro (password manager)
- [ ] Usar em variáveis de ambiente depois

### 4️⃣ Configurar Backend (10 min)

#### 4.1 Variáveis de Ambiente
```bash
cd backend
cp .env.example .env
```

#### 4.2 Editar `.env`
```
DATABASE_URL=postgresql://[usuario]:[senha]@[host]:[porta]/[banco]
SECRET_KEY=gere-uma-chave-aleatoria-de-32-caracteres
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:5173,https://seu-frontend.vercel.app
DEBUG=false
```

**Onde obter?**
- `DATABASE_URL`: Supabase "Connection Pooling"
- `SECRET_KEY`: 
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

### 5️⃣ Configurar Frontend (5 min)

#### 5.1 Variáveis de Ambiente
```bash
cd frontend
cp .env.example .env
```

#### 5.2 Editar `.env`
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://[seu-projeto].supabase.co
VITE_SUPABASE_ANON_KEY=[sua-chave-publica]
```

### 6️⃣ Testar Localmente (5 min)

```bash
# Se não estiver rodando, inicie:
docker-compose up -d

# Acessar
# Frontend: http://localhost:5173
# Swagger: http://localhost:8000/docs

# Login
Email: admin@financeiro.local
Senha: SenhaTemporaria123!
```

- [ ] Página de login carrega
- [ ] Login funciona
- [ ] Dashboard carrega
- [ ] Não há erros no console

---

## 🚀 Deploy em Produção

### Phase 1: Frontend (Vercel) - 15 min

1. [ ] Ir para https://vercel.com
2. [ ] Clique "New Project"
3. [ ] Conecte repositório GitHub
4. [ ] Selecione projeto
5. [ ] Configure:
   - Root Directory: `./frontend`
   - Framework Preset: Vite
6. [ ] Clique "Environment Variables"
7. [ ] Adicione:
   ```
   VITE_API_URL=https://seu-backend.render.com
   VITE_SUPABASE_URL=...
   VITE_SUPABASE_ANON_KEY=...
   ```
8. [ ] Clique "Deploy"
9. [ ] Aguarde (2-3 min)
10. [ ] Teste em https://seu-projeto.vercel.app

### Phase 2: Backend (Render) - 20 min

1. [ ] Ir para https://render.com
2. [ ] Clique "New Web Service"
3. [ ] Conecte repositório GitHub
4. [ ] Configure:
   - **Name**: `gestao-financeira-backend`
   - **Environment**: Docker
   - **Branch**: main
   - **Root Directory**: `./backend`
5. [ ] Clique "Advanced"
6. [ ] Adicione variáveis (do passo de configuração backend):
   ```
   DATABASE_URL=...
   SECRET_KEY=...
   CORS_ORIGINS=https://seu-frontend.vercel.app
   ```
7. [ ] Clique "Create Web Service"
8. [ ] Aguarde deploy (5-10 min)
9. [ ] Teste em https://seu-backend.render.com/docs

### Phase 3: Conectar Frontend ao Backend - 5 min

1. [ ] No Vercel, ir em "Settings" → "Environment Variables"
2. [ ] Editar `VITE_API_URL`
3. [ ] Mudar para: `https://seu-backend.render.com`
4. [ ] Redeploy (automático ao fazer push)

---

## 📋 Configuração Pós-Deploy

### Primeiro Acesso Produção

1. [ ] Acessar https://seu-projeto.vercel.app
2. [ ] Login com `admin@financeiro.local` / `SenhaTemporaria123!`
3. [ ] **IMPORTANTE**: Alterar senha padrão
4. [ ] Configurar email de recuperação
5. [ ] Testar importação de dados

### Teste de Funcionalidades

- [ ] Dashboard carrega dados
- [ ] Pode criar transação
- [ ] Pode importar arquivo
- [ ] Pode criar meta
- [ ] Pode gerar relatório PDF
- [ ] Pode fazer logout
- [ ] Pode fazer login novamente

---

## 🔒 Segurança Pós-Deploy

### Verificações Essenciais

- [ ] SSL certificado válido (HTTPS)
- [ ] CORS só permite seu domínio
- [ ] Variáveis sensíveis não estão no Git
- [ ] Senha padrão foi alterada
- [ ] Backups estão configurados (Supabase)
- [ ] Logging está ativo

### GitHub Security

```bash
# Adicionar ao .gitignore (se não estiver)
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Remover .env se foi commitado acidentalmente
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## 📊 Próximas Features (Opcional)

### Semana 1
- [ ] Integrar com plataforma bancária (Open Banking)
- [ ] Exportar em mais formatos
- [ ] Dashboard em tempo real com WebSocket

### Semana 2
- [ ] Orçamento mensal detalhado
- [ ] Alertas por email
- [ ] Gráficos mais avançados

### Semana 3
- [ ] App mobile (React Native)
- [ ] Compartilhamento de dados (casal/família)
- [ ] Integração com Stripe (premium features)

---

## 🆘 Problemas Comuns & Soluções

### Login não funciona
```
✓ Verificar DATABASE_URL no backend
✓ Verificar se schema.sql foi executado
✓ Resetar senha do admin (SQL):
  UPDATE users SET hashed_password = '$2b$12...' WHERE email = 'admin@financeiro.local';
```

### CORS Error
```
✓ Adicionar seu domínio em CORS_ORIGINS
✓ Fazer redeploy do backend
✓ Limpar cache do navegador
```

### Dados não aparecem
```
✓ Verificar console (F12)
✓ Verificar logs do backend
✓ Testar em http://localhost:8000/docs
```

### Arquivo não importa
```
✓ Verificar formato (CSV, Excel, PDF)
✓ Verificar se tem colunas esperadas
✓ Ver logs do backend para erro específico
```

---

## 📞 Referências Rápidas

| Recurso | Link |
|---------|------|
| Supabase Docs | https://supabase.com/docs |
| FastAPI Docs | https://fastapi.tiangolo.com |
| React Docs | https://react.dev |
| Vercel Docs | https://vercel.com/docs |
| Render Docs | https://render.com/docs |

---

## 📝 Logs & Monitoramento

### Onde ver logs?

**Backend (Render)**
- Dashboard → Seu projeto → "Logs"

**Frontend (Vercel)**
- Dashboard → Seu projeto → "Deployments"

**Database (Supabase)**
- Dashboard → "Database" → "Logs"

### Monitoramento Recomendado

- [ ] Verificar logs diariamente primeira semana
- [ ] Configurar alertas no Render
- [ ] Monitorar performance no Vercel
- [ ] Backup automático Supabase (já ativado)

---

## 🎓 Documentação de Referência

**Para maiores detalhes, leia:**

1. `README.md` - Overview geral
2. `QUICK_START.md` - Primeiros 5 minutos
3. `DEPLOYMENT.md` - Deploy passo a passo
4. `ARCHITECTURE.md` - Como funciona tudo
5. `PROJECT_SUMMARY.md` - Resumo do que foi criado

---

## ✅ Checklist Final

Antes de considerar "pronto":

- [ ] Git repository criado e commit inicial feito
- [ ] Backend deployado no Render
- [ ] Frontend deployado no Vercel
- [ ] Supabase configurado com dados
- [ ] Domínio customizado configurado (opcional)
- [ ] SSL/HTTPS funcionando
- [ ] Senha padrão alterada
- [ ] Email de recuperação configurado
- [ ] Dados importados (teste com CSV)
- [ ] Relatório PDF funciona
- [ ] Testes no navegador (Chrome, Firefox, Safari)
- [ ] Testes em mobile
- [ ] Logs sendo monitorados

---

## 🎉 Pronto!

Parabéns! Você tem um sistema financeiro profissional rodando em produção!

**Próximos passos:**
1. Usar o sistema diariamente
2. Coletar feedback
3. Implementar melhorias
4. Adicionar mais features conforme necessário

---

*Última atualização: 2026-09-28*

**Dúvidas?** Consulte os arquivos `.md` ou os logs do sistema.

**Sucesso! 🚀**
