# ✅ Checklist de Deploy - Sistema de Finanças Pessoais

## Fase 1: Preparação

### GitHub
- [ ] Repositório criado e pushado para GitHub
- [ ] Repositório público ou acesso configurado
- [ ] Branch principal é `main`
- [ ] `.gitignore` está correto (sem .env, node_modules, venv)

### Dependências
- [ ] `requirements.txt` está atualizado (backend)
- [ ] `package.json` está atualizado (frontend)
- [ ] Dockerfile do backend está correto
- [ ] docker-compose.yml testado localmente

---

## Fase 2: Supabase Setup

### Criar Projeto
- [ ] Conta Supabase criada (supabase.com)
- [ ] Projeto criado (nome: `finance-personal`)
- [ ] Região selecionada (próxima ao seu local)
- [ ] Senha do banco salva em local seguro

### Configurar Banco
- [ ] Schema SQL executado no SQL Editor
- [ ] Tabelas criadas com sucesso:
  - [ ] `users`
  - [ ] `categories`
  - [ ] `transactions`
  - [ ] `file_uploads`
  - [ ] `goals`
  - [ ] `audit_logs`
- [ ] Índices criados
- [ ] Usuário padrão criado (admin@financeiro.local)

### Obter Credenciais
- [ ] Project URL copiado (VITE_SUPABASE_URL)
- [ ] Anon Public Key copiado (VITE_SUPABASE_ANON_KEY)
- [ ] Service Role Key copiado (SUPABASE_SERVICE_ROLE_KEY)
- [ ] Connection String copiada (DATABASE_URL)
- [ ] Credenciais salvas em local seguro

### Testes Supabase
- [ ] Conexão de teste bem-sucedida
- [ ] Tabelas visíveis no dashboard
- [ ] Dados de exemplo inseridos e consultados

---

## Fase 3: Deploy Frontend (Vercel)

### Conectar Vercel
- [ ] Conta Vercel criada (vercel.com)
- [ ] Repositório GitHub conectado
- [ ] Projeto criado no Vercel
- [ ] Deploy automático ativado

### Configurar Variáveis
- [ ] `VITE_API_URL` definida (será atualizada depois)
- [ ] `VITE_SUPABASE_URL` definida
- [ ] `VITE_SUPABASE_ANON_KEY` definida
- [ ] Variáveis sincronizadas com Settings → Environment

### Testar Deploy
- [ ] Build bem-sucedido no Vercel
- [ ] Preview URL acessível
- [ ] Frontend carrega sem erros
- [ ] Styling (TailwindCSS) aplicado corretamente

### Nota
- [ ] Anotar URL do frontend (ex: `https://finance-personal.vercel.app`)

---

## Fase 4: Deploy Backend (Render)

### Conectar Render
- [ ] Conta Render criada (render.com)
- [ ] Repositório GitHub conectado
- [ ] Web Service criado
- [ ] Deploy automático ativado

### Configurar Variáveis
- [ ] `DATABASE_URL` definida (URL do Supabase)
- [ ] `SECRET_KEY` gerada (32+ caracteres aleatórios)
- [ ] `JWT_ALGORITHM` = `HS256`
- [ ] `JWT_EXPIRATION_HOURS` = `24`
- [ ] `CORS_ORIGINS` definida com URL do Vercel
- [ ] `SUPABASE_URL` definida
- [ ] `SUPABASE_KEY` definida
- [ ] Email/SMTP configurado (opcional)
- [ ] Todas as variáveis em `Environment`

### Testar Deploy
- [ ] Build bem-sucedido no Render
- [ ] Serviço online e ativo
- [ ] Logs mostram "Uvicorn running"
- [ ] Health check OK

### Nota
- [ ] Anotar URL do backend (ex: `https://finance-api.render.com`)

---

## Fase 5: Integração Frontend-Backend

### Atualizar URLs
- [ ] URL do backend atualizada no Vercel
- [ ] Re-deployment automático do frontend
- [ ] CORS configurado corretamente

