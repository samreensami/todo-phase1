"""Database session management for Neon PostgreSQL."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.models import Ticket, TicketCreate, TicketUpdate, Status, Priority


class TicketStorage:
    """Manages tickets using Neon PostgreSQL database."""

    def __init__(self, session: AsyncSession):
        """Initialize storage with database session.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session

    async def create(self, ticket_data: TicketCreate) -> Ticket:
        """Create a new ticket in database.

        Args:
            ticket_data: Ticket data to create

        Returns:
            Created ticket
        """
        db_ticket = Ticket.model_validate(ticket_data)
        self.session.add(db_ticket)
        await self.session.commit()
        await self.session.refresh(db_ticket)
        return db_ticket

    async def get(self, ticket_id: int) -> Optional[Ticket]:
        """Get a ticket by ID.

        Args:
            ticket_id: Ticket ID

        Returns:
            Ticket if found, None otherwise
        """
        statement = select(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.exec(statement)
        return result.first()

    async def list_all(self, status: Optional[Status] = None, priority: Optional[Priority] = None) -> List[Ticket]:
        """List all tickets with optional filtering.

        Args:
            status: Filter by status (optional)
            priority: Filter by priority (optional)

        Returns:
            List of tickets
        """
        statement = select(Ticket)

        if status:
            statement = statement.where(Ticket.status == status)
        if priority:
            statement = statement.where(Ticket.priority == priority)

        statement = statement.order_by(Ticket.created_at.desc())

        result = await self.session.exec(statement)
        return list(result.all())

    async def update(self, ticket_id: int, ticket_data: TicketUpdate) -> Optional[Ticket]:
        """Update a ticket.

        Args:
            ticket_id: Ticket ID
            ticket_data: Data to update

        Returns:
            Updated ticket if found, None otherwise
        """
        statement = select(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.exec(statement)
        ticket = result.first()

        if ticket:
            update_data = ticket_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(ticket, field, value)

            self.session.add(ticket)
            await self.session.commit()
            await self.session.refresh(ticket)

        return ticket

    async def update_status(self, ticket_id: int, status: Status) -> Optional[Ticket]:
        """Update ticket status.

        Args:
            ticket_id: Ticket ID
            status: New status

        Returns:
            Updated ticket if found, None otherwise
        """
        statement = select(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.exec(statement)
        ticket = result.first()

        if ticket:
            ticket.status = status
            self.session.add(ticket)
            await self.session.commit()
            await self.session.refresh(ticket)

        return ticket

    async def update_priority(self, ticket_id: int, priority: Priority) -> Optional[Ticket]:
        """Update ticket priority.

        Args:
            ticket_id: Ticket ID
            priority: New priority

        Returns:
            Updated ticket if found, None otherwise
        """
        statement = select(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.exec(statement)
        ticket = result.first()

        if ticket:
            ticket.priority = priority
            self.session.add(ticket)
            await self.session.commit()
            await self.session.refresh(ticket)

        return ticket

    async def delete(self, ticket_id: int) -> bool:
        """Delete a ticket.

        Args:
            ticket_id: Ticket ID

        Returns:
            True if deleted, False if not found
        """
        statement = select(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.exec(statement)
        ticket = result.first()

        if ticket:
            await self.session.delete(ticket)
            await self.session.commit()
            return True
        return False
