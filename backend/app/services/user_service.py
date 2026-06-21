from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.models import Budget, FinancialHealth, Goal, Receipt, Transaction, User
from app.schemas.schemas import BudgetCreate, BudgetUpdate, GoalCreate, GoalUpdate, ReceiptCreate, TransactionCreate, TransactionUpdate, UserCreate


class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            name=user.name,
            hashed_password=get_password_hash(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email.lower()).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        user = UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user


class TransactionService:
    @staticmethod
    def create_transaction(db: Session, user_id: UUID, transaction: TransactionCreate) -> Transaction:
        db_transaction = Transaction(
            user_id=user_id,
            **transaction.model_dump(),
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def get_transaction(db: Session, user_id: UUID, transaction_id: UUID) -> Transaction | None:
        return (
            db.query(Transaction)
            .filter(and_(Transaction.id == transaction_id, Transaction.user_id == user_id))
            .first()
        )

    @staticmethod
    def get_user_transactions(
        db: Session,
        user_id: UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        category: str | None = None,
        type_filter: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Transaction]:
        query = db.query(Transaction).filter(Transaction.user_id == user_id)

        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if category:
            query = query.filter(Transaction.category == category)
        if type_filter:
            query = query.filter(Transaction.type == type_filter)

        return query.order_by(Transaction.date.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def update_transaction(
        db: Session,
        user_id: UUID,
        transaction_id: UUID,
        payload: TransactionUpdate,
    ) -> Transaction | None:
        transaction = TransactionService.get_transaction(db, user_id, transaction_id)
        if not transaction:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(transaction, field, value)

        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def delete_transaction(db: Session, user_id: UUID, transaction_id: UUID) -> bool:
        transaction = TransactionService.get_transaction(db, user_id, transaction_id)
        if not transaction:
            return False
        db.delete(transaction)
        db.commit()
        return True

    @staticmethod
    def get_transaction_stats(
        db: Session,
        user_id: UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, float | int]:
        query = db.query(Transaction).filter(Transaction.user_id == user_id)

        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        transactions = query.all()

        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expenses = sum(t.amount for t in transactions if t.type == "expense")

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net": total_income - total_expenses,
            "transaction_count": len(transactions),
        }

    @staticmethod
    def get_category_breakdown(
        db: Session,
        user_id: UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, float]:
        query = db.query(Transaction).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.type == "expense",
            )
        )

        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        breakdown: dict[str, float] = {}
        for transaction in query.all():
            breakdown[transaction.category] = breakdown.get(transaction.category, 0) + transaction.amount

        return breakdown


class BudgetService:
    @staticmethod
    def list_budgets(db: Session, user_id: UUID) -> list[Budget]:
        return db.query(Budget).filter(Budget.user_id == user_id).order_by(Budget.end_date.asc()).all()

    @staticmethod
    def create_budget(db: Session, user_id: UUID, budget: BudgetCreate) -> Budget:
        db_budget = Budget(user_id=user_id, **budget.model_dump())
        db.add(db_budget)
        db.commit()
        db.refresh(db_budget)
        return db_budget

    @staticmethod
    def get_budget(db: Session, user_id: UUID, budget_id: UUID) -> Budget | None:
        return db.query(Budget).filter(and_(Budget.id == budget_id, Budget.user_id == user_id)).first()

    @staticmethod
    def update_budget(db: Session, user_id: UUID, budget_id: UUID, payload: BudgetUpdate) -> Budget | None:
        budget = BudgetService.get_budget(db, user_id, budget_id)
        if not budget:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(budget, field, value)
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def delete_budget(db: Session, user_id: UUID, budget_id: UUID) -> bool:
        budget = BudgetService.get_budget(db, user_id, budget_id)
        if not budget:
            return False
        db.delete(budget)
        db.commit()
        return True


