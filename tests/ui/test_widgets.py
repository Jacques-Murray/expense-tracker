"""Unit tests for UI widgets."""
import tkinter as tk
from decimal import Decimal
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

import matplotlib.pyplot as plt

from expense_tracker.models.expense import Expense
from expense_tracker.ui.widgets import ExpenseChart, ExpenseForm, ExpenseList


class TestExpenseForm(TestCase):
    """Test cases for the ExpenseForm class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.root = tk.Tk()
        self.on_add_expense = MagicMock()
        self.form = ExpenseForm(self.root, self.on_add_expense)

    def tearDown(self):
        """Clean up after each test."""
        self.root.destroy()

    def test_initialization(self):
        """Test form initialization and widget creation."""
        self.assertIsNotNone(self.form.amount_entry)
        self.assertIsNotNone(self.form.category_var)
        self.assertIsNotNone(self.form.description_entry)

    def test_add_valid_expense(self):
        """Test submitting a valid expense."""
        # Set up test data
        self.form.amount_var.set("50.25")
        self.form.category_var.set("Food")
        self.form.description_var.set("Lunch")

        # Submit form
        self.form._add_expense()

        # Check if callback was called with correct data
        self.on_add_expense.assert_called_once_with(Decimal("50.25"), "Food", "Lunch")

        # Check if form was cleared
        self.assertEqual(self.form.amount_var.get(), "")
        self.assertEqual(self.form.category_var.get(), self.form.CATEGORIES[0])
        self.assertEqual(self.form.description_var.get(), "")

    def test_add_invalid_amount(self):
        """Test submitting an invalid amount."""
        # Set up test data with invalid amount
        self.form.amount_var.set("invalid")
        self.form.category_var.set("Food")
        self.form.description_var.set("Lunch")

        # Submit form
        self.form._add_expense()

        # Check that callback was not called
        self.on_add_expense.assert_not_called()


class TestExpenseList(TestCase):
    """Test cases for the ExpenseList class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.root = tk.Tk()
        self.on_delete_expense = MagicMock()
        self.expense_list = ExpenseList(self.root, self.on_delete_expense)

    def tearDown(self):
        """Clean up after each test."""
        self.root.destroy()

    def test_initialization(self):
        """Test list initialization."""
        self.assertIsNotNone(self.expense_list.tree)
        # Check column configuration
        columns = self.expense_list.tree["columns"]
        self.assertEqual(len(columns), 4)  # amount, category, description, date

    def test_update_expenses(self):
        """Test updating the list with expenses."""
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

        self.expense_list.update_expenses(expenses)

        # Check if items were added to tree
        items = self.expense_list.tree.get_children()
        self.assertEqual(len(items), 2)

        # Check first item values
        first_item_values = self.expense_list.tree.item(items[0])["values"]
        self.assertEqual(first_item_values[0], "$50.25")  # amount
        self.assertEqual(first_item_values[1], "Food")  # category
        self.assertEqual(first_item_values[2], "Lunch")  # description

    @patch("expense_tracker.ui.widgets.messagebox.askyesno", return_value=True)
    def test_delete_expense(self, mock_confirm):
        """Test deleting an expense."""
        # Add an expense
        expense = Expense(
            id=1,
            amount=Decimal("50.25"),
            category="Food",
            description="Lunch",
        )
        self.expense_list.update_expenses([expense])

        # Select and delete the expense
        items = self.expense_list.tree.get_children()
        self.expense_list.tree.selection_set(items[0])
        self.expense_list._delete_selected()

        # Check if callback was called with correct ID
        self.on_delete_expense.assert_called_once_with(1)


class TestExpenseChart(TestCase):
    """Test cases for the ExpenseChart class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.root = tk.Tk()
        self.chart = ExpenseChart(self.root)

    def tearDown(self):
        """Clean up after each test."""
        plt.close("all")  # Close all figures
        self.root.destroy()

    def test_update_chart_no_expenses(self):
        """Test updating chart with no expenses."""
        self.chart.update_chart([])
        # Check if text was added to chart
        self.assertTrue(len(self.chart.ax.texts) > 0)
        self.assertEqual(self.chart.ax.texts[0].get_text(), "No expenses to display")

    def test_update_chart_with_expenses(self):
        """Test updating chart with expenses."""
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

        self.chart.update_chart(expenses)
        # Check if pie chart was created
        self.assertTrue(len(self.chart.ax.patches) > 0)


if __name__ == "__main__":
    main()
