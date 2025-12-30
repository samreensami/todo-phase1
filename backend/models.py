"""Ticket data models with Pydantic validation."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class Priority(str, Enum):
    """Ticket priority levels."""
    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"


class Status(str, Enum):
    """Ticket status values."""
    BACKLOG = "BACKLOG"
    DONE = "DONE"


class Ticket(BaseModel):
    """Ticket model with validation."""
    model_config = ConfigDict(use_enum_values=True)

    id: int = Field(..., description="Unique ticket identifier")
    title: str = Field(..., min_length=1, description="Ticket title")
    priority: Priority = Field(default=Priority.MED, description="Ticket priority")
    status: Status = Field(default=Status.BACKLOG, description="Ticket status")
