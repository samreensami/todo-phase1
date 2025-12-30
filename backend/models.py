"""Ticket data models with SQLAlchemy SQLModel."""

from enum import Enum
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession


class Priority(str, Enum):
    """Ticket priority levels."""
    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"


class Status(str, Enum):
    """Ticket status values."""
    BACKLOG = "BACKLOG"
    DONE = "DONE"


class Ticket(SQLModel, table=True):
    """Ticket model with database schema."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, description="Ticket title")
    priority: Priority = Field(default=Priority.MED, description="Ticket priority")
    status: Status = Field(default=Status.BACKLOG, description="Ticket status")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        description="Last update timestamp"
    )


# Pydantic schemas for API requests/responses
class TicketBase(SQLModel):
    """Base ticket schema for requests."""
    title: str
    priority: Priority = Priority.MED
    status: Status = Status.BACKLOG


class TicketCreate(TicketBase):
    """Schema for creating tickets."""
    pass


class TicketUpdate(SQLModel):
    """Schema for updating tickets."""
    title: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None


class TicketPublic(TicketBase):
    """Public ticket schema (without sensitive fields)."""
    id: int
    created_at: datetime
    updated_at: datetime
