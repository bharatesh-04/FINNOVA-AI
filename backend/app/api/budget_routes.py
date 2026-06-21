from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.db.session import get_db
from app.schemas.schemas import BudgetCreate, BudgetResponse, BudgetUpdate
from app.services.user_service import BudgetService

router = APIRouter(prefix="/api/v1/budgets", tags=["budgets"])


@router.get("", response_model=list[BudgetResponse])
def get_budgets(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return BudgetService.list_budgets(db, user_id)


@router.post("", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget: BudgetCreate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return BudgetService.create_budget(db, user_id, budget)


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    budget = BudgetService.get_budget(db, user_id, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: UUID,
    budget: BudgetUpdate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = BudgetService.update_budget(db, user_id, budget_id, budget)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return updated


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = BudgetService.delete_budget(db, user_id, budget_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return {"message": "Budget deleted"}
