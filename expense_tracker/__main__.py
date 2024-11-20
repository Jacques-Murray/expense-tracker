"""Main entry point for the expense tracker application."""
import tkinter as tk

from expense_tracker.services.expense_manager import ExpenseManager
from expense_tracker.services.storage import JSONStorage
from expense_tracker.ui.expense_view import ExpenseView


def main():
    """Start the expense tracker application."""
    # Initialize services
    storage = JSONStorage("expenses.json")
    manager = ExpenseManager(storage)

    # Create and configure root window
    root = tk.Tk()
    root.title("Expense Tracker")

    # Create view with callbacks
    view = ExpenseView(
        root,
        on_add_expense=manager.add_expense,
        on_delete_expense=manager.delete_expense,
    )

    # Load and display initial expenses
    view.update_expenses(manager.get_expenses())

    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
