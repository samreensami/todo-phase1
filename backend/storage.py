"""In-memory ticket storage manager."""

from typing import Dict, List, Optional
from backend.models import Ticket, Priority, Status


class TicketStorage:
    """Manages tickets in memory."""

    def __init__(self):
        """Initialize empty ticket storage."""
        self._tickets: Dict[int, Ticket] = {}
        self._next_id: int = 1

    def create(self, title: str, priority: Priority = Priority.MED, status: Status = Status.BACKLOG) -> Ticket:
        """Create a new ticket.

        Args:
            title: Ticket title
            priority: Ticket priority (default: MED)
            status: Ticket status (default: BACKLOG)

        Returns:
            Created ticket
        """
        ticket = Ticket(
            id=self._next_id,
            title=title,
            priority=priority,
            status=status
        )
        self._tickets[self._next_id] = ticket
        self._next_id += 1
        return ticket

    def get(self, ticket_id: int) -> Optional[Ticket]:
        """Get a ticket by ID.

        Args:
            ticket_id: Ticket ID

        Returns:
            Ticket if found, None otherwise
        """
        return self._tickets.get(ticket_id)

    def list_all(self) -> List[Ticket]:
        """List all tickets.

        Returns:
            List of all tickets
        """
        return list(self._tickets.values())

    def update_status(self, ticket_id: int, status: Status) -> Optional[Ticket]:
        """Update ticket status.

        Args:
            ticket_id: Ticket ID
            status: New status

        Returns:
            Updated ticket if found, None otherwise
        """
        ticket = self._tickets.get(ticket_id)
        if ticket:
            ticket.status = status
        return ticket

    def update_priority(self, ticket_id: int, priority: Priority) -> Optional[Ticket]:
        """Update ticket priority.

        Args:
            ticket_id: Ticket ID
            priority: New priority

        Returns:
            Updated ticket if found, None otherwise
        """
        ticket = self._tickets.get(ticket_id)
        if ticket:
            ticket.priority = priority
        return ticket

    def delete(self, ticket_id: int) -> bool:
        """Delete a ticket.

        Args:
            ticket_id: Ticket ID

        Returns:
            True if deleted, False if not found
        """
        if ticket_id in self._tickets:
            del self._tickets[ticket_id]
            return True
        return False

    def filter_by_status(self, status: Status) -> List[Ticket]:
        """Filter tickets by status.

        Args:
            status: Status to filter by

        Returns:
            List of tickets with matching status
        """
        return [t for t in self._tickets.values() if t.status == status]

    def filter_by_priority(self, priority: Priority) -> List[Ticket]:
        """Filter tickets by priority.

        Args:
            priority: Priority to filter by

        Returns:
            List of tickets with matching priority
        """
        return [t for t in self._tickets.values() if t.priority == priority]
