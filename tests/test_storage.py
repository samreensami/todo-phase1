"""Tests for ticket storage CRUD operations."""

import pytest
from backend.storage import TicketStorage
from backend.models import Priority, Status


class TestTicketStorage:
    """Test TicketStorage class."""

    @pytest.fixture
    def storage(self):
        """Create a fresh storage instance for each test."""
        return TicketStorage()

    # CREATE tests
    def test_create_ticket_basic(self, storage):
        """Test creating a basic ticket."""
        ticket = storage.create("Test task")
        assert ticket.id == 1
        assert ticket.title == "Test task"
        assert ticket.priority == Priority.MED
        assert ticket.status == Status.BACKLOG

    def test_create_ticket_with_priority(self, storage):
        """Test creating a ticket with specific priority."""
        ticket = storage.create("High priority task", priority=Priority.HIGH)
        assert ticket.id == 1
        assert ticket.title == "High priority task"
        assert ticket.priority == Priority.HIGH

    def test_create_ticket_with_status(self, storage):
        """Test creating a ticket with specific status."""
        ticket = storage.create("Done task", status=Status.DONE)
        assert ticket.id == 1
        assert ticket.status == Status.DONE

    def test_create_multiple_tickets_increments_id(self, storage):
        """Test that creating multiple tickets increments ID."""
        ticket1 = storage.create("Task 1")
        ticket2 = storage.create("Task 2")
        ticket3 = storage.create("Task 3")
        assert ticket1.id == 1
        assert ticket2.id == 2
        assert ticket3.id == 3

    # READ tests
    def test_get_existing_ticket(self, storage):
        """Test retrieving an existing ticket."""
        created = storage.create("Test task")
        retrieved = storage.get(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_nonexistent_ticket(self, storage):
        """Test retrieving a non-existent ticket returns None."""
        result = storage.get(999)
        assert result is None

    def test_list_all_empty(self, storage):
        """Test listing all tickets when storage is empty."""
        tickets = storage.list_all()
        assert tickets == []

    def test_list_all_with_tickets(self, storage):
        """Test listing all tickets."""
        storage.create("Task 1")
        storage.create("Task 2")
        storage.create("Task 3")
        tickets = storage.list_all()
        assert len(tickets) == 3
        assert tickets[0].title == "Task 1"
        assert tickets[1].title == "Task 2"
        assert tickets[2].title == "Task 3"

    def test_filter_by_status_backlog(self, storage):
        """Test filtering tickets by BACKLOG status."""
        storage.create("Task 1", status=Status.BACKLOG)
        storage.create("Task 2", status=Status.DONE)
        storage.create("Task 3", status=Status.BACKLOG)

        backlog_tickets = storage.filter_by_status(Status.BACKLOG)
        assert len(backlog_tickets) == 2
        assert all(t.status == Status.BACKLOG for t in backlog_tickets)

    def test_filter_by_status_done(self, storage):
        """Test filtering tickets by DONE status."""
        storage.create("Task 1", status=Status.BACKLOG)
        storage.create("Task 2", status=Status.DONE)
        storage.create("Task 3", status=Status.DONE)

        done_tickets = storage.filter_by_status(Status.DONE)
        assert len(done_tickets) == 2
        assert all(t.status == Status.DONE for t in done_tickets)

    def test_filter_by_priority_high(self, storage):
        """Test filtering tickets by HIGH priority."""
        storage.create("Task 1", priority=Priority.HIGH)
        storage.create("Task 2", priority=Priority.MED)
        storage.create("Task 3", priority=Priority.HIGH)

        high_priority = storage.filter_by_priority(Priority.HIGH)
        assert len(high_priority) == 2
        assert all(t.priority == Priority.HIGH for t in high_priority)

    def test_filter_by_priority_low(self, storage):
        """Test filtering tickets by LOW priority."""
        storage.create("Task 1", priority=Priority.LOW)
        storage.create("Task 2", priority=Priority.MED)
        storage.create("Task 3", priority=Priority.LOW)

        low_priority = storage.filter_by_priority(Priority.LOW)
        assert len(low_priority) == 2
        assert all(t.priority == Priority.LOW for t in low_priority)

    def test_filter_returns_empty_when_no_matches(self, storage):
        """Test filtering returns empty list when no matches."""
        storage.create("Task 1", priority=Priority.HIGH, status=Status.BACKLOG)

        done_tickets = storage.filter_by_status(Status.DONE)
        assert done_tickets == []

    # UPDATE tests
    def test_update_status_existing_ticket(self, storage):
        """Test updating status of an existing ticket."""
        ticket = storage.create("Test task", status=Status.BACKLOG)
        updated = storage.update_status(ticket.id, Status.DONE)

        assert updated is not None
        assert updated.status == Status.DONE
        assert updated.id == ticket.id
        assert updated.title == ticket.title

    def test_update_status_nonexistent_ticket(self, storage):
        """Test updating status of non-existent ticket returns None."""
        result = storage.update_status(999, Status.DONE)
        assert result is None

    def test_update_priority_existing_ticket(self, storage):
        """Test updating priority of an existing ticket."""
        ticket = storage.create("Test task", priority=Priority.MED)
        updated = storage.update_priority(ticket.id, Priority.HIGH)

        assert updated is not None
        assert updated.priority == Priority.HIGH
        assert updated.id == ticket.id
        assert updated.title == ticket.title

    def test_update_priority_nonexistent_ticket(self, storage):
        """Test updating priority of non-existent ticket returns None."""
        result = storage.update_priority(999, Priority.HIGH)
        assert result is None

    def test_updates_persist_in_storage(self, storage):
        """Test that updates persist in storage."""
        ticket = storage.create("Test task", priority=Priority.LOW, status=Status.BACKLOG)
        storage.update_priority(ticket.id, Priority.HIGH)
        storage.update_status(ticket.id, Status.DONE)

        retrieved = storage.get(ticket.id)
        assert retrieved.priority == Priority.HIGH
        assert retrieved.status == Status.DONE

    # DELETE tests
    def test_delete_existing_ticket(self, storage):
        """Test deleting an existing ticket."""
        ticket = storage.create("Test task")
        result = storage.delete(ticket.id)

        assert result is True
        assert storage.get(ticket.id) is None

    def test_delete_nonexistent_ticket(self, storage):
        """Test deleting a non-existent ticket returns False."""
        result = storage.delete(999)
        assert result is False

    def test_delete_removes_from_list(self, storage):
        """Test that deleted ticket is removed from list."""
        storage.create("Task 1")
        ticket2 = storage.create("Task 2")
        storage.create("Task 3")

        storage.delete(ticket2.id)
        all_tickets = storage.list_all()

        assert len(all_tickets) == 2
        assert all(t.id != ticket2.id for t in all_tickets)

    def test_delete_removes_from_filters(self, storage):
        """Test that deleted ticket is removed from filtered results."""
        ticket1 = storage.create("Task 1", priority=Priority.HIGH)
        storage.create("Task 2", priority=Priority.HIGH)

        storage.delete(ticket1.id)
        high_priority = storage.filter_by_priority(Priority.HIGH)

        assert len(high_priority) == 1
        assert high_priority[0].id != ticket1.id

    # Integration tests
    def test_full_crud_cycle(self, storage):
        """Test complete CRUD cycle."""
        # Create
        ticket = storage.create("Integration test", priority=Priority.MED, status=Status.BACKLOG)
        assert ticket.id == 1

        # Read
        retrieved = storage.get(ticket.id)
        assert retrieved.title == "Integration test"

        # Update
        storage.update_priority(ticket.id, Priority.HIGH)
        storage.update_status(ticket.id, Status.DONE)
        updated = storage.get(ticket.id)
        assert updated.priority == Priority.HIGH
        assert updated.status == Status.DONE

        # Delete
        deleted = storage.delete(ticket.id)
        assert deleted is True
        assert storage.get(ticket.id) is None

    def test_multiple_tickets_operations(self, storage):
        """Test operations with multiple tickets."""
        # Create multiple tickets
        t1 = storage.create("Task 1", priority=Priority.HIGH, status=Status.BACKLOG)
        t2 = storage.create("Task 2", priority=Priority.LOW, status=Status.BACKLOG)
        t3 = storage.create("Task 3", priority=Priority.HIGH, status=Status.DONE)

        # Verify all created
        assert len(storage.list_all()) == 3

        # Update one
        storage.update_status(t1.id, Status.DONE)

        # Filter by status
        done_tickets = storage.filter_by_status(Status.DONE)
        assert len(done_tickets) == 2

        # Delete one
        storage.delete(t2.id)
        assert len(storage.list_all()) == 2

        # Verify remaining tickets
        remaining = storage.list_all()
        assert t1.id in [t.id for t in remaining]
        assert t3.id in [t.id for t in remaining]
        assert t2.id not in [t.id for t in remaining]
