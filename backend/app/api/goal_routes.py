from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.db.session import get_db
from app.schemas.schemas import GoalCreate, GoalResponse, GoalUpdate
from app.services.user_service import GoalService

router = APIRouter(prefix="/api/v1/goals", tags=["goals"])


@router.get("", response_model=list[GoalResponse])
def get_goals(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return GoalService.list_goals(db, user_id)


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal: GoalCreate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return GoalService.create_goal(db, user_id, goal)


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = GoalService.get_goal(db, user_id, goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: UUID,
    goal: GoalUpdate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = GoalService.update_goal(db, user_id, goal_id, goal)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return updated


@router.delete("/{goal_id}")
def delete_goal(
    goal_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = GoalService.delete_goal(db, user_id, goal_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return {"message": "Goal deleted"}
