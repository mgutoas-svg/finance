from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, models, crud
from app.security import get_current_user

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=List[schemas.CategoryResponse])
async def list_categories(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todas as categorias do usuário"""
    return crud.get_categories(db, current_user.id)


@router.post("", response_model=schemas.CategoryResponse)
async def create_category(
    category: schemas.CategoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar nova categoria personalizada"""
    return crud.create_category(db, current_user.id, category)


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar categoria"""
    # Verificar se é categoria padrão
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )

    if not category.is_custom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar categorias padrão"
        )

    deleted = crud.delete_category(db, category_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )

    return {"message": "Categoria deletada com sucesso"}
