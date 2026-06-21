from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class UserBase(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email address')
        return v.lower()

class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    role: str
    avatar: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=1, max_length=128)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v.lower()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ChatRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)

class TransactionBase(BaseModel):
    type: str  # expense, income
    amount: float = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=10)
    category: str = Field(..., min_length=1, max_length=100)
    merchant: Optional[str] = Field(default=None, max_length=255)
    description: str = Field(..., min_length=1, max_length=500)
    date: datetime
    is_recurring: bool = False
    recurring_frequency: Optional[str] = Field(default=None, max_length=50)
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator('type')
    @classmethod
    def validate_type(cls, value):
        normalized = value.lower()
        if normalized not in {"expense", "income"}:
            raise ValueError("Transaction type must be 'expense' or 'income'")
        return normalized

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    merchant: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None

    @field_validator('type')
    @classmethod
    def validate_type(cls, value):
        if value is None:
            return value
        normalized = value.lower()
        if normalized not in {"expense", "income"}:
            raise ValueError("Transaction type must be 'expense' or 'income'")
        return normalized

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value

class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BudgetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    budget_type: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=10)
    category: Optional[str] = None
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    budget_type: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self

class BudgetResponse(BudgetBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class GoalBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    target_amount: float = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=10)
    deadline: datetime
    category: Optional[str] = None
    priority: str = "medium"

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None

    @field_validator('target_amount', 'current_amount')
    @classmethod
    def validate_amounts(cls, value):
        if value is not None and value < 0:
            raise ValueError("Amount must be zero or greater")
        return value

class GoalResponse(GoalBase):
    id: UUID
    user_id: UUID
    current_amount: float
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReceiptBase(BaseModel):
    image_url: str = Field(..., min_length=1, max_length=500)

class ReceiptCreate(ReceiptBase):
    pass

class ReceiptResponse(ReceiptBase):
    id: UUID
    user_id: UUID
    extracted_data: Optional[Dict[str, Any]] = None
    status: str
    transaction_id: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReceiptExtractResponse(BaseModel):
    merchant_name: Optional[str] = None
    amount: Optional[float] = None
    tax: Optional[float] = None
    date: Optional[str] = None
    currency: str = "INR"
    items: List[Dict[str, Any]] = Field(default_factory=list)
    category: Optional[str] = "others"
    confidence: float = 0.0

class FinancialHealthResponse(BaseModel):
    score: float
    savings_rate: float
    debt_ratio: float
    income_stability: float
    emergency_fund: float
    budget_adherence: float
    last_updated: datetime

class ChatMessageSchema(BaseModel):
    role: str  # user, assistant
    content: str
    timestamp: datetime

class PaginationParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
