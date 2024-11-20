import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        
        # Initialize data storage
        self.data_file = "expenses.json"
        self.expenses = self.load_expenses()
        
        # Categories
        self.categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
        
        self.create_widgets()
        
    def load_expenses(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
        
    def save_expenses(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f)
            
    def create_widgets(self):
        # Create main frames
        input_frame = ttk.LabelFrame(self.root, text="Add Expense", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        display_frame = ttk.LabelFrame(self.root, text="Expenses Summary", padding="10")
        display_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Input widgets
        ttk.Label(input_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.categories)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Description:").grid(row=0, column=4, padx=5, pady=5)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(input_frame, textvariable=self.desc_var)
        self.desc_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=6, padx=5, pady=5)
        
        # Treeview for expenses
        self.tree = ttk.Treeview(display_frame, columns=("Date", "Amount", "Category", "Description"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Buttons frame
        button_frame = ttk.Frame(display_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Charts", command=self.show_charts).pack(side=tk.LEFT, padx=5)
        
        # Load existing expenses
        self.update_expense_list()
        
    def add_expense(self):
        try:
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            description = self.desc_var.get()
            
            if not category:
                messagebox.showerror("Error", "Please select a category")
                return
                
            expense = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "amount": amount,
                "category": category,
                "description": description
            }
            
            self.expenses.append(expense)
            self.save_expenses()
            self.update_expense_list()
            
            # Clear inputs
            self.amount_var.set("")
            self.category_var.set("")
            self.desc_var.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            
    def update_expense_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for expense in self.expenses:
            self.tree.insert("", "end", values=(
                expense["date"],
                f"${expense['amount']:.2f}",
                expense["category"],
                expense["description"]
            ))
            
    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            index = self.tree.index(selected_item)
            self.expenses.pop(index)
            self.save_expenses()
            self.update_expense_list()
            
    def export_to_csv(self):
        df = pd.DataFrame(self.expenses)
        df.to_csv("expenses_export.csv", index=False)
        messagebox.showinfo("Success", "Expenses exported to expenses_export.csv")
        
    def show_charts(self):
        if not self.expenses:
            messagebox.showwarning("Warning", "No expenses to display")
            return
            
        df = pd.DataFrame(self.expenses)
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Create a new window for charts
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Analysis")
        chart_window.geometry("800x600")
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Category-wise expenses (Pie Chart)
        category_sums = df.groupby('category')['amount'].sum()
        ax1.pie(category_sums, labels=category_sums.index, autopct='%1.1f%%')
        ax1.set_title('Expenses by Category')
        
        # Daily expenses (Bar Chart)
        df['date'] = pd.to_datetime(df['date']).dt.date
        daily_sums = df.groupby('date')['amount'].sum()
        daily_sums.plot(kind='bar', ax=ax2)
        ax2.set_title('Daily Expenses')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Embed the charts in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
