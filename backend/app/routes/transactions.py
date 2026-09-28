from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.database import get_db
from app import schemas, models, crud
from app.security import get_current_user
from app.services.file_processor import FileProcessor

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=List[schemas.TransactionResponse])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar lançamentos financeiros do usuário
    """
    transactions = crud.get_transactions(
        db,
        current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id
    )
    return transactions


@router.post("", response_model=schemas.TransactionResponse)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Criar novo lançamento financeiro
    """
    # Validar categoria se fornecida
    if transaction.category_id:
        category = db.query(models.Category).filter(
            models.Category.id == transaction.category_id,
            models.Category.user_id == current_user.id
        ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada"
            )

    db_transaction = crud.create_transaction(db, current_user.id, transaction)
    return db_transaction


@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualizar lançamento financeiro
    """
    transaction = crud.update_transaction(
        db, transaction_id, current_user.id, transaction_update
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )

    return transaction


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletar lançamento financeiro
    """
    deleted = crud.delete_transaction(db, transaction_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )

    return {"message": "Lançamento deletado com sucesso"}


@router.post("/import")
async def import_transactions(
    file: UploadFile = File(...),
    category_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Importar lançamentos de arquivo (CSV, PDF, Excel)
    """
    # Validar tipo de arquivo
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["csv", "pdf", "xlsx"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de arquivo não suportado. Use CSV, PDF ou Excel."
        )

    # Processar arquivo
    processor = FileProcessor()
    contents = await file.read()

    try:
        transactions_data = processor.process_file(contents, file_ext)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )

    # Registrar upload
    file_upload = models.FileUpload(
        user_id=current_user.id,
        filename=file.filename,
        file_type=file_ext,
        status="processing"
    )
    db.add(file_upload)
    db.commit()

    # Importar transações
    imported_count = 0
    errors = []

    for trans_data in transactions_data:
        try:
            # Usar categoria padrão ou fornecida
            if not trans_data.get("category_id") and category_id:
                trans_data["category_id"] = category_id

            transaction = schemas.TransactionCreate(**trans_data)
            crud.create_transaction(db, current_user.id, transaction)
            imported_count += 1
        except Exception as e:
            errors.append(str(e))

    # Atualizar status do upload
    file_upload.records_imported = imported_count
    file_upload.status = "success" if imported_count > 0 else "error"
    file_upload.error_message = "; ".join(errors) if errors else None
    db.commit()

    return {
        "file_id": file_upload.id,
        "records_imported": imported_count,
        "errors": errors
    }
