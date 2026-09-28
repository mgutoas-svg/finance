# ⚡ Quick Start - 5 Minutos

## Início Rápido com Docker

```bash
# 1. Clone o repositório
git clone seu-repositorio-url
cd gestao-financeira

# 2. Inicie os containers
docker-compose up -d

# 3. Aguarde 30 segundos
sleep 30

# 4. Acesse
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

## Login Padrão

**Email**: `admin@financeiro.local`  
**Senha**: `SenhaTemporaria123!`

⚠️ **Altere a senha no primeiro acesso!**

---

## Sem Docker? Manual Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou: venv\Scripts\activate (Windows)
pip install -r requirements.txt
cp .env.example .env

# Edite .env com DATABASE_URL do Supabase

uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env

# Edite .env com VITE_API_URL=http://localhost:8000

npm run dev
```

---

## Verificar Instalação

### Backend está rodando?
```bash
curl http://localhost:8000/health
```

Resposta esperada:
```json
{"status":"ok","timestamp":"...","version":"1.0.0"}
```

### Frontend está rodando?
Acesse: http://localhost:5173

Deve carregar a página de login

---

## Próximos Passos

1. **Altere a senha padrão**
   - Clique em Configurações → Senha

2. **Configure email de recuperação**
   - Clique em Configurações → Email de Recuperação

3. **Importe dados**
   - Vá para Transações → Importar
   - Suporta CSV, PDF, Excel

4. **Crie suas categorias customizadas**
   - Vá para Categorias → Nova Categoria

5. **Defina metas**
   - Vá para Metas → Nova Meta

---

## Troubleshooting Rápido

### Erro: "Cannot connect to database"
```bash
# Verificar se Postgres está rodando
docker ps

# Se não houver container db, reinicie:
docker-compose down
docker-compose up -d
```

### Erro: "Port already in use"
```bash
# Trocar portas no docker-compose.yml
# Ex: "5433:5432" para porta 5433
# Depois: docker-compose down && docker-compose up -d
```

### Frontend não conecta ao backend
```bash
# Verificar VITE_API_URL em frontend/.env
# Deve ser http://localhost:8000 (ou seu IP/domínio)
```

---

## Estrutura de Pastas

```
gestao-financeira/
├── backend/           ← API Python
├── frontend/          ← Interface React
├── database/          ← Schema SQL
├── docs/              ← Documentação
└── docker-compose.yml ← Configuração Docker
```

---

## Comandos Úteis

```bash
# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Parar serviços
docker-compose down

# Reiniciar
docker-compose restart backend

# Limpar volumes (⚠️ apaga dados)
docker-compose down -v

# Acessar banco de dados
docker exec -it financeiro_db psql -U financeiro_user -d financeiro_db
```

---

## Suporte Rápido

| Problema | Solução |
|----------|---------|
| Porta ocupada | Trocar porta no docker-compose.yml |
| DB não inicializa | `docker-compose logs db` |
| Auth falha | Verificar DATABASE_URL |
| CORS error | Verificar CORS_ORIGINS no .env |

---

## Próximo: Deploy

Quando estiver pronto para publicar:
1. Leia `docs/DEPLOYMENT.md`
2. Configure Supabase
3. Deploy no Vercel (frontend)
4. Deploy no Render (backend)

---

**Dúvidas?** Veja a documentação completa em `README.md` ou `docs/DEPLOYMENT.md`
