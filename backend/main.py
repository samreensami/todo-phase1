"""FastAPI application for Ticket Management API."""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from backend.database import get_session
from backend.models import Ticket, TicketCreate, TicketUpdate, TicketPublic
from backend.storage import TicketStorage
from backend.models import Priority, Status

# Create FastAPI app
app = FastAPI(
    title="Dev-Ops Ticket Management API",
    description="REST API for managing tickets",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Dev-Ops Ticket Management API",
        "version": "1.0.0",
        "endpoints": {
            "tickets": "/api/tickets",
            "docs": "/docs"
        }
    }


@app.get("/api/tickets", response_model=List[TicketPublic], tags=["Tickets"])
async def list_tickets(
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    session: Session = Depends(get_session)
):
    """List all tickets with optional filtering.

    Args:
        status: Filter by ticket status (optional)
        priority: Filter by ticket priority (optional)
        session: Database session

    Returns:
        List of tickets
    """
    storage = TicketStorage(session)
    tickets = await storage.list_all(status=status, priority=priority)
    return tickets


@app.get("/api/tickets/{ticket_id}", response_model=TicketPublic, tags=["Tickets"])
async def get_ticket(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific ticket by ID.

    Args:
        ticket_id: Ticket ID
        session: Database session

    Returns:
        Ticket details

    Raises:
        404: Ticket not found
    """
    storage = TicketStorage(session)
    ticket = await storage.get(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@app.post("/api/tickets", response_model=TicketPublic, status_code=201, tags=["Tickets"])
async def create_ticket(
    ticket_data: TicketCreate,
    session: Session = Depends(get_session)
):
    """Create a new ticket.

    Args:
        ticket_data: Ticket data to create
        session: Database session

    Returns:
        Created ticket
    """
    storage = TicketStorage(session)
    ticket = await storage.create(ticket_data)
    return ticket


@app.put("/api/tickets/{ticket_id}", response_model=TicketPublic, tags=["Tickets"])
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    session: Session = Depends(get_session)
):
    """Update a ticket.

    Args:
        ticket_id: Ticket ID
        ticket_data: Ticket data to update
        session: Database session

    Returns:
        Updated ticket

    Raises:
        404: Ticket not found
    """
    storage = TicketStorage(session)

    # Check if ticket exists
    existing = await storage.get(ticket_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update ticket
    ticket = await storage.update(ticket_id, ticket_data)
    return ticket


@app.patch("/api/tickets/{ticket_id}/status", response_model=TicketPublic, tags=["Tickets"])
async def update_ticket_status(
    ticket_id: int,
    status: Status,
    session: Session = Depends(get_session)
):
    """Update ticket status.

    Args:
        ticket_id: Ticket ID
        status: New status
        session: Database session

    Returns:
        Updated ticket

    Raises:
        404: Ticket not found
    """
    storage = TicketStorage(session)

    # Check if ticket exists
    existing = await storage.get(ticket_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update status
    ticket = await storage.update_status(ticket_id, status)
    return ticket


@app.patch("/api/tickets/{ticket_id}/priority", response_model=TicketPublic, tags=["Tickets"])
async def update_ticket_priority(
    ticket_id: int,
    priority: Priority,
    session: Session = Depends(get_session)
):
    """Update ticket priority.

    Args:
        ticket_id: Ticket ID
        priority: New priority
        session: Database session

    Returns:
        Updated ticket

    Raises:
        404: Ticket not found
    """
    storage = TicketStorage(session)

    # Check if ticket exists
    existing = await storage.get(ticket_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update priority
    ticket = await storage.update_priority(ticket_id, priority)
    return ticket


@app.delete("/api/tickets/{ticket_id}", status_code=204, tags=["Tickets"])
async def delete_ticket(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    """Delete a ticket.

    Args:
        ticket_id: Ticket ID
        session: Database session

    Returns:
        No content (204)

    Raises:
        404: Ticket not found
    """
    storage = TicketStorage(session)

    # Check if ticket exists
    existing = await storage.get(ticket_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Delete ticket
    await storage.delete(ticket_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
