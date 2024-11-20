"""
Module containing the GUI view components for the expense tracker.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from decimal import Decimal, InvalidOperation
from expense_tracker.models.expense import Expense

class ExpenseView:
    """Main view class for the expense tracker GUI."""

    CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]

    def __init__(
        self,
        root: tk.Tk,
        on_add_expense: Callable[[Decimal, str, str], None],
        on_delete_expense: Callable[[str], None],
        on_export: Callable[[], None]
    ):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")

        self.on_add_expense = on_add_expense
        self.on_delete_expense = on_delete_expense
        self.on_export = on_export

        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Input Frame
        self.input_frame = ttk.LabelFrame(self.root, text="Add Expense", padding="10")
        
        # Input Fields
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(self.input_frame, textvariable=self.amount_var)
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            self.input_frame,
            textvariable=self.category_var,
            values=self.CATEGORIES
        )
        
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(self.input_frame, textvariable=self.desc_var)
        
        # Display Frame
        self.display_frame = ttk.LabelFrame(self.root, text="Expenses Summary", padding="10")
        
        # Treeview
        self.tree = ttk.Treeview(
            self.display_frame,
            columns=("Date", "Amount", "Category", "Description"),
            show="headings"
        )
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(
            self.display_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Buttons
        self.button_frame = ttk.Frame(self.display_frame)
        self.delete_btn = ttk.Button(
            self.button_frame,
            text="Delete Selected",
            command=self._handle_delete
        )
        self.export_btn = ttk.Button(
            self.button_frame,
            text="Export to CSV",
            command=self.on_export
        )
        self.chart_btn = ttk.Button(
            self.button_frame,
            text="Show Charts",
            command=self.show_charts
        )

    def _setup_layout(self) -> None:
        """Setup the layout of widgets."""
        # Input Frame Layout
        self.input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.input_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Description:").grid(row=0, column=4, padx=5, pady=5)
        self.desc_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(
            self.input_frame,
            text="Add Expense",
            command=self._handle_add
        ).grid(row=0, column=6, padx=5, pady=5)

        # Display Frame Layout
        self.display_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, pady=5, sticky="ns")
        
        # Button Frame Layout
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        self.chart_btn.pack(side=tk.LEFT, padx=5)

        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

    def _handle_add(self) -> None:
        """Handle adding a new expense."""
        try:
            amount = Decimal(self.amount_var.get())
            category = self.category_var.get()
            description = self.desc_var.get()

            if not category:
                messagebox.showerror("Error", "Please select a category")
                return

            self.on_add_expense(amount, category, description)
            
            # Clear inputs
            self.amount_var.set("")
            self.category_var.set("")
            self.desc_var.set("")
            
        except InvalidOperation:
            messagebox.showerror("Error", "Please enter a valid amount")

    def _handle_delete(self) -> None:
        """Handle deleting selected expense."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            item_id = self.tree.item(selected_item[0])['values'][0]  # Get ID from first column
            self.on_delete_expense(item_id)

    def update_expense_list(self, expenses: List[Expense]) -> None:
        """Update the expense list display."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for expense in expenses:
            self.tree.insert("", "end", values=(
                expense.id,
                f"${expense.amount:.2f}",
                expense.category,
                expense.description
            ))

    def show_charts(self, category_totals: dict[str, Decimal] = None) -> None:
        """Display expense charts."""
        if not category_totals:
            messagebox.showwarning("Warning", "No expenses to display")
            return

        # Create a new window for charts
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Analysis")
        chart_window.geometry("800x600")

        # Create figure with pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Convert Decimal to float for plotting
        values = [float(val) for val in category_totals.values()]
        
        ax.pie(values, labels=category_totals.keys(), autopct='%1.1f%%')
        ax.set_title('Expenses by Category')
        
        plt.tight_layout()
        
        # Embed the chart
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
