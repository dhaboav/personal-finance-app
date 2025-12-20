from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Categories(SQLModel, table=True):
    """Category model representing finance categories"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    items: List["Items"] = Relationship(back_populates="categories")


class Labels(SQLModel, table=True):
    """Label model representing finance labels"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    items: List["Items"] = Relationship(back_populates="labels")


class Items(SQLModel, table=True):
    """Item model representing an item for finance record"""

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    category: Optional[int] = Field(default=None, foreign_key="categories.id")
    categories: Optional[Categories] = Relationship(back_populates="items")
    name: str
    label: Optional[int] = Field(default=None, foreign_key="labels.id")
    labels: Optional[Labels] = Relationship(back_populates="items")
    total: int
