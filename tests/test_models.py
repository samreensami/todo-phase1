"""Tests for ticket models."""

import pytest
from pydantic import ValidationError
from src.models import Ticket, Priority, Status


class TestPriorityEnum:
    """Test Priority enum."""

    def test_priority_values(self):
        """Test all priority values are valid."""
        assert Priority.LOW.value == "LOW"
        assert Priority.MED.value == "MED"
        assert Priority.HIGH.value == "HIGH"


class TestStatusEnum:
    """Test Status enum."""

    def test_status_values(self):
        """Test all status values are valid."""
        assert Status.BACKLOG.value == "BACKLOG"
        assert Status.DONE.value == "DONE"


class TestTicketModel:
    """Test Ticket model."""

    def test_ticket_creation_with_all_fields(self):
        """Test creating a ticket with all fields."""
        ticket = Ticket(
            id=1,
            title="Test ticket",
            priority=Priority.HIGH,
            status=Status.BACKLOG
        )
        assert ticket.id == 1
        assert ticket.title == "Test ticket"
        assert ticket.priority == Priority.HIGH
        assert ticket.status == Status.BACKLOG

    def test_ticket_creation_with_defaults(self):
        """Test creating a ticket with default priority and status."""
        ticket = Ticket(id=1, title="Test ticket")
        assert ticket.id == 1
        assert ticket.title == "Test ticket"
        assert ticket.priority == Priority.MED
        assert ticket.status == Status.BACKLOG

    def test_ticket_title_required(self):
        """Test that ticket title is required."""
        with pytest.raises(ValidationError):
            Ticket(id=1)

    def test_ticket_id_required(self):
        """Test that ticket id is required."""
        with pytest.raises(ValidationError):
            Ticket(title="Test ticket")

    def test_ticket_empty_title_rejected(self):
        """Test that empty title is rejected."""
        with pytest.raises(ValidationError):
            Ticket(id=1, title="")

    def test_ticket_priority_validation(self):
        """Test priority accepts valid enum values."""
        ticket = Ticket(id=1, title="Test", priority=Priority.LOW)
        assert ticket.priority == Priority.LOW

    def test_ticket_status_validation(self):
        """Test status accepts valid enum values."""
        ticket = Ticket(id=1, title="Test", status=Status.DONE)
        assert ticket.status == Status.DONE

    def test_ticket_model_config(self):
        """Test that enum values are used correctly."""
        ticket = Ticket(id=1, title="Test", priority=Priority.HIGH, status=Status.DONE)
        # Verify enums are stored properly
        assert isinstance(ticket.priority, (Priority, str))
        assert isinstance(ticket.status, (Status, str))
