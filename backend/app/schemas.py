from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user_id: int


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    recovery_email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    ideal_percentage: Optional[float] = 0.0
    alert_percentage: Optional[float] = 0.0


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    is_custom: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Transaction Schemas
class TransactionBase(BaseModel):
    description: str = Field(..., max_length=255)
    amount: float = Field(..., gt=0)
    transaction_date: datetime
    transaction_type: str  # 'income' ou 'expense'
    category_id: Optional[int] = None
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None
    notes: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    source: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Goal Schemas
class GoalBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    target_amount: float = Field(..., gt=0)
    frequency: str  # daily, weekly, monthly
    category_id: Optional[int] = None
    due_date: Optional[datetime] = None


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    frequency: Optional[str] = None
    status: Optional[str] = None


class GoalResponse(GoalBase):
    id: int
    user_id: int
    current_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
    progress_percentage: Optional[float] = None

    class Config:
        from_attributes = True


# File Upload Schemas
class FileUploadResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    records_imported: int
    error_message: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


# Analytics Schemas
class FinancialSummary(BaseModel):
    period_start: datetime
    period_end: datetime
    total_income: float
    total_expense: float
    net_result: float
    transaction_count: int


class CategoryAnalysis(BaseModel):
    category_id: int
    category_name: str
    total_amount: float
    percentage_of_total: float
    transaction_count: int
    average_transaction: float
    is_alert: bool  # Se ultrapassou ideal_percentage


class GoalProgress(BaseModel):
    goal_id: int
    title: str
    target_amount: float
    current_amount: float
    progress_percentage: float
    days_remaining: Optional[int] = None
    on_track: bool


class Recommendation(BaseModel):
    title: str
    description: str
    category: str
    priority: str  # high, medium, low
    estimated_savings: float


class AnalyticsResponse(BaseModel):
    summary: FinancialSummary
    by_category: List[CategoryAnalysis]
    goals: List[GoalProgress]
    recommendations: List[Recommendation]


# Report Schemas
class ReportRequest(BaseModel):
    period_start: datetime
    period_end: datetime
    include_goals: bool = True
    include_recommendations: bool = True


class ReportResponse(BaseModel):
    report_id: str
    filename: str
    generated_at: datetime
    download_url: str
