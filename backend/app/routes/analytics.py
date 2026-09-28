from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from app.database import get_db
from app import schemas, models
from app.security import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary", response_model=schemas.FinancialSummary)
async def get_financial_summary(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resumo financeiro do período"""

    # Datas padrão (últimos 30 dias)
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)

    # Query
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.transaction_date >= start_date,
        models.Transaction.transaction_date <= end_date
    ).all()

    total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
    total_expense = sum(abs(t.amount) for t in transactions if t.transaction_type == "expense")
    net_result = total_income - total_expense

    return {
        "period_start": start_date,
        "period_end": end_date,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_result": net_result,
        "transaction_count": len(transactions)
    }


@router.get("/by-category", response_model=List[schemas.CategoryAnalysis])
async def get_category_analysis(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Análise de gastos por categoria"""

    # Datas padrão
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)

    # Pegar todas as despesas
    expenses = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.transaction_type == "expense",
        models.Transaction.transaction_date >= start_date,
        models.Transaction.transaction_date <= end_date
    ).all()

    total_expenses = sum(abs(t.amount) for t in expenses)

    # Agrupar por categoria
    category_totals = {}
    for expense in expenses:
        cat_id = expense.category_id or 0
        if cat_id not in category_totals:
            category_totals[cat_id] = {
                "amount": 0,
                "count": 0,
                "category_name": "Sem categoria"
            }
        category_totals[cat_id]["amount"] += abs(expense.amount)
        category_totals[cat_id]["count"] += 1

    # Enriquecer com informações de categoria
    categories = db.query(models.Category).filter(
        models.Category.user_id == current_user.id
    ).all()

    category_map = {c.id: c for c in categories}

    # Construir resposta
    analysis = []
    for cat_id, data in category_totals.items():
        category = category_map.get(cat_id)
        category_name = category.name if category else "Sem categoria"
        ideal_pct = category.ideal_percentage if category else 0

        percentage = (data["amount"] / total_expenses * 100) if total_expenses > 0 else 0
        is_alert = percentage > (ideal_pct * 1.2) if ideal_pct > 0 else False

        analysis.append({
            "category_id": cat_id,
            "category_name": category_name,
            "total_amount": data["amount"],
            "percentage_of_total": percentage,
            "transaction_count": data["count"],
            "average_transaction": data["amount"] / data["count"],
            "is_alert": is_alert
        })

    return sorted(analysis, key=lambda x: x["total_amount"], reverse=True)


@router.get("/recommendations", response_model=List[schemas.Recommendation])
async def get_recommendations(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Gerar recomendações baseadas em análise"""

    # Datas padrão
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)

    # Análise por categoria
    category_analysis = await get_category_analysis(start_date, end_date, current_user, db)

    recommendations = []

    # Recomendar baseado em gastos elevados
    for cat_analysis in category_analysis:
        if cat_analysis["is_alert"]:
            estimated_savings = cat_analysis["total_amount"] * 0.1
            recommendations.append({
                "title": f"Reduzir gastos em {cat_analysis['category_name']}",
                "description": f"Categoria com {cat_analysis['percentage_of_total']:.1f}% do total de gastos. Potencial de economia: R$ {estimated_savings:.2f}",
                "category": cat_analysis["category_name"],
                "priority": "high",
                "estimated_savings": estimated_savings
            })

    # Recomendar acompanhamento de metas
    goals = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.status == "active"
    ).all()

    for goal in goals:
        progress_pct = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0

        if progress_pct < 30 and goal.due_date:
            days_left = (goal.due_date - datetime.utcnow()).days
            if days_left < 30:
                recommendations.append({
                    "title": f"Acelerar progresso da meta '{goal.title}'",
                    "description": f"Meta com apenas {progress_pct:.1f}% de progresso. {days_left} dias restantes.",
                    "category": "Metas",
                    "priority": "high",
                    "estimated_savings": 0
                })

    return sorted(recommendations, key=lambda x: x["priority"] == "high", reverse=True)
