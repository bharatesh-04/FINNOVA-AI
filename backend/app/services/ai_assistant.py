from datetime import datetime, timezone
from typing import Dict, List
from uuid import uuid4

import requests

from app.core.config import settings


class FinancialAssistant:
    def __init__(self):
        self.context: Dict = {}
        self.conversation_history: List[Dict] = []

    def add_to_context(self, context_data: Dict):
        self.context = context_data

    def process_query(self, query: str, user_transactions: List[Dict] | None = None) -> str:
        from datetime import timezone
        context = self._build_context(user_transactions or [])
        response = self._generate_response(query, context)

        now = datetime.now(timezone.utc).isoformat()
        self.conversation_history.append(
            {
                "id": str(uuid4()),
                "role": "user",
                "content": query,
                "timestamp": now,
            }
        )
        self.conversation_history.append(
            {
                "id": str(uuid4()),
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

        return response

    def _build_context(self, transactions: List[Dict]) -> str:
        if not transactions:
            return "No transaction data available."

        total_income = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "income")
        total_expenses = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "expense")

        context = "Here is the user's recent financial data:\n"
        context += f"Total Income: INR {total_income}\n"
        context += f"Total Expenses: INR {total_expenses}\n"
        context += f"Net: INR {total_income - total_expenses}\n"

        categories: Dict[str, float] = {}
        for transaction in transactions:
            if transaction["type"] == "expense":
                category = transaction.get("category", "others")
                categories[category] = categories.get(category, 0) + transaction["amount"]

        if categories:
            context += "\nSpending by Category:\n"
            for category, amount in sorted(categories.items(), key=lambda item: item[1], reverse=True):
                context += f"- {category}: INR {amount}\n"

        return context

    def _generate_response(self, query: str, context: str) -> str:
        prompt = f"""You are a helpful financial advisor. Answer the user's question based on their financial data.

Financial Data:
{context}

User Question: {query}

Provide a helpful, concise response."""

        try:
            response = requests.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=20,
            )
            response.raise_for_status()
            answer = response.json().get("response")
            if answer:
                return answer
        except (requests.RequestException, ValueError):
            pass

        return self._generate_fallback_response(query)

    def _generate_fallback_response(self, query: str) -> str:
        query_lower = query.lower()

        if any(word in query_lower for word in ["spend", "spent", "money"]):
            return (
                "Based on your financial data, monitor your largest spending categories "
                "and look for recurring expenses you can reduce."
            )

        if any(word in query_lower for word in ["save", "savings", "budget"]):
            return (
                "To improve savings, set a realistic budget for each major category "
                "and move planned savings before discretionary spending."
            )

        if "afford" in query_lower:
            return (
                "I can help estimate affordability from your income and spending. "
                "Tell me the amount and whether it is one-time or recurring."
            )

        return (
            "I'm here to help with spending, budgets, savings goals, and other "
            "financial questions."
        )

    def get_history(self) -> List[Dict]:
        return self.conversation_history

    def clear_history(self):
        self.conversation_history = []
