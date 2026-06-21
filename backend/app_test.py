"""
Test FastAPI app - Mock database for demonstration
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request Models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

# Initialize FastAPI app
app = FastAPI(
    title="Finnova AI API",
    version="1.0.0",
    description="AI-powered personal finance management platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data store
MOCK_USERS = {}
MOCK_TRANSACTIONS = {}
MOCK_USER_ID = uuid4()

@app.get("/")
def root():
    return {
        "message": "Welcome to Finnova AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "✅ Running successfully!",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": "Finnova AI",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# Authentication endpoints
@app.post("/api/v1/auth/register")
def register(request: RegisterRequest):
    user_id = uuid4()
    MOCK_USERS[user_id] = {
        "id": str(user_id),
        "email": request.email,
        "name": request.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return {
        "access_token": "mock_access_token_" + str(user_id)[:8],
        "refresh_token": "mock_refresh_token_" + str(user_id)[:8],
        "user": MOCK_USERS[user_id],
    }

@app.post("/api/v1/auth/login")
def login(request: LoginRequest):
    user_id = list(MOCK_USERS.keys())[0] if MOCK_USERS else uuid4()
    return {
        "access_token": "mock_access_token_" + str(user_id)[:8],
        "refresh_token": "mock_refresh_token_" + str(user_id)[:8],
        "user": {
            "id": str(user_id),
            "email": request.email,
            "name": "Test User",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    }

@app.post("/api/v1/auth/refresh")
def refresh_token(refresh_token: str):
    return {
        "access_token": "mock_access_token_refreshed",
        "refresh_token": "mock_refresh_token_refreshed",
        "user": {
            "id": str(uuid4()),
            "email": "test@example.com",
            "name": "Test User",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    }

@app.get("/api/v1/auth/me")
def get_me():
    return {
        "id": str(MOCK_USER_ID),
        "email": "test@example.com",
        "name": "Test User",
        "role": "user",
        "avatar": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

# Transaction endpoints
@app.get("/api/v1/transactions")
def get_transactions(
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
):
    transactions = [
        {
            "id": str(uuid4()),
            "type": "expense",
            "amount": 150.00,
            "currency": "INR",
            "category": "Food",
            "merchant": "Pizza Hut",
            "description": "Lunch",
            "date": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid4()),
            "type": "income",
            "amount": 5000.00,
            "currency": "INR",
            "category": "Salary",
            "merchant": "Employer",
            "description": "Monthly salary",
            "date": datetime.now(timezone.utc).isoformat(),
        },
    ]
    return {"transactions": transactions, "count": len(transactions)}

@app.post("/api/v1/transactions")
def create_transaction(
    type: str, amount: float, category: str, merchant: str, description: str, date: str
):
    transaction_id = uuid4()
    return {
        "id": str(transaction_id),
        "type": type,
        "amount": amount,
        "currency": "INR",
        "category": category,
        "merchant": merchant,
        "description": description,
        "date": date,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/api/v1/transactions/stats")
def get_transaction_stats(startDate: Optional[str] = None, endDate: Optional[str] = None):
    return {
        "total_income": 25000.00,
        "total_expenses": 4500.00,
        "net": 20500.00,
        "transaction_count": 12,
    }

@app.get("/api/v1/transactions/dashboard-stats")
def get_dashboard_stats():
    return {
        "total_balance": 20500.00,
        "total_income": 25000.00,
        "total_expenses": 4500.00,
        "total_savings": 20500.00,
        "net_worth": 20500.00,
        "financial_health_score": 75,
    }

@app.get("/api/v1/transactions/category-breakdown")
def get_category_breakdown():
    return {
        "Food": 1500.00,
        "Transport": 800.00,
        "Entertainment": 500.00,
        "Shopping": 1200.00,
        "Others": 500.00,
    }

# Analytics endpoints
@app.get("/api/v1/analytics/financial-health")
def get_financial_health():
    return {
        "score": 75,
        "status": "excellent",
        "savings_rate": 82.0,
        "debt_ratio": 0.0,
        "income_stability": 90.0,
        "emergency_fund": 70.0,
        "budget_adherence": 85.0,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "recommendations": [
            "Review your largest spending categories weekly.",
            "Keep at least one month of expenses in emergency savings.",
        ],
    }

@app.get("/api/v1/analytics/spending-trends")
def get_spending_trends(period: str = "monthly"):
    return {
        "2026-01": {"income": 25000, "expenses": 3500},
        "2026-02": {"income": 25000, "expenses": 4200},
        "2026-03": {"income": 25000, "expenses": 3800},
        "2026-04": {"income": 25000, "expenses": 4500},
        "2026-05": {"income": 25000, "expenses": 4100},
        "2026-06": {"income": 25000, "expenses": 4200},
    }

@app.get("/api/v1/analytics/forecasts")
def get_forecasts(type: Optional[str] = None):
    return [
        {
            "id": "expense-forecast",
            "type": "expense",
            "period": "monthly",
            "predictions": [
                {"date": "2026-07", "predicted": 4300, "lower": 3800, "upper": 4800},
                {"date": "2026-08", "predicted": 4400, "lower": 3900, "upper": 4900},
            ],
            "confidence_interval": 0.8,
            "trend": "stable",
        }
    ]

@app.get("/api/v1/analytics/insights")
def get_insights():
    return [
        {
            "id": "cash-flow",
            "type": "cash_flow",
            "title": "Cash flow",
            "description": "Your current net cash flow is INR 20500.00.",
            "severity": "info",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]

# Budget endpoints
@app.get("/api/v1/budgets")
def get_budgets():
    return [
        {
            "id": str(uuid4()),
            "name": "Monthly Budget",
            "type": "total",
            "amount": 5000.00,
            "currency": "INR",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]

# Goals endpoints
@app.get("/api/v1/goals")
def get_goals():
    return [
        {
            "id": str(uuid4()),
            "name": "Save for Vacation",
            "target_amount": 50000.00,
            "current_amount": 25000.00,
            "deadline": (datetime.now(timezone.utc) + timedelta(days=180)).isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]

# Chat endpoints
@app.post("/api/v1/chat")
def chat(content: str):
    return {
        "id": str(uuid4()),
        "role": "assistant",
        "content": f"I understand you asked: '{content}'. Based on your financial data, I recommend reviewing your spending habits and setting up automatic savings.",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/api/v1/chat/history")
def get_chat_history():
    return []

# Receipt endpoints
@app.get("/api/v1/receipts")
def get_receipts():
    return []

if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting Finnova AI API Server")
    logger.info("📊 Endpoints available at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
