"""Main view class for the expense tracker UI, coordinating all components."""
import tkinter as tk
from decimal import Decimal
from typing import Callable, List

from expense_tracker.models.expense import Expense
from expense_tracker.ui.widgets import ExpenseChart, ExpenseForm, ExpenseList


class ExpenseView:
    """Main view class coordinating all UI components."""

    def __init__(
        self,
        root: tk.Tk,
        on_add_expense: Callable[[Decimal, str, str], None],
        on_delete_expense: Callable[[str], None],
    ):
        """Initialize the main view.

        Args:
            root: Root Tkinter window
            on_add_expense: Callback for adding a new expense
            on_delete_expense: Callback for deleting an expense
        """
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")

        # Create main container with padding
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        # Create and arrange widgets
        self._setup_ui(on_add_expense, on_delete_expense)

    def _setup_ui(
        self,
        on_add_expense: Callable[[Decimal, str, str], None],
        on_delete_expense: Callable[[str], None],
    ):
        """Set up the main UI layout.

        Args:
            on_add_expense: Callback for adding a new expense
            on_delete_expense: Callback for deleting an expense
        """
        # Left panel: Form and List
        left_panel = tk.Frame(self.main_frame)
        left_panel.pack(side="left", fill="both", expand=True)

        # Expense form
        self.expense_form = ExpenseForm(left_panel, on_add_expense)
        self.expense_form.pack(fill="x", padx=5, pady=5)

        # Expense list
        self.expense_list = ExpenseList(left_panel, on_delete_expense)
        self.expense_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Right panel: Chart
        right_panel = tk.Frame(self.main_frame)
        right_panel.pack(side="right", fill="both")

        # Expense chart
        self.expense_chart = ExpenseChart(right_panel)
        self.expense_chart.pack(fill="both", expand=True, padx=5, pady=5)

    def update_expenses(self, expenses: List[Expense]):
        """Update all UI components with new expense data.

        Args:
            expenses: List of expenses to display
        """
        self.expense_list.update_expenses(expenses)
        self.expense_chart.update_chart(expenses)
