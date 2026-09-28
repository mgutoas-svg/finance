from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db, get_db
from app.routes import auth, transactions, categories, goals, analytics, reports
from app import crud
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Criar app
app = FastAPI(
    title="Sistema de Gestão Financeira",
    description="API para gerenciamento de finanças pessoais",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")

    response = await call_next(request)

    logger.info(f"Status: {response.status_code}")

    return response


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Inicializar banco de dados e criar usuário padrão"""
    logger.info("Iniciando aplicação...")

    try:
        # Inicializar banco
        init_db()

        # Criar usuário padrão
        db = next(get_db())
        user = crud.create_default_user(db)

        # Criar categorias padrão
        crud.create_default_categories(db, user.id)

        logger.info("Banco de dados inicializado com sucesso")
        logger.info(f"Usuário padrão criado: {user.email}")

    except Exception as e:
        logger.error(f"Erro ao inicializar: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup na desligação"""
    logger.info("Desligando aplicação...")


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# Incluir rotas
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(goals.router)
app.include_router(analytics.router)
app.include_router(reports.router)


# Tratamento de erro global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor",
            "error_type": type(exc).__name__
        }
    )


# Root
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bem-vindo ao Sistema de Gestão Financeira",
        "version": "1.0.0",
        "docs": "/docs"
    }
