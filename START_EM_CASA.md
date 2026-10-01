# 🏠 COMECE EM CASA - Guia Completo

## ✅ O Que Já Está Pronto

Tudo isso está no GitHub, pronto para você usar em casa:

### 📚 Documentação
- ✅ VPS_SETUP.md - Guia passo-a-passo completo
- ✅ CREDENCIAIS_CONFIGURADAS.md - Suas credenciais Supabase
- ✅ ENV_SETUP.md - Variáveis de ambiente explicadas
- ✅ DEPLOY_AGORA.md - Alternativa com Vercel/Render

### 📦 Código
- ✅ Frontend React + Vite
- ✅ Backend FastAPI
- ✅ requirements.txt (Python) - Já corrigido
- ✅ package.json (Node) - Pronto para usar
- ✅ docker-compose.yml - Para desenvolvimento local
- ✅ Arquivos .env - Com suas credenciais Supabase

### 🔑 Credenciais
- ✅ Supabase linkado (finance-ai)
- ✅ Database URL
- ✅ Anon Key
- ✅ Service Role Key
- ✅ Tudo salvo nos arquivos .env

---

## 🏃 Quando Chegar em Casa

### **Opção A: VPS (Recomendado)**

1. Acesse: https://github.com/mgutoas-svg/finance
2. Leia: **VPS_SETUP.md**
3. Siga os 7 passos
4. Em 30 min está online!

### **Opção B: Local (Teste)**

```bash
# Clone o repo
git clone https://github.com/mgutoas-svg/finance.git
cd finance

# Execute (sem Docker)
cd frontend && npm install && npm run dev
cd ../backend && pip install -r requirements.txt && python -m uvicorn app.main:app --reload
```

### **Opção C: VPS com Múltiplos Apps**

1. Crie VPS no DigitalOcean ($5-10/mês)
2. Instale Docker
3. Clone múltiplos repos
4. Use docker-compose.yml para cada um
5. Configure Nginx como reverse proxy

---

## 📋 Checklist para Casa

### Antes de Começar
- [ ] Conexão internet estável
- [ ] Editor de texto (VS Code)
- [ ] SSH instalado (Windows já tem)
- [ ] Conta GitHub (já tem)
- [ ] Cartão para VPS (se usar DigitalOcean)

### Durante o Setup
- [ ] Leia VPS_SETUP.md completamente
- [ ] Crie VPS no DigitalOcean
- [ ] Gere SSH key
- [ ] Clone o repositório
- [ ] Instale Docker
- [ ] Execute docker-compose up -d
- [ ] Acesse http://seu-ip:3000

### Depois
- [ ] Teste login (admin@financeiro.local)
- [ ] Altere senha padrão
- [ ] Importe seus dados
- [ ] Configure domínio (opcional)
- [ ] Configure HTTPS (opcional)

---

## 🎯 URLs do Projeto

```
GitHub: https://github.com/mgutoas-svg/finance
Supabase: https://supabase.com/dashboard
DigitalOcean: https://digitalocean.com
```

---

## 📞 Documentos Principais

| Arquivo | Leia Quando |
|---------|-------------|
| VPS_SETUP.md | Vai fazer deploy em VPS |
| CREDENCIAIS_CONFIGURADAS.md | Quer saber as credenciais |
| ENV_SETUP.md | Problema com variáveis de env |
| DEPLOY_AGORA.md | Quer usar Vercel/Render |
| NEXT_STEPS.md | Quick start rápido |

---

## 🚀 Fluxo Recomendado em Casa

```
1. Leia VPS_SETUP.md (10 min)
2. Crie conta DigitalOcean (5 min)
3. Crie VPS Droplet (5 min)
4. Conecte via SSH (2 min)
5. Instale Docker (5 min)
6. Clone repo (2 min)
7. Execute docker-compose (5 min)
8. Acesse localhost:3000 (1 min)
9. Faça login (1 min)
10. Aproveite! 🎉

TOTAL: ~40 minutos
```

---

## 🆘 Se Tiver Problemas

### "Não consegui conectar via SSH"
- Verifique IP da VPS
- Verifique SSH key está correta
- Tente: `ssh -vvv root@seu-ip` (debug mode)

### "Docker não instala"
- Atualize sistema: `sudo apt update && sudo apt upgrade -y`
- Execute comando inteiro do VPS_SETUP.md

### "Frontend não carrega"
- Verifique firewall (porte 3000 aberto)
- Acesse: http://seu-ip:3000 (não localhost)
- Verifique logs: `docker-compose logs frontend`

### "Backend retorna erro"
- Verifique DATABASE_URL está correto
- Teste conexão ao Supabase
- Veja logs: `docker-compose logs backend`

---

## 💡 Dicas Importantes

1. **Sempre use SSH key**, nunca senha
2. **Guarde o IP da VPS** em lugar seguro
3. **Backup regular** dos dados (Supabase faz automático)
4. **Use HTTPS** quando colocar em produção
5. **Monitore os logs** regularmente

---

## 🎉 Depois Que Estiver Online

- Você pode adicionar mais apps na mesma VPS
- Configurar múltiplos domínios
- Escalar conforme necessário
- Economizar em relação a Vercel/Render

---

## 📞 Precisa de Ajuda?

- Dúvidas durante setup? Abra issue no GitHub
- Problema técnico? Verifique troubleshooting em VPS_SETUP.md
- Quer adicionar features? Clone e customize!

---

## 🔗 Links Rápidos

- Repo: https://github.com/mgutoas-svg/finance
- DigitalOcean: https://digitalocean.com
- Supabase: https://supabase.com
- Docker: https://docker.com

---

**Boa sorte em casa! 🚀**

Quando tiver a VPS pronta, é só seguir o guia!

