.PHONY: help setup dev up down logs clean lint test deploy

help:
	@echo "Gestão Financeira - Comandos Disponíveis"
	@echo ""
	@echo "Setup:"
	@echo "  make setup       - Configurar ambiente (cria .env files)"
	@echo "  make install     - Instalar dependências"
	@echo ""
	@echo "Desenvolvimento:"
	@echo "  make dev         - Iniciar serviços em desenvolvimento"
	@echo "  make up          - Iniciar containers Docker"
	@echo "  make down        - Parar containers Docker"
	@echo "  make restart     - Reiniciar containers"
	@echo ""
	@echo "Monitoramento:"
	@echo "  make logs        - Ver logs de todos os serviços"
	@echo "  make logs-back   - Ver logs do backend"
	@echo "  make logs-front  - Ver logs do frontend"
	@echo ""
	@echo "Qualidade:"
	@echo "  make lint        - Rodar linter"
	@echo "  make test        - Rodar testes"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       - Remover volumes e containers"
	@echo "  make clean-all   - Limpar tudo (⚠️ apaga dados)"

setup:
	@echo "Configurando projeto..."
	@cp backend/.env.example backend/.env
	@cp frontend/.env.example frontend/.env
	@echo "✓ Arquivos .env criados"
	@echo "⚠️  Edite os arquivos .env antes de iniciar"

install:
	@echo "Instalando dependências..."
	@cd backend && pip install -r requirements.txt
	@cd frontend && npm install
	@echo "✓ Dependências instaladas"

dev:
	@echo "Iniciando desenvolvimento (sem Docker)..."
	@echo "Backend (Terminal 1): make dev-back"
	@echo "Frontend (Terminal 2): make dev-front"

dev-back:
	@cd backend && uvicorn app.main:app --reload

dev-front:
	@cd frontend && npm run dev

up:
	docker-compose up -d
	@echo "✓ Containers iniciados"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000"

down:
	docker-compose down
	@echo "✓ Containers parados"

restart:
	docker-compose restart
	@echo "✓ Containers reiniciados"

logs:
	docker-compose logs -f

logs-back:
	docker-compose logs -f backend

logs-front:
	docker-compose logs -f frontend

db-shell:
	docker exec -it financeiro_db psql -U financeiro_user -d financeiro_db

lint:
	@echo "Executando linter..."
	@cd backend && pylint app/
	@cd frontend && npm run lint

test:
	@echo "Executando testes..."
	@cd backend && pytest
	@cd frontend && npm run test

clean:
	docker-compose down -v
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	@echo "✓ Containers e cache removidos"

clean-all: clean
	rm -rf backend/.env
	rm -rf frontend/.env
	rm -rf backend/venv
	rm -rf frontend/node_modules
	@echo "⚠️  Projeto limpo completamente"

build:
	docker-compose build
	@echo "✓ Containers construídos"

.env-check:
	@if [ ! -f backend/.env ]; then \
		echo "⚠️  backend/.env não encontrado. Execute: make setup"; \
		exit 1; \
	fi