### Testar Autenticação
```bash
curl -X POST https://finance-api.render.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@financeiro.local","password":"SenhaTemporaria123!"}'
```
- [ ] Retorna token JWT
- [ ] Não há erro 403 CORS

### Testar Frontend-Backend
- [ ] Acessar frontend
- [ ] Fazer login com admin@financeiro.local
- [ ] Ver dashboard
- [ ] Não há erros no Console (F12)
- [ ] Requisições para API funcionam

---

## Fase 6: Testes de Produção

### Funcionalidades Críticas
- [ ] **Autenticação**
  - [ ] Login funciona
  - [ ] Logout funciona
  - [ ] Token persiste
  - [ ] Refresh token funciona

- [ ] **Dashboard**
  - [ ] Dados carregam
  - [ ] Gráficos renderizam
  - [ ] Resumo financeiro correto

- [ ] **Transações**
  - [ ] Criar transação
  - [ ] Listar transações
  - [ ] Editar transação
  - [ ] Deletar transação

- [ ] **Importação**
  - [ ] Upload CSV funciona
  - [ ] Upload PDF funciona
  - [ ] Upload Excel funciona
  - [ ] Dados importados aparecem no dashboard

- [ ] **Metas**
  - [ ] Criar meta
  - [ ] Editar meta
  - [ ] Ver progresso
  - [ ] Marcar como concluída

- [ ] **Relatórios**
  - [ ] Gerar PDF funciona
  - [ ] Download funciona
  - [ ] Dados corretos no PDF

### Performance
- [ ] Tempo de carregamento < 3s
- [ ] Sem erros 500
- [ ] Sem timeouts

### Segurança
- [ ] HTTPS em produção
- [ ] CORS configurado corretamente
- [ ] Headers de segurança presentes
- [ ] Sem dados sensíveis expostos

---

## Fase 7: Monitoramento

### Configurar Alertas
- [ ] Alertas de erro no Vercel ativados
- [ ] Alertas de erro no Render ativados
- [ ] Alertas de uptime configurados

### Backup
- [ ] Backup automático do Supabase ativado
- [ ] Verificar agendamento de backups
- [ ] Testes de restauração de backup

### Logs
- [ ] Logs do Vercel acessíveis
- [ ] Logs do Render acessíveis
- [ ] Logs do Supabase acessíveis

---

## Fase 8: Pós-Deploy

### Documentação
- [ ] README atualizado com links reais
- [ ] Guia de deploy preenchido com URLs reais
- [ ] Documentação da API atualizada
- [ ] Troubleshooting documentado

### Manutenção
- [ ] Plano de atualização definido
- [ ] Política de backup definida
- [ ] Contato de suporte definido

### Comunicação
- [ ] URL da aplicação compartilhada com stakeholders
- [ ] Credenciais compartilhadas com segurança
- [ ] Tutorial de uso enviado

---

## URLs Finais

| Serviço | URL | Status |
|---------|-----|--------|
| Frontend | `https://finance-personal.vercel.app` | ☐ |
| Backend API | `https://finance-api.render.com` | ☐ |
| Supabase Dashboard | `https://supabase.com/dashboard/projects` | ☐ |
| GitHub Repo | `https://github.com/mgutoas-svg/finance` | ☐ |

---

## Notas Importantes

- [ ] Senha padrão deve ser alterada no primeiro login
- [ ] Chaves secretas devem ser regeneradas periodicamente
- [ ] Backups devem ser testados regularmente
- [ ] Logs devem ser monitorados diariamente (primeiras 2 semanas)

---

## Suporte

Se encontrar problemas em qualquer fase:
1. Consulte o `DEPLOYMENT_GUIDE.md`
2. Verifique os logs do serviço
3. Abra uma issue no GitHub
4. Contacte o suporte dos serviços (Vercel, Render, Supabase)

**Data do Deploy:** _______________

**Responsável:** _______________

**Status Final:** [ ] ✅ Pronto para Produção

