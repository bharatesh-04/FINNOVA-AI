from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.db.session import get_db
from app.schemas.schemas import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services.user_service import TransactionService

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


def _parse_datetime(value: Optional[str], field_name: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be an ISO formatted datetime",
        ) from exc


def _serialize_transaction(transaction) -> dict:
    return TransactionResponse.model_validate(transaction).model_dump(mode="json")


@router.get("", response_model=dict)
def get_transactions(
    user_id: UUID = Depends(get_current_user),
    start_date: Optional[str] = Query(None, alias="startDate"),
    end_date: Optional[str] = Query(None, alias="endDate"),
    category: Optional[str] = None,
    type_filter: Optional[str] = Query(None, alias="type"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    transactions = TransactionService.get_user_transactions(
        db,
        user_id,
        _parse_datetime(start_date, "startDate"),
        _parse_datetime(end_date, "endDate"),
        category,
        type_filter,
        limit,
        offset,
    )

    return {
        "transactions": [_serialize_transaction(transaction) for transaction in transactions],
        "count": len(transactions),
    }


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TransactionService.create_transaction(db, user_id, transaction)


@router.get("/stats", response_model=dict)
def get_transaction_stats(
    user_id: UUID = Depends(get_current_user),
    start_date: Optional[str] = Query(None, alias="startDate"),
    end_date: Optional[str] = Query(None, alias="endDate"),
    db: Session = Depends(get_db),
):
    return TransactionService.get_transaction_stats(
        db,
        user_id,
        _parse_datetime(start_date, "startDate"),
        _parse_datetime(end_date, "endDate"),
    )


@router.get("/dashboard-stats", response_model=dict)
def get_dashboard_stats(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=30)

    stats = TransactionService.get_transaction_stats(db, user_id, start_date, end_date)
    net = float(stats["net"])

    return {
        "total_balance": net,
        "total_income": stats["total_income"],
        "total_expenses": stats["total_expenses"],
        "total_savings": max(net, 0),
        "net_worth": net,
        "financial_health_score": 75,
    }


@router.get("/category-breakdown", response_model=dict)
def get_category_breakdown(
    user_id: UUID = Depends(get_current_user),
    start_date: Optional[str] = Query(None, alias="startDate"),
    end_date: Optional[str] = Query(None, alias="endDate"),
    db: Session = Depends(get_db),
):
    return TransactionService.get_category_breakdown(
        db,
        user_id,
        _parse_datetime(start_date, "startDate"),
        _parse_datetime(end_date, "endDate"),
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transaction = TransactionService.get_transaction(db, user_id, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID,
    transaction: TransactionUpdate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = TransactionService.update_transaction(db, user_id, transaction_id, transaction)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return updated


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = TransactionService.delete_transaction(db, user_id, transaction_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return {"message": "Transaction deleted"}
