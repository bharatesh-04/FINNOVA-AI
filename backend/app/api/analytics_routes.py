from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.db.session import get_db
from app.models.models import Transaction
from app.services.user_service import AnalyticsService, TransactionService

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/financial-health", response_model=dict)
def get_financial_health(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    score = AnalyticsService.calculate_financial_health_score(db, user_id)

    return {
        "score": score,
        "status": "excellent" if score >= 76 else "good" if score >= 51 else "fair" if score >= 26 else "poor",
        "savings_rate": 0.0,
        "debt_ratio": 0.0,
        "income_stability": 0.0,
        "emergency_fund": 0.0,
        "budget_adherence": 0.0,
        "last_updated": datetime.now(timezone.utc),
        "recommendations": [
            "Add income and expense transactions to unlock personalized recommendations."
        ] if score == 0 else [
            "Review your largest spending categories weekly.",
            "Keep at least one month of expenses in emergency savings.",
        ],
    }


@router.get("/spending-trends", response_model=dict)
def get_spending_trends(
    user_id: UUID = Depends(get_current_user),
    period: str = Query("monthly", pattern="^(weekly|monthly|yearly)$"),
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_spending_trends(db, user_id, period)


@router.get("/forecasts", response_model=list)
def get_forecasts(
    user_id: UUID = Depends(get_current_user),
    type: str | None = None,
    db: Session = Depends(get_db),
):
    trends = AnalyticsService.get_spending_trends(db, user_id, "monthly")
    if not trends:
        return []

    points = [
        {"date": period, "predicted": values.get("expenses", 0.0), "lower": 0.0, "upper": values.get("expenses", 0.0)}
        for period, values in sorted(trends.items())
    ]
    return [
        {
            "id": "expense-forecast",
            "user_id": str(user_id),
            "type": type or "expense",
            "period": "monthly",
            "predictions": points,
            "confidence_interval": 0.8,
            "trend": "stable",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]


@router.get("/insights", response_model=list)
def get_insights(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stats = TransactionService.get_transaction_stats(db, user_id)
    if stats["transaction_count"] == 0:
        return [
            {
                "id": "getting-started",
                "user_id": str(user_id),
                "type": "empty_state",
                "title": "Add your first transaction",
                "description": "Insights will improve once you add income and expenses.",
                "severity": "info",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ]

    return [
        {
            "id": "cash-flow",
            "user_id": str(user_id),
            "type": "cash_flow",
            "title": "Cash flow",
            "description": f"Your current net cash flow is INR {stats['net']:.2f}.",
            "severity": "info" if stats["net"] >= 0 else "warning",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]


@router.get("/subscriptions", response_model=list)
def get_subscriptions(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id, Transaction.is_recurring.is_(True))
        .order_by(Transaction.date.desc())
        .all()
    )
    return [
        {
            "id": str(transaction.id),
            "name": transaction.merchant or transaction.description,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "frequency": transaction.recurring_frequency or "monthly",
            "category": transaction.category,
            "status": "active",
            "renewal_date": transaction.date.isoformat(),
        }
        for transaction in transactions
    ]


@router.get("/fraud-alerts", response_model=list)
def get_fraud_alerts(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.date.desc())
        .limit(100)
        .all()
    )

    seen: set[tuple[float, str | None, str]] = set()
    alerts = []
    for transaction in transactions:
        key = (round(transaction.amount, 2), transaction.merchant, transaction.category)
        if key in seen:
            alerts.append(
                {
                    "id": str(transaction.id),
                    "type": "duplicate",
                    "message": "Possible duplicate transaction detected",
                    "severity": "warning",
                    "created_at": transaction.created_at.isoformat(),
                }
            )
        seen.add(key)

    return alerts


@router.get("/report")
def generate_report(
    user_id: UUID = Depends(get_current_user),
    format: str = Query("json", pattern="^(json|csv)$"),
    db: Session = Depends(get_db),
):
    stats = TransactionService.get_transaction_stats(db, user_id)
    if format == "csv":
        csv = "metric,value\n"
        csv += f"total_income,{stats['total_income']}\n"
        csv += f"total_expenses,{stats['total_expenses']}\n"
        csv += f"net,{stats['net']}\n"
        return Response(
            content=csv,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=finnova-report.csv"},
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "format": format,
        "stats": stats,
        "message": "PDF generation is not configured; returning report data instead.",
    }
