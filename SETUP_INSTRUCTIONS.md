# 🚀 Instruções de Setup - Sistema de Finanças Pessoais

## Opção 1: Setup Rápido com Docker (Recomendado)

### Pré-requisitos
- Docker e Docker Compose instalados
- Git configurado

### Passo 1: Clonar repositório
```bash
git clone https://github.com/mgutoas-svg/finance.git
cd finance
```

### Passo 2: Iniciar os serviços
```bash
docker-compose up -d
```

### Passo 3: Acessar a aplicação
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

### Passo 4: Fazer login
- Email: `admin@financeiro.local`
- Senha: `SenhaTemporaria123!`

---

## Opção 2: Setup Manual (Desenvolvimento)

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Git

### Backend

```bash
# 1. Clonar e acessar o diretório
git clone https://github.com/mgutoas-svg/finance.git
cd finance/backend

# 2. Criar virtual environment
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais do PostgreSQL

# 5. Executar aplicação
uvicorn app.main:app --reload
```

A API estará em: `http://localhost:8000`

### Frontend

```bash
# 1. Acessar o diretório
cd ../frontend

# 2. Instalar dependências
npm install

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Altere VITE_API_URL para http://localhost:8000 se necessário

# 4. Executar aplicação
npm run dev
```

O Frontend estará em: `http://localhost:5173`

---

## Opção 3: Deploy em Produção

Para fazer o deploy em Vercel (Frontend) + Render (Backend) + Supabase (Database):

**Veja o arquivo [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) para instruções completas.**

---

## Verificações de Saúde

### Verificar se tudo está funcionando

```bash
# Verificar Backend
curl http://localhost:8000/health

# Verificar Banco de Dados
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@financeiro.local","password":"SenhaTemporaria123!"}'

# Frontend
Abra http://localhost:5173 no navegador
```

---

## Troubleshooting

### Erro: "Connection refused" no Backend

**Solução:**
1. Verifique se PostgreSQL está rodando
2. Verifique se a `DATABASE_URL` está correta no `.env`
3. Certifique-se que o banco existe

### Erro: "Module not found" no Frontend

**Solução:**
```bash
cd frontend
rm -rf node_modules
npm install
```

### Erro: "Port already in use"

**Solução:**
1. Para a porta 8000 (Backend):
```bash
lsof -i :8000
kill -9 <PID>
```

2. Para a porta 5173 (Frontend):
```bash
lsof -i :5173
kill -9 <PID>
```

---

## Próximos Passos

1. ✅ Setup completado
2. 📝 Altere a senha padrão (Settings → Change Password)
3. 📊 Importe seus dados (Upload arquivos CSV/PDF/Excel)
4. 🎯 Crie suas metas financeiras
5. 📈 Acompanhe seus gastos
6. 🚀 Quando pronto, faça o deploy em produção

---

## Comandos Úteis

### Docker
```bash
# Ver status dos serviços
docker-compose ps

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Reiniciar serviços
docker-compose restart

# Limpar tudo (cuidado!)
docker-compose down -v
```

### Python/Backend
```bash
# Executar migrações
alembic upgrade head

# Ver documentação Swagger
http://localhost:8000/docs

# Ver documentação ReDoc
http://localhost:8000/redoc
```

### Node/Frontend
```bash
# Build para produção
npm run build

# Preview do build
npm run preview

# Lint do código
npm run lint
```

---

## Ajuda

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs`
2. Abra uma issue no GitHub
3. Verifique a documentação completa em `docs/`

