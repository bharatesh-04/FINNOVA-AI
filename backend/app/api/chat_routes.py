from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.db.session import get_db
from app.models.models import Transaction
from app.schemas.schemas import AskRequest, ChatRequest
from app.services.ai_assistant import FinancialAssistant

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

assistants: dict[str, FinancialAssistant] = {}


def _get_assistant(user_id: UUID) -> FinancialAssistant:
    key = str(user_id)
    if key not in assistants:
        assistants[key] = FinancialAssistant()
    return assistants[key]


def _transaction_context(db: Session, user_id: UUID) -> list[dict]:
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.date.desc())
        .limit(100)
        .all()
    )
    return [
        {
            "id": str(transaction.id),
            "type": transaction.type,
            "amount": transaction.amount,
            "category": transaction.category,
            "merchant": transaction.merchant,
            "description": transaction.description,
        }
        for transaction in transactions
    ]


@router.post("/message", response_model=dict)
def send_message(
    data: ChatRequest,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from datetime import timezone
    assistant = _get_assistant(user_id)
    tx_data = _transaction_context(db, user_id)
    assistant.add_to_context({"transactions": tx_data})

    response = assistant.process_query(data.content, tx_data)
    return {
        "id": str(uuid4()),
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/history", response_model=list)
def get_history(user_id: UUID = Depends(get_current_user)):
    return _get_assistant(user_id).get_history()


@router.delete("/history")
def clear_history(user_id: UUID = Depends(get_current_user)):
    _get_assistant(user_id).clear_history()
    return {"message": "History cleared"}


@router.post("/ask", response_model=dict)
def ask_question(
    data: AskRequest,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assistant = _get_assistant(user_id)
    tx_data = _transaction_context(db, user_id)
    from datetime import timezone
    response = assistant.process_query(data.question, tx_data)
    return {
        "question": data.question,
        "answer": response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
