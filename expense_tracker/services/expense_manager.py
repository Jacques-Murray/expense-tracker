"""
Module for managing expense-related operations.
"""
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid
from expense_tracker.models.expense import Expense
from expense_tracker.services.storage import StorageInterface

class ExpenseManager:
    """Service class for managing expenses."""

    def __init__(self, storage: StorageInterface):
        self.storage = storage
        self._expenses: List[Expense] = []
        self.load_expenses()

    def load_expenses(self) -> None:
        """Load expenses from storage."""
        self._expenses = self.storage.load_expenses()

    def save_expenses(self) -> None:
        """Save expenses to storage."""
        self.storage.save_expenses(self._expenses)

    def add_expense(self, amount: Decimal, category: str, description: str) -> Expense:
        """Add a new expense."""
        expense = Expense(
            id=str(uuid.uuid4()),
            amount=amount,
            category=category,
            description=description,
            date=datetime.now()
        )
        self._expenses.append(expense)
        self.save_expenses()
        return expense

    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense by ID."""
        initial_length = len(self._expenses)
        self._expenses = [e for e in self._expenses if e.id != expense_id]
        
        if len(self._expenses) < initial_length:
            self.save_expenses()
            return True
        return False

    def get_expense(self, expense_id: str) -> Optional[Expense]:
        """Get an expense by ID."""
        return next((e for e in self._expenses if e.id == expense_id), None)

    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses."""
        return self._expenses.copy()

    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """Get expenses filtered by category."""
        return [e for e in self._expenses if e.category == category]

    def get_total_expenses(self) -> Decimal:
        """Get total amount of all expenses."""
        return sum((e.amount for e in self._expenses), Decimal('0'))

    def get_category_totals(self) -> dict[str, Decimal]:
        """Get total expenses by category."""
        totals: dict[str, Decimal] = {}
        for expense in self._expenses:
            totals[expense.category] = totals.get(expense.category, Decimal('0')) + expense.amount
        return totals
