# 🔗 Linkar Projeto Supabase Existente

## Seu Projeto
- **Nome**: finance-ai
- **Project ID**: ekpyjbkqniipqilindo
- **Region**: us-east-2 (Ohio)

---

## Passo 1: Obter Credenciais do Supabase

### URL do Projeto
1. Vá para https://supabase.com/dashboard/projects
2. Clique em seu projeto `finance-ai`
3. Vá para **Settings** (engrenagem, canto inferior esquerdo)
4. Clique em **API**
5. Copie a **Project URL** (será algo como `https://ekpyjbkqniipqilindo.supabase.co`)
   - Isso será: `VITE_SUPABASE_URL` (frontend) e `SUPABASE_URL` (backend)

### Chaves de Acesso
Na mesma página (**Settings** → **API**), você verá:

1. **Anon Public Key**
   - Copie e guarde (será: `VITE_SUPABASE_ANON_KEY`)
   - Seguro compartilhar no frontend

2. **Service Role Key** 
   - Copie e guarde (será: `SUPABASE_KEY` backend)
   - ⚠️ NÃO compartilhe! Só no backend

### Database Connection String
1. Vá para **Settings** → **Database**
2. Procure por **Connection Pooling** (recomendado para Render)
3. Se não estiver ativado, clique em **Session mode** e copie:
   ```
   postgresql://postgres.[projeto]:[password]@db.supabase.co:6543/postgres
   ```
   - Isso será: `DATABASE_URL` (backend)

---

## Passo 2: Executar Schema SQL

Se ainda não executou, execute o schema no seu banco:

1. Dashboard Supabase → **SQL Editor**
2. Clique em **New Query**
3. Cole o conteúdo de `database/schema.sql`
4. Clique em **▶️ Run** (play)
5. ✅ Tabelas criadas!

Para verificar:
- Vá para **Table Editor** no menu esquerdo
- Você deve ver as tabelas:
  - `users`
  - `categories`
  - `transactions`
  - `file_uploads`
  - `goals`
  - `audit_logs`

---

## Passo 3: Template de Credenciais

Copie estas credenciais do seu projeto Supabase:

```env
# SUPABASE
VITE_SUPABASE_URL=https://ekpyjbkqniipqilindo.supabase.co
VITE_SUPABASE_ANON_KEY=sua-anon-key-aqui
SUPABASE_URL=https://ekpyjbkqniipqilindo.supabase.co
SUPABASE_KEY=sua-service-role-key-aqui
DATABASE_URL=postgresql://postgres.ekpyjbkqniipqilindo:sua-senha@db.supabase.co:6543/postgres
```

---

## Próximas Etapas

1. ✅ Banco linkado
2. 📝 Atualizar `frontend/.env` com credenciais
3. 📝 Atualizar `backend/.env` com credenciais
4. 🚀 Fazer deploy no Vercel (frontend)
5. 🚀 Fazer deploy no Render (backend)

---

## Teste a Conexão

### No Backend
```bash
cd backend
python
>>> import os
>>> os.environ['DATABASE_URL']  # Deve mostrar a URL
```

### No Frontend
```bash
# Abrir DevTools (F12) no navegador
fetch('https://ekpyjbkqniipqilindo.supabase.co/rest/v1/users?select=count()', {
  headers: {
    'apikey': 'sua-anon-key'
  }
})
.then(r => r.json())
.then(console.log)
```

Se retornar dados, está funcionando! ✅

---

## Suporte

- Documentação completa: [NEXT_STEPS.md](./NEXT_STEPS.md)
- Todas as variáveis: [ENV_SETUP.md](./ENV_SETUP.md)

