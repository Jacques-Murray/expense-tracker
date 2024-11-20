"""Unit tests for the main expense view."""
import tkinter as tk
from decimal import Decimal
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from expense_tracker.models.expense import Expense
from expense_tracker.ui.expense_view import ExpenseView


class TestExpenseView(TestCase):
    """Test cases for the ExpenseView class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.root = tk.Tk()
        self.on_add_expense = MagicMock()
        self.on_delete_expense = MagicMock()
        self.view = ExpenseView(
            self.root,
            self.on_add_expense,
            self.on_delete_expense,
        )

    def tearDown(self):
        """Clean up after each test."""
        self.root.destroy()

    def test_initialization(self):
        """Test view initialization and widget creation."""
        # Check if main components were created
        self.assertIsNotNone(self.view.expense_form)
        self.assertIsNotNone(self.view.expense_list)
        self.assertIsNotNone(self.view.expense_chart)

        # Check window configuration
        self.assertEqual(self.root.title(), "Expense Tracker")

    @patch("expense_tracker.ui.widgets.ExpenseList.update_expenses")
    @patch("expense_tracker.ui.widgets.ExpenseChart.update_chart")
    def test_update_expenses(self, mock_update_chart, mock_update_list):
        """Test updating expenses in all components."""
        expenses = [
            Expense(
                id=1,
                amount=Decimal("50.25"),
                category="Food",
                description="Lunch",
            ),
            Expense(
                id=2,
                amount=Decimal("30.00"),
                category="Transport",
                description="Bus fare",
            ),
        ]

        self.view.update_expenses(expenses)

        # Verify that both list and chart were updated
        mock_update_list.assert_called_once_with(expenses)
        mock_update_chart.assert_called_once_with(expenses)


if __name__ == "__main__":
    main()
