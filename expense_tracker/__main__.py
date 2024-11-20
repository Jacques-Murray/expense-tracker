"""
Main entry point for the expense tracker application.
"""
import tkinter as tk
import pandas as pd
from expense_tracker.models.expense import Expense
from expense_tracker.services.storage import JSONStorage
from expense_tracker.services.expense_manager import ExpenseManager
from expense_tracker.views.expense_view import ExpenseView

class ExpenseTrackerApp:
    """Main application class implementing the Controller in MVC pattern."""

    def __init__(self):
        self.root = tk.Tk()
        self.storage = JSONStorage("expenses.json")
        self.expense_manager = ExpenseManager(self.storage)
        self.view = ExpenseView(
            self.root,
            self.handle_add_expense,
            self.handle_delete_expense,
            self.handle_export
        )
        self.update_view()

    def handle_add_expense(self, amount, category, description):
        """Handle adding a new expense."""
        self.expense_manager.add_expense(amount, category, description)
        self.update_view()

    def handle_delete_expense(self, expense_id):
        """Handle deleting an expense."""
        if self.expense_manager.delete_expense(expense_id):
            self.update_view()

    def handle_export(self):
        """Handle exporting expenses to CSV."""
        expenses = self.expense_manager.get_all_expenses()
        df = pd.DataFrame([e.to_dict() for e in expenses])
        df.to_csv("expenses_export.csv", index=False)
        tk.messagebox.showinfo("Success", "Expenses exported to expenses_export.csv")

    def update_view(self):
        """Update the view with current expenses."""
        expenses = self.expense_manager.get_all_expenses()
        self.view.update_expense_list(expenses)

    def run(self):
        """Start the application."""
        self.root.mainloop()

def main():
    """Application entry point."""
    app = ExpenseTrackerApp()
    app.run()

if __name__ == "__main__":
    main()