class GoalService:
    @staticmethod
    def list_goals(db: Session, user_id: UUID) -> list[Goal]:
        return db.query(Goal).filter(Goal.user_id == user_id).order_by(Goal.deadline.asc()).all()

    @staticmethod
    def create_goal(db: Session, user_id: UUID, goal: GoalCreate) -> Goal:
        db_goal = Goal(user_id=user_id, **goal.model_dump())
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)
        return db_goal

    @staticmethod
    def get_goal(db: Session, user_id: UUID, goal_id: UUID) -> Goal | None:
        return db.query(Goal).filter(and_(Goal.id == goal_id, Goal.user_id == user_id)).first()

    @staticmethod
    def update_goal(db: Session, user_id: UUID, goal_id: UUID, payload: GoalUpdate) -> Goal | None:
        goal = GoalService.get_goal(db, user_id, goal_id)
        if not goal:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(goal, field, value)
        db.commit()
        db.refresh(goal)
        return goal

    @staticmethod
    def delete_goal(db: Session, user_id: UUID, goal_id: UUID) -> bool:
        goal = GoalService.get_goal(db, user_id, goal_id)
        if not goal:
            return False
        db.delete(goal)
        db.commit()
        return True


class ReceiptService:
    @staticmethod
    def create_receipt(
        db: Session,
        user_id: UUID,
        receipt: ReceiptCreate,
        extracted_data: dict[str, Any] | None = None,
        status: str = "pending",
    ) -> Receipt:
        db_receipt = Receipt(
            user_id=user_id,
            image_url=receipt.image_url,
            extracted_data=extracted_data,
            status=status,
        )
        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)
        return db_receipt

    @staticmethod
    def list_receipts(db: Session, user_id: UUID, limit: int = 10, offset: int = 0) -> list[Receipt]:
        return (
            db.query(Receipt)
            .filter(Receipt.user_id == user_id)
            .order_by(Receipt.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_receipt(db: Session, user_id: UUID, receipt_id: UUID) -> Receipt | None:
        return db.query(Receipt).filter(and_(Receipt.id == receipt_id, Receipt.user_id == user_id)).first()

    @staticmethod
    def delete_receipt(db: Session, user_id: UUID, receipt_id: UUID) -> bool:
        receipt = ReceiptService.get_receipt(db, user_id, receipt_id)
        if not receipt:
            return False
        db.delete(receipt)
        db.commit()
        return True


class AnalyticsService:
    @staticmethod
    def calculate_financial_health_score(db: Session, user_id: UUID) -> float:
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=90)

        stats = TransactionService.get_transaction_stats(db, user_id, start_date, end_date)
        total_income = float(stats["total_income"])
        total_expenses = float(stats["total_expenses"])

        if total_income == 0:
            savings_rate = 0.0
            score = 0.0
        else:
            savings_rate = (total_income - total_expenses) / total_income * 100
            score = min(100, max(0, savings_rate * 1.2))

        health = db.query(FinancialHealth).filter(FinancialHealth.user_id == user_id).first()
        if not health:
            health = FinancialHealth(user_id=user_id)

        health.score = score
        health.savings_rate = savings_rate
        health.budget_adherence = min(100, max(0, 100 - max(0, total_expenses - total_income)))
        health.last_updated = datetime.now(timezone.utc)

        db.add(health)
        db.commit()

        return score

    @staticmethod
    def get_spending_trends(db: Session, user_id: UUID, period: str = "monthly") -> dict[str, dict[str, float]]:
        end_date = datetime.now(timezone.utc)
        if period == "weekly":
            start_date = end_date - timedelta(days=90)
            date_format = "%Y-W%U"
        elif period == "yearly":
            start_date = end_date - timedelta(days=365 * 2)
            date_format = "%Y"
        else:
            start_date = end_date - timedelta(days=180)
            date_format = "%Y-%m"

        transactions = (
            db.query(Transaction)
            .filter(
                and_(
                    Transaction.user_id == user_id,
                    Transaction.date >= start_date,
                    Transaction.date <= end_date,
                )
            )
            .all()
        )

        trends: dict[str, dict[str, float]] = {}
        for transaction in transactions:
            key = transaction.date.strftime(date_format)
            trends.setdefault(key, {"income": 0.0, "expenses": 0.0})
            if transaction.type == "income":
                trends[key]["income"] += transaction.amount
            else:
                trends[key]["expenses"] += transaction.amount

        return trends
