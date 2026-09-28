from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from app.security import hash_password, verify_password
from typing import List, Optional


# User CRUD
def create_default_user(db: Session) -> models.User:
    """Cria o usuário padrão se não existir"""
    existing = db.query(models.User).filter(
        models.User.email == "admin@financeiro.local"
    ).first()

    if existing:
        return existing

    user = models.User(
        email="admin@financeiro.local",
        hashed_password=hash_password("SenhaTemporaria123!"),
        full_name="Administrador",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User:
    user = get_user_by_id(db, user_id)
    if user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user


def change_password(db: Session, user_id: int, new_password: str) -> models.User:
    user = get_user_by_id(db, user_id)
    if user:
        user.hashed_password = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user


# Category CRUD
def create_default_categories(db: Session, user_id: int):
    """Cria categorias padrão para novo usuário"""
    default_categories = [
        {"name": "Alimentação", "ideal_percentage": 15},
        {"name": "Transporte", "ideal_percentage": 15},
        {"name": "Saúde", "ideal_percentage": 5},
        {"name": "Educação", "ideal_percentage": 10},
        {"name": "Lazer", "ideal_percentage": 10},
        {"name": "Compras", "ideal_percentage": 10},
        {"name": "Utilities", "ideal_percentage": 10},
        {"name": "Seguros", "ideal_percentage": 5},
        {"name": "Investimentos", "ideal_percentage": 10},
        {"name": "Outros", "ideal_percentage": 0},
    ]

    for cat_data in default_categories:
        existing = db.query(models.Category).filter(
            models.Category.user_id == user_id,
            models.Category.name == cat_data["name"]
        ).first()

        if not existing:
            category = models.Category(
                user_id=user_id,
                name=cat_data["name"],
                ideal_percentage=cat_data["ideal_percentage"],
                alert_percentage=cat_data["ideal_percentage"] * 1.2,
                is_custom=False
            )
            db.add(category)

    db.commit()


def get_categories(db: Session, user_id: int) -> List[models.Category]:
    return db.query(models.Category).filter(
        models.Category.user_id == user_id
    ).all()


def create_category(
    db: Session, user_id: int, category: schemas.CategoryCreate
) -> models.Category:
    db_category = models.Category(
        user_id=user_id,
        **category.dict(),
        is_custom=True
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == user_id
    ).first()

    if category:
        db.delete(category)
        db.commit()
        return True
    return False


# Transaction CRUD
def create_transaction(
    db: Session, user_id: int, transaction: schemas.TransactionCreate
) -> models.Transaction:
    db_transaction = models.Transaction(
        user_id=user_id,
        **transaction.dict(),
        source="manual"
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category_id: Optional[int] = None
) -> List[models.Transaction]:
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    )

    if start_date:
        query = query.filter(models.Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.transaction_date <= end_date)
    if category_id:
        query = query.filter(models.Transaction.category_id == category_id)

    return query.order_by(
        models.Transaction.transaction_date.desc()
    ).offset(skip).limit(limit).all()


def update_transaction(
    db: Session,
    transaction_id: int,
    user_id: int,
    transaction_update: schemas.TransactionUpdate
) -> Optional[models.Transaction]:
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()

    if transaction:
        update_data = transaction_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(transaction, field, value)
        transaction.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(transaction)

    return transaction


def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()

    if transaction:
        db.delete(transaction)
        db.commit()
        return True
    return False


# Goal CRUD
def create_goal(
    db: Session, user_id: int, goal: schemas.GoalCreate
) -> models.Goal:
    db_goal = models.Goal(
        user_id=user_id,
        **goal.dict()
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def get_goals(db: Session, user_id: int) -> List[models.Goal]:
    return db.query(models.Goal).filter(
        models.Goal.user_id == user_id
    ).all()


def update_goal(
    db: Session, goal_id: int, user_id: int, goal_update: schemas.GoalUpdate
) -> Optional[models.Goal]:
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user_id
    ).first()

    if goal:
        update_data = goal_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(goal, field, value)
        goal.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(goal)

    return goal


def delete_goal(db: Session, goal_id: int, user_id: int) -> bool:
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user_id
    ).first()

    if goal:
        db.delete(goal)
        db.commit()
        return True
    return False


# Audit Log CRUD
def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: Optional[int] = None,
    old_values: Optional[str] = None,
    new_values: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> models.AuditLog:
    log = models.AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(log)
    db.commit()
    return log
