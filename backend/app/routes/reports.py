from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app import schemas, models
from app.security import get_current_user
from app.services.report_generator import ReportGenerator
import os
import tempfile

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("/generate-pdf")
async def generate_pdf_report(
    report_request: schemas.ReportRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Gerar relatório em PDF"""

    # Coletar dados
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.transaction_date >= report_request.period_start,
        models.Transaction.transaction_date <= report_request.period_end
    ).all()

    goals = []
    if report_request.include_goals:
        goals = db.query(models.Goal).filter(
            models.Goal.user_id == current_user.id
        ).all()

    # Calcular consolidado
    total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
    total_expense = sum(abs(t.amount) for t in transactions if t.transaction_type == "expense")
    net_result = total_income - total_expense

    # Análise por categoria
    category_totals = {}
    categories = db.query(models.Category).filter(
        models.Category.user_id == current_user.id
    ).all()

    category_map = {c.id: c for c in categories}

    for trans in transactions:
        if trans.transaction_type == "expense":
            cat_id = trans.category_id or 0
            if cat_id not in category_totals:
                category_totals[cat_id] = 0
            category_totals[cat_id] += abs(trans.amount)

    # Gerar PDF
    generator = ReportGenerator()
    pdf_path = generator.generate_report(
        user_name=current_user.full_name or "Usuário",
        period_start=report_request.period_start,
        period_end=report_request.period_end,
        total_income=total_income,
        total_expense=total_expense,
        net_result=net_result,
        category_totals=category_totals,
        category_map=category_map,
        goals=goals if report_request.include_goals else [],
        include_recommendations=report_request.include_recommendations
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )


@router.get("/export-csv")
async def export_csv(
    start_date: datetime,
    end_date: datetime,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exportar transações em CSV"""

    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.transaction_date >= start_date,
        models.Transaction.transaction_date <= end_date
    ).order_by(models.Transaction.transaction_date.desc()).all()

    # Criar CSV
    csv_content = "Data,Tipo,Categoria,Descrição,Valor\n"

    categories = db.query(models.Category).filter(
        models.Category.user_id == current_user.id
    ).all()
    category_map = {c.id: c.name for c in categories}

    for trans in transactions:
        category_name = category_map.get(trans.category_id, "Sem categoria")
        csv_content += f'{trans.transaction_date.strftime("%d/%m/%Y")},"{trans.transaction_type}","{category_name}","{trans.description}",{trans.amount:.2f}\n'

    # Salvar temporariamente
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
        f.write(csv_content)
        temp_path = f.name

    return FileResponse(
        path=temp_path,
        media_type="text/csv",
        filename=f"transacoes_{datetime.now().strftime('%Y%m%d')}.csv"
    )
