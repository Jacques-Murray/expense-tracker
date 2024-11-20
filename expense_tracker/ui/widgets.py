"""Module containing reusable GUI widgets for the expense tracker application."""
import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox, ttk
from typing import Callable, Dict, List

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from expense_tracker.models.expense import Expense


class ExpenseForm(ttk.Frame):
    """Form widget for adding new expenses."""

    CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]

    def __init__(
        self,
        parent: tk.Widget,
        on_add_expense: Callable[[Decimal, str, str], None],
    ):
        """Initialize the expense form widget.

        Args:
            parent: Parent widget
            on_add_expense: Callback for adding a new expense
        """
        super().__init__(parent)
        self._on_add_expense = on_add_expense
        self._setup_ui()

    def _setup_ui(self):
        """Set up the form UI components."""
        # Amount input
        ttk.Label(self, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(self, textvariable=self.amount_var)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category dropdown
        ttk.Label(self, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar(value=self.CATEGORIES[0])
        category_dropdown = ttk.Combobox(
            self,
            textvariable=self.category_var,
            values=self.CATEGORIES,
            state="readonly",
        )
        category_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Description input
        ttk.Label(self, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(self, textvariable=self.description_var)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        # Add button
        add_button = ttk.Button(self, text="Add Expense", command=self._add_expense)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def _add_expense(self):
        """Handle adding a new expense."""
        try:
            amount = Decimal(self.amount_var.get())
            if amount <= 0:
                raise ValueError("Amount must be positive")

            category = self.category_var.get()
            description = self.description_var.get().strip()

            if not description:
                raise ValueError("Description is required")

            self._on_add_expense(amount, category, description)
            self._clear_form()

        except (InvalidOperation, ValueError) as e:
            messagebox.showerror("Error", str(e))

    def _clear_form(self):
        """Clear all form inputs."""
        self.amount_var.set("")
        self.category_var.set(self.CATEGORIES[0])
        self.description_var.set("")
        self.amount_entry.focus()


class ExpenseList(ttk.Frame):
    """Widget for displaying and managing the list of expenses."""

    def __init__(
        self,
        parent: tk.Widget,
        on_delete_expense: Callable[[str], None],
    ):
        """Initialize the expense list widget.

        Args:
            parent: Parent widget
            on_delete_expense: Callback for deleting an expense
        """
        super().__init__(parent)
        self._on_delete_expense = on_delete_expense
        self._setup_ui()

    def _setup_ui(self):
        """Set up the list UI components."""
        columns = ("amount", "category", "description", "date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Configure columns
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("date", text="Date")

        self.tree.column("amount", width=100)
        self.tree.column("category", width=100)
        self.tree.column("description", width=200)
        self.tree.column("date", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack components
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind delete key
        self.tree.bind("<Delete>", self._delete_selected)

    def update_expenses(self, expenses: List[Expense]):
        """Update the displayed list of expenses.

        Args:
            expenses: List of expenses to display
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in expenses:
            self.tree.insert(
                "",
                "end",
                values=(
                    f"${expense.amount:.2f}",
                    expense.category,
                    expense.description,
                    expense.date.strftime("%Y-%m-%d %H:%M"),
                ),
                tags=(expense.id,),
            )

    def _delete_selected(self, event=None):
        """Handle deleting the selected expense."""
        selected_item = self.tree.selection()
        if selected_item:
            expense_id = self.tree.item(selected_item[0])["tags"][0]
            if messagebox.askyesno("Confirm Delete", "Delete this expense?"):
                self._on_delete_expense(expense_id)


class ExpenseChart(ttk.Frame):
    """Widget for displaying expense statistics charts."""

    def __init__(self, parent: tk.Widget):
        """Initialize the chart widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_chart(self, expenses: List[Expense]):
        """Update the pie chart with current expense data.

        Args:
            expenses: List of expenses to visualize
        """
        self.ax.clear()

        if not expenses:
            self.ax.text(
                0.5,
                0.5,
                "No expenses to display",
                horizontalalignment="center",
                verticalalignment="center",
            )
        else:
            # Calculate totals by category
            category_totals: Dict[str, float] = {}
            for expense in expenses:
                category_totals[expense.category] = category_totals.get(
                    expense.category, 0
                ) + float(expense.amount)

            # Create pie chart
            labels = list(category_totals.keys())
            sizes = list(category_totals.values())
            self.ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
            )
            self.ax.axis("equal")

        self.canvas.draw()
