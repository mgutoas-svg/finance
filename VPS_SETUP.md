# 🖥️ Guia Completo: VPS + Deploy - Sistema de Finanças Pessoais

## 📋 Sumário

1. Criar VPS no DigitalOcean ($5/mês)
2. Conectar via SSH
3. Instalar Docker
4. Deploy do sistema (1 comando!)
5. Testar e usar

**Total de tempo: 30 minutos**

---

## 🎯 PASSO 1: Criar VPS no DigitalOcean (10 min)

### 1.1 Criar Conta
1. Acesse https://digitalocean.com
2. Clique em **Sign Up**
3. Use seu email
4. Complete o registro
5. Adicione método de pagamento (cartão)

### 1.2 Criar um Droplet (VPS)
1. Na dashboard, clique em **Create** → **Droplets**
2. Configure:
   - **Image**: `Ubuntu 24.04 x64`
   - **Size**: `Basic $5/mo` (512MB é pouco, melhor $6/mo com 1GB)
   - **Region**: `New York` ou `São Francisco` (mais próximo do Brasil)
   - **VPC Network**: Deixe padrão
   - **Authentication**: 
     - ✅ Escolha **SSH key** (mais seguro)
     - Se não tem: gere uma SSH key (instruções abaixo)
   - **Hostname**: `finance-server`

3. Clique em **Create Droplet**
4. Aguarde 1-2 minutos até ficar "active" (verde)
5. **Copie o IP que aparece** (algo como `123.45.67.89`)

### 1.3 Gerar SSH Key (Se Não Tiver)

**No Windows PowerShell:**
```powershell
# Verificar se já tem
ls $env:USERPROFILE\.ssh\

# Se não tem, gerar
ssh-keygen -t ed25519 -C "seu-email@gmail.com"
# Pressione Enter 2x para deixar sem passphrase
```

Depois copie a chave pública:
```powershell
cat $env:USERPROFILE\.ssh\id_ed25519.pub
```

Cole em **DigitalOcean → Create → SSH Key → New SSH Key**

---

## 🔐 PASSO 2: Conectar à VPS via SSH (2 min)

**No PowerShell ou Terminal:**
```bash
ssh root@SEU_IP_AQUI
# Exemplo: ssh root@123.45.67.89
```

Se tiver problema de permissão:
```bash
icacls "$env:USERPROFILE\.ssh\id_ed25519" /inheritance:r /grant:r "$env:USERNAME`:`(F`)"
```

---

## 🐳 PASSO 3: Instalar Docker (5 min)

**Na VPS (via SSH), execute:**

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Verificar instalação
docker --version
```

---

## 📦 PASSO 4: Clonar e Configurar o Projeto (5 min)

**Na VPS:**

```bash
# Clonar repositório
git clone https://github.com/mgutoas-svg/finance.git
cd finance

# Criar arquivo docker-compose.yml para produção
cat > docker-compose.prod.yml << 'COMPOSE'
version: '3.8'

services:
  frontend:
    image: node:18-alpine
    working_dir: /app
    environment:
      VITE_API_URL: http://localhost:8000
      VITE_SUPABASE_URL: https://ekpyjbkqniinpqilindo.supabase.co
      VITE_SUPABASE_ANON_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrcHlqYmtxbmlpbnBxaWxpbmRvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAyMDk0MTAsImV4cCI6MjA5NTc4NTQxMH0.VJ0FRsQ-_R5Gus0cTER7CV4ytFlUFAx67XwBWS23_cA
    ports:
      - "3000:5173"
    volumes:
      - ./frontend:/app
    command: sh -c "npm install && npm run build && npm run preview"
    networks:
      - finance-net

  backend:
    image: python:3.11-slim
    working_dir: /app
    environment:
      DATABASE_URL: postgresql://postgres:$@Mg9586as@db.supabase.co:5432/postgres
      SECRET_KEY: finance-sistema-seguranca-chave-super-secreta-32-caracteres-minimo
      JWT_ALGORITHM: HS256
      JWT_EXPIRATION_HOURS: 24
      CORS_ORIGINS: http://localhost:3000
      DEBUG: "false"
      SUPABASE_URL: https://ekpyjbkqniinpqilindo.supabase.co
      SUPABASE_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrcHlqYmtxbmlpbnBxaWxpbmRvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDIwOTQxMCwiZXhwIjoyMDk1Nzg1NDEwfQ.sojFCLJCqv9dk8EBZI8oi8iKwGzXJuIJqslVb3CpjIo
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    command: bash -c "pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    networks:
      - finance-net
    depends_on:
      - frontend

networks:
  finance-net:
    driver: bridge
COMPOSE

# Iniciar os serviços
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🧪 PASSO 5: Verificar Acesso (2 min)

**Na VPS:**
```bash
# Ver status dos containers
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

**No seu navegador, acesse:**
- Frontend: `http://SEU_IP:3000`
- Backend API: `http://SEU_IP:8000/docs`

---

## 🌐 PASSO 6: Configurar Domínio (Opcional, 5 min)

Se tiver um domínio:

1. Acesse seu registrador (GoDaddy, Namecheap, etc)
2. Vá para DNS Settings
3. Adicione um registro **A**:
   - Name: `@` (ou `www`)
   - Value: Seu IP da VPS
   - TTL: 3600

Aguarde 5-30 minutos para propagar.

---

## 🔒 PASSO 7: Configurar HTTPS com Let's Encrypt (5 min)

**Na VPS:**

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Gerar certificado (se tiver domínio)
sudo certbot certonly --standalone -d seu-dominio.com

# Ou para teste local, usar auto-assinado:
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

---

## 📊 URLs Finais

| Serviço | URL |
|---------|-----|
| Frontend | `http://SEU_IP:3000` |
| Backend | `http://SEU_IP:8000` |
| API Docs | `http://SEU_IP:8000/docs` |
| Com Domínio | `https://seu-dominio.com` |

---

## 🧹 Comandos Úteis

```bash
# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Parar serviços
docker-compose -f docker-compose.prod.yml down

# Reiniciar
docker-compose -f docker-compose.prod.yml restart

# Remover tudo (cuidado!)
docker-compose -f docker-compose.prod.yml down -v
```

---

## 🚨 Troubleshooting

### Porta 3000 ou 8000 já em uso
```bash
# Ver o que está usando
sudo lsof -i :3000
sudo lsof -i :8000

# Matar processo
sudo kill -9 PID
```

### Backend não conecta no banco
- Verifique `DATABASE_URL` está correto
- Teste a conexão: `psql "seu_database_url"`

### Frontend não carrega
- Acesse `http://SEU_IP:3000` no navegador
- Abra DevTools (F12) → Console
- Procure por erros

---

## 💡 Dicas Importantes

1. **Sempre use SSH key**, nunca senha
2. **Faça backup regular** do banco (Supabase faz automático)
3. **Monitore logs** regularmente
4. **Atualize Docker** quando houver atualizações
5. **Use HTTPS em produção** (Let's Encrypt é grátis)

---

## 🎉 Pronto!

Seu sistema está rodando em uma **VPS dedicada** com controle total! 

Agora pode:
- ✅ Rodar múltiplos sistemas
- ✅ Personalizar conforme quiser
- ✅ Escalar quando necessário
- ✅ Economizar em relação a Vercel

**Aproveite!** 🚀

