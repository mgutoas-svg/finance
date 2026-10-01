# 🚀 GUIA DE DEPLOYMENT AGORA - Passo a Passo

## 📋 Seu Status Atual

✅ Credenciais Supabase: Configuradas  
✅ Código atualizado: No GitHub  
✅ Tudo pronto: Para fazer deploy!

---

## 🎯 Vai levar 15 minutos total

### **PASSO 1: Deploy Frontend no Vercel (5 min)**

1. Abra https://vercel.com em um navegador
2. Clique em **Sign Up** (ou faça login se já tem conta)
3. **Conecte seu GitHub**
4. Clique em **Add New Project**
5. Procure e selecione `finance`
6. Configure:
   - **Project Name**: deixe `finance`
   - **Framework**: `Vite` (detecta automático)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (automático)
   - **Output Directory**: `dist` (automático)

7. **Clique em Deploy**
8. Aguarde 2-3 minutos até terminar
9. Copie a URL que aparece (algo como `https://finance-xxxxxx.vercel.app`)

**Salve essa URL! Precisaremos dela depois.**

---

### **PASSO 2: Deploy Backend no Render (10 min)**

1. Abra https://render.com em um navegador
2. Clique em **Sign Up** (ou faça login)
3. **Conecte seu GitHub**
4. Clique em **New +**
5. Selecione **Web Service**
6. Procure `finance` e clique
7. Configure:
   - **Name**: `finance-api`
   - **Environment**: `Python 3`
   - **Branch**: `main`
   - **Build Command**: 
     ```
     pip install -r backend/requirements.txt
     ```
   - **Start Command**:
     ```
     cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
     ```

8. **Clique em Advanced** (expande mais opções)
9. Em **Environment Variables**, clique **Add From File** ou adicione manualmente:

**COPIE E COLE ESTAS VARIÁVEIS:**

```
DATABASE_URL=postgresql://postgres:$@Mg9586as@db.supabase.co:5432/postgres
SECRET_KEY=finance-sistema-seguranca-chave-super-secreta-32-caracteres-minimo
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
REFRESH_TOKEN_EXPIRATION_DAYS=7
API_HOST=0.0.0.0
DEBUG=false
CORS_ORIGINS=https://SEU_FRONTEND_VERCEL_AQUI.vercel.app
SUPABASE_URL=https://ekpyjbkqniinpqilindo.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrcHlqYmtxbmlpbnBxaWxpbmRvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDIwOTQxMCwiZXhwIjoyMDk1Nzg1NDEwfQ.sojFCLJCqv9dk8EBZI8oi8iKwGzXJuIJqslVb3CpjIo
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
MAX_UPLOAD_SIZE_MB=10
ALLOWED_FILE_TYPES=csv,pdf,xlsx
LOG_LEVEL=INFO
```

**IMPORTANTE:** Na variável `CORS_ORIGINS`, substitua `SEU_FRONTEND_VERCEL_AQUI` pela URL do Vercel que você salvou no Passo 1!

Exemplo:
```
CORS_ORIGINS=https://finance-abc123xyz.vercel.app
```

10. **Clique em Create Web Service**
11. Aguarde 3-5 minutos (verá "Deploying...")
12. Quando terminar, copie a URL (algo como `https://finance-api-xxxxx.onrender.com`)

**Salve essa URL também!**

---

### **PASSO 3: Atualizar Frontend com URL do Backend (2 min)**

1. Volte ao Vercel
2. Clique no seu projeto `finance`
3. Vá para **Settings** (engrenagem)
4. Clique em **Environment Variables**
5. Procure por `VITE_API_URL`
6. Clique no lápis para editar
7. Mude o valor para a URL do Render (que você salvou)
   - De: `https://finance-api.render.com`
   - Para: `https://SEU-BACKEND-RENDER.onrender.com`

8. **Clique em Save**
9. Aguarde re-deployment automático (2 min)

---

## ✅ Pronto! Seu Sistema Está Online!

### **URLs Finais:**

```
Frontend: https://seu-frontend.vercel.app
Backend: https://seu-backend.onrender.com
Banco: Supabase (gerenciado)
```

---

## 🧪 Testar se Funcionou

### **Teste 1: Acessar Frontend**
1. Abra a URL do Vercel
2. Você deve ver a tela de login
3. Se carregar, está funcionando! ✅

### **Teste 2: Fazer Login**
1. Email: `admin@financeiro.local`
2. Senha: `SenhaTemporaria123!`
3. Se entrar, backend conectou! ✅

### **Teste 3: Alterar Senha**
1. Vá para Settings/Configurações
2. Altere a senha
3. Se conseguir, tudo funciona! ✅

---

## 🚨 Se Algo Não Funcionar

### Erro: Frontend carrega mas login não funciona

**Solução:**
1. Abra DevTools do navegador (F12)
2. Vá para **Console**
3. Procure por erros vermelhos
4. Se disser "CORS blocked", volte ao Render e verifique `CORS_ORIGINS`

### Erro: Página em branco

**Solução:**
1. Vercel → Settings → Environment Variables
2. Verifique se `VITE_API_URL` está correto
3. Rode novo deployment (clique Deploy)

### Erro: Banco de dados não conecta

**Solução:**
1. Render → seu projeto
2. Clique em **Logs**
3. Procure por erro de conexão
4. Verifique `DATABASE_URL` no Render

---

## 📞 Resumo Final

| Item | URL | Status |
|------|-----|--------|
| Frontend | `https://seu-frontend.vercel.app` | ✅ |
| Backend | `https://seu-backend.onrender.com` | ✅ |
| Banco | Supabase | ✅ |
| GitHub | https://github.com/mgutoas-svg/finance | ✅ |

---

## 🎉 Parabéns! 

Seu sistema de finanças pessoais está **ONLINE**! 

Agora você pode:
1. ✅ Fazer login
2. ✅ Importar dados
3. ✅ Ver dashboard
4. ✅ Acompanhar gastos
5. ✅ Criar metas

**Aproveite!** 🚀

---

## 📚 Próximos Passos (Opcional)

- [ ] Alterar senha padrão
- [ ] Importer seus dados (CSV, PDF, Excel)
- [ ] Criar suas metas financeiras
- [ ] Configurar email para recuperação de senha (opcional)
- [ ] Monitorar logs no Render

---

**Desenvolvido com ❤️ para suas finanças pessoais**

