"""
Module containing the Expense model and related functionality.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Expense:
    """
    Represents an expense entry with amount, category, and description.
    """
    amount: Decimal
    category: str
    description: str
    date: datetime = datetime.now()
    id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert expense to dictionary format for storage."""
        return {
            'id': self.id,
            'amount': str(self.amount),
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        """Create an Expense instance from dictionary data."""
        return cls(
            id=data.get('id'),
            amount=Decimal(data['amount']),
            category=data['category'],
            description=data['description'],
            date=datetime.fromisoformat(data['date'])
        )
