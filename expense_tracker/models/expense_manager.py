"""
Module for managing expenses, including CRUD operations and analysis.
"""
import json
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional

from .expense import Expense


class ExpenseManager:
    """Manages expense operations including storage, retrieval, and analysis."""

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize ExpenseManager with optional storage path."""
        if storage_path is None:
            storage_path = os.path.join(os.path.expanduser("~"), ".expense_tracker")
        self.storage_path = Path(storage_path)
        self.expenses_file = self.storage_path / "expenses.json"
        self._ensure_storage_exists()
        self.expenses: List[Expense] = self._load_expenses()

    def _ensure_storage_exists(self) -> None:
        """Ensure storage directory and files exist."""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        if not self.expenses_file.exists():
            self.expenses_file.write_text("[]")

    def _load_expenses(self) -> List[Expense]:
        """Load expenses from storage."""
        try:
            data = json.loads(self.expenses_file.read_text())
            return [Expense.from_dict(expense_data) for expense_data in data]
        except Exception:
            return []

    def _save_expenses(self) -> None:
        """Save expenses to storage."""
        data = [expense.to_dict() for expense in self.expenses]
        self.expenses_file.write_text(json.dumps(data, indent=2))

    def add_expense(self, expense: Expense) -> None:
        """Add a new expense."""
        if expense.id is None:
            expense.id = str(len(self.expenses))
        self.expenses.append(expense)
        self._save_expenses()

    def get_expense(self, expense_id: str) -> Optional[Expense]:
        """Get expense by ID."""
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    def update_expense(self, expense_id: str, updated_expense: Expense) -> bool:
        """Update an existing expense."""
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                updated_expense.id = expense_id
                self.expenses[i] = updated_expense
                self._save_expenses()
                return True
        return False

    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense by ID."""
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                del self.expenses[i]
                self._save_expenses()
                return True
        return False

    def get_expenses(self) -> List[Expense]:
        """Get all expenses (alias for get_all_expenses)."""
        return self.get_all_expenses()

    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses."""
        return sorted(self.expenses, key=lambda x: x.date, reverse=True)

    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """Get expenses filtered by category."""
        return [
            expense
            for expense in self.expenses
            if expense.category.lower() == category.lower()
        ]

    def get_total_expenses(self) -> Decimal:
        """Get total of all expenses."""
        return sum((expense.amount for expense in self.expenses), Decimal("0"))

    def get_category_totals(self) -> Dict[str, Decimal]:
        """Get total expenses by category."""
        totals: Dict[str, Decimal] = {}
        for expense in self.expenses:
            totals[expense.category] = totals.get(expense.category, Decimal('0')) + expense.amount
        return totals

    def get_expenses_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Expense]:
        """Get expenses within a date range."""
        return [
            expense
            for expense in self.expenses
            if start_date <= expense.date <= end_date
        ]

    def get_monthly_expenses(self, year: int, month: int) -> List[Expense]:
        """Get expenses for a specific month."""
        return [
            expense
            for expense in self.expenses
            if expense.date.year == year and expense.date.month == month
        ]

    def get_monthly_total(self, year: int, month: int) -> Decimal:
        """Get total expenses for a specific month."""
        monthly_expenses = self.get_monthly_expenses(year, month)
        return sum((expense.amount for expense in monthly_expenses), Decimal("0"))
