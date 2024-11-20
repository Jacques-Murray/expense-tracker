"""
Module for handling expense data storage operations.
"""
import json
import os
from typing import List, Protocol
from expense_tracker.models.expense import Expense

class StorageInterface(Protocol):
    """Protocol defining the interface for storage implementations."""
    def save_expenses(self, expenses: List[Expense]) -> None:
        """Save expenses to storage."""
        ...

    def load_expenses(self) -> List[Expense]:
        """Load expenses from storage."""
        ...

class JSONStorage:
    """Implementation of expense storage using JSON files."""
    
    def __init__(self, filepath: str = "expenses.json"):
        self.filepath = filepath

    def save_expenses(self, expenses: List[Expense]) -> None:
        """Save expenses to a JSON file."""
        data = [expense.to_dict() for expense in expenses]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_expenses(self) -> List[Expense]:
        """Load expenses from a JSON file."""
        if not os.path.exists(self.filepath):
            return []
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Expense.from_dict(item) for item in data]
