from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app import schemas, models, crud
from app.security import get_current_user

router = APIRouter(prefix="/api/goals", tags=["goals"])


@router.get("", response_model=List[schemas.GoalResponse])
async def list_goals(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todas as metas do usuário"""
    goals = crud.get_goals(db, current_user.id)

    # Adicionar progresso percentual
    for goal in goals:
        if goal.target_amount > 0:
            goal.progress_percentage = (goal.current_amount / goal.target_amount) * 100
        else:
            goal.progress_percentage = 0

    return goals


@router.post("", response_model=schemas.GoalResponse)
async def create_goal(
    goal: schemas.GoalCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar nova meta financeira"""
    db_goal = crud.create_goal(db, current_user.id, goal)

    if db_goal.target_amount > 0:
        db_goal.progress_percentage = (db_goal.current_amount / db_goal.target_amount) * 100
    else:
        db_goal.progress_percentage = 0

    return db_goal


@router.put("/{goal_id}", response_model=schemas.GoalResponse)
async def update_goal(
    goal_id: int,
    goal_update: schemas.GoalUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualizar meta financeira"""
    goal = crud.update_goal(db, goal_id, current_user.id, goal_update)

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meta não encontrada"
        )

    if goal.target_amount > 0:
        goal.progress_percentage = (goal.current_amount / goal.target_amount) * 100
    else:
        goal.progress_percentage = 0

    return goal


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar meta"""
    deleted = crud.delete_goal(db, goal_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meta não encontrada"
        )

    return {"message": "Meta deletada com sucesso"}
