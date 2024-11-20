"""Unit tests for the CLI module."""
import io
from decimal import Decimal
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from expense_tracker.cli import (
    create_parser,
    format_expense,
    handle_add,
    handle_delete,
    handle_list,
    handle_stats,
)
from expense_tracker.models.expense import Expense


class TestCLI(TestCase):
    """Test cases for the CLI module."""

    def setUp(self):
        """Set up test environment before each test."""
        self.parser = create_parser()
        self.manager = MagicMock()

    def test_format_expense(self):
        """Test expense formatting."""
        expense = Expense(
            id=1,
            amount=Decimal("50.25"),
            category="Food",
            description="Lunch",
        )
        formatted = format_expense(expense)
        self.assertIn("[1]", formatted)
        self.assertIn("$50.25", formatted)
        self.assertIn("Food", formatted)
        self.assertIn("Lunch", formatted)

    def test_add_valid_expense(self):
        """Test adding a valid expense."""
        args = self.parser.parse_args(["add", "50.25", "Food", "Lunch"])
        expense = Expense(
            id=1,
            amount=Decimal("50.25"),
            category="Food",
            description="Lunch",
        )
        self.manager.add_expense.return_value = expense

        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            handle_add(args, self.manager)
            output = mock_stdout.getvalue()

        self.manager.add_expense.assert_called_once_with(
            amount=Decimal("50.25"),
            category="Food",
            description="Lunch",
        )
        self.assertIn("Added expense:", output)
        self.assertIn("$50.25", output)

    def test_add_invalid_amount(self):
        """Test adding an expense with invalid amount."""
        args = self.parser.parse_args(["add", "invalid", "Food", "Lunch"])

        with patch("sys.stderr", new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit):
                handle_add(args, self.manager)
            output = mock_stderr.getvalue()

        self.assertIn("Invalid amount format", output)
        self.manager.add_expense.assert_not_called()

    def test_list_expenses(self):
        """Test listing expenses."""
        args = self.parser.parse_args(["list"])
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
        self.manager.get_expenses.return_value = expenses

        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            handle_list(args, self.manager)
            output = mock_stdout.getvalue()

        self.assertIn("$50.25", output)
        self.assertIn("$30.00", output)
        self.assertIn("Total: $80.25", output)

    def test_list_expenses_with_category_filter(self):
        """Test listing expenses with category filter."""
        args = self.parser.parse_args(["list", "--category", "Food"])
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
        self.manager.get_expenses.return_value = expenses

        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            handle_list(args, self.manager)
            output = mock_stdout.getvalue()

        self.assertIn("$50.25", output)
        self.assertNotIn("$30.00", output)
        self.assertIn("Total: $50.25", output)

    def test_delete_expense(self):
        """Test deleting an expense."""
        args = self.parser.parse_args(["delete", "1"])

        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            handle_delete(args, self.manager)
            output = mock_stdout.getvalue()

        self.manager.delete_expense.assert_called_once_with(1)
        self.assertIn("Deleted expense with ID: 1", output)

    def test_delete_nonexistent_expense(self):
        """Test deleting a nonexistent expense."""
        args = self.parser.parse_args(["delete", "999"])
        self.manager.delete_expense.side_effect = KeyError()

        with patch("sys.stderr", new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit):
                handle_delete(args, self.manager)
            output = mock_stderr.getvalue()

        self.assertIn("No expense found with ID 999", output)

    def test_stats(self):
        """Test viewing expense statistics."""
        args = self.parser.parse_args(["stats"])
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
        self.manager.get_expenses.return_value = expenses

        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            handle_stats(args, self.manager)
            output = mock_stdout.getvalue()

        self.assertIn("Total expenses: $80.25", output)
        self.assertIn("Food: $50.25", output)
        self.assertIn("Transport: $30.00", output)
        self.assertIn("62.6%", output)  # Food percentage
        self.assertIn("37.4%", output)  # Transport percentage


if __name__ == "__main__":
    main()
