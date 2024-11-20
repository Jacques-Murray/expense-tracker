"""Command Line Interface for the Expense Tracker application."""
import argparse
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Dict, List

from expense_tracker.models.expense import Expense
from expense_tracker.models.expense_manager import ExpenseManager


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser.

    Returns:
        The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Expense Tracker - Track and manage your expenses"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add expense command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", help="Expense amount (e.g., 50.25)")
    add_parser.add_argument("category", help="Expense category")
    add_parser.add_argument("description", help="Expense description")

    # List expenses command
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument(
        "--category",
        help="Filter expenses by category",
        required=False,
    )
    list_parser.add_argument(
        "--sort",
        choices=["date", "amount", "category"],
        default="date",
        help="Sort expenses by field",
        required=False,
    )

    # Delete expense command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("id", type=int, help="ID of the expense to delete")

    # Stats command
    subparsers.add_parser("stats", help="View expense statistics")

    return parser


def format_expense(expense: Expense) -> str:
    """Format an expense for display.

    Args:
        expense: The expense to format.

    Returns:
        A formatted string representation of the expense.
    """
    return (
        f"[{expense.id}] ${expense.amount:.2f} - {expense.category} - "
        f"{expense.description} ({expense.date.strftime('%Y-%m-%d %H:%M')})"
    )


def format_expense_stats(expenses: List[Expense]) -> str:
    """Format expense statistics for display.

    Returns a string containing total expenses and breakdown by category.
    """
    if not expenses:
        return "No expenses found."

    total = sum(expense.amount for expense in expenses)
    category_totals: Dict[str, Decimal] = {}

    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = Decimal("0")
        category_totals[expense.category] += expense.amount

    lines = [f"Total expenses: ${total:.2f}"]
    for category, amount in sorted(category_totals.items()):
        percentage = (amount / total * 100) if total else Decimal("0")
        lines.append(f"{category}: ${amount:.2f} ({percentage:.1f}%)")

    return "\n".join(lines)


def handle_add(args: argparse.Namespace, manager: ExpenseManager) -> None:
    """Handle the add expense command.

    Args:
        args: Parsed command line arguments.
        manager: Expense manager instance.
    """
    try:
        amount = Decimal(args.amount)
        expense = manager.add_expense(
            amount=amount,
            date=date.today(),
            category=args.category,
            description=args.description,
        )
        print(f"Added expense: {format_expense(expense)}")

    except InvalidOperation:
        print("Error: Invalid amount format", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def handle_list(args: argparse.Namespace, manager: ExpenseManager) -> None:
    """Handle the list expenses command.

    Args:
        args: Parsed command line arguments.
        manager: The expense manager instance.
    """
    expenses = manager.get_expenses()

    # Apply category filter
    if args.category:
        expenses = [e for e in expenses if e.category == args.category]

    # Sort expenses
    if args.sort == "amount":
        expenses.sort(key=lambda x: x.amount)
    elif args.sort == "category":
        expenses.sort(key=lambda x: x.category)
    else:  # date
        expenses.sort(key=lambda x: x.date)

    if not expenses:
        print("No expenses found.")
        return

    # Print expenses
    for expense in expenses:
        print(format_expense(expense))

    # Print summary
    total = sum(e.amount for e in expenses)
    print(f"\nTotal: ${total:.2f}")


def handle_delete(args: argparse.Namespace, manager: ExpenseManager) -> None:
    """Handle the delete expense command.

    Args:
        args: Parsed command line arguments.
        manager: The expense manager instance.
    """
    try:
        manager.delete_expense(args.id)
        print(f"Deleted expense with ID: {args.id}")
    except KeyError:
        print(f"Error: No expense found with ID {args.id}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def handle_stats(args: argparse.Namespace, manager: ExpenseManager) -> None:
    """Handle the stats command.

    Args:
        args: Parsed command line arguments.
        manager: The expense manager instance.
    """
    expenses = manager.get_expenses()
    if not expenses:
        print("No expenses found.")
        return

    print(format_expense_stats(expenses))


def main() -> None:
    """Run the CLI application."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = ExpenseManager()

    # Handle commands
    if args.command == "add":
        handle_add(args, manager)
    elif args.command == "list":
        handle_list(args, manager)
    elif args.command == "delete":
        handle_delete(args, manager)
    elif args.command == "stats":
        handle_stats(args, manager)


if __name__ == "__main__":
    main()
