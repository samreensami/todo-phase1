"""CLI interface using Typer with Rich formatting."""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from src.models import Priority, Status
from src.storage import TicketStorage

app = typer.Typer(help="Dev-Ops Ticket Management CLI")
console = Console()
storage = TicketStorage()


def display_ticket(ticket):
    """Display a single ticket with rich formatting."""
    priority_colors = {
        "LOW": "green",
        "MED": "yellow",
        "HIGH": "red"
    }
    status_colors = {
        "BACKLOG": "blue",
        "DONE": "green"
    }

    # Get string values from enums
    priority_val = ticket.priority.value if hasattr(ticket.priority, 'value') else ticket.priority
    status_val = ticket.status.value if hasattr(ticket.status, 'value') else ticket.status

    priority_color = priority_colors.get(priority_val, "white")
    status_color = status_colors.get(status_val, "white")

    panel = Panel(
        f"[bold]Title:[/bold] {ticket.title}\n"
        f"[bold]Priority:[/bold] [{priority_color}]{priority_val}[/{priority_color}]\n"
        f"[bold]Status:[/bold] [{status_color}]{status_val}[/{status_color}]",
        title=f"Ticket #{ticket.id}",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(panel)


def display_tickets_table(tickets):
    """Display multiple tickets in a table."""
    if not tickets:
        console.print("[yellow]No tickets found.[/yellow]")
        return

    table = Table(title="Tickets", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title", style="white")
    table.add_column("Priority", justify="center")
    table.add_column("Status", justify="center")

    priority_colors = {
        "LOW": "green",
        "MED": "yellow",
        "HIGH": "red"
    }
    status_colors = {
        "BACKLOG": "blue",
        "DONE": "green"
    }

    for ticket in tickets:
        # Get string values from enums
        priority_val = ticket.priority.value if hasattr(ticket.priority, 'value') else ticket.priority
        status_val = ticket.status.value if hasattr(ticket.status, 'value') else ticket.status

        priority_color = priority_colors.get(priority_val, "white")
        status_color = status_colors.get(status_val, "white")

        table.add_row(
            str(ticket.id),
            ticket.title,
            f"[{priority_color}]{priority_val}[/{priority_color}]",
            f"[{status_color}]{status_val}[/{status_color}]"
        )

    console.print(table)


@app.command()
def create(
    title: str = typer.Argument(..., help="Ticket title"),
    priority: Priority = typer.Option(Priority.MED, help="Ticket priority"),
    status: Status = typer.Option(Status.BACKLOG, help="Ticket status")
):
    """Create a new ticket."""
    ticket = storage.create(title=title, priority=priority, status=status)
    console.print(f"[green]SUCCESS[/green] Ticket created successfully!")
    display_ticket(ticket)


@app.command()
def list(
    status: Optional[Status] = typer.Option(None, help="Filter by status"),
    priority: Optional[Priority] = typer.Option(None, help="Filter by priority")
):
    """List all tickets or filter by status/priority."""
    if status:
        tickets = storage.filter_by_status(status)
    elif priority:
        tickets = storage.filter_by_priority(priority)
    else:
        tickets = storage.list_all()

    display_tickets_table(tickets)


@app.command()
def get(ticket_id: int = typer.Argument(..., help="Ticket ID")):
    """Get a specific ticket by ID."""
    ticket = storage.get(ticket_id)
    if ticket:
        display_ticket(ticket)
    else:
        console.print(f"[red]ERROR[/red] Ticket #{ticket_id} not found.")
        raise typer.Exit(code=1)


@app.command()
def update_status(
    ticket_id: int = typer.Argument(..., help="Ticket ID"),
    status: Status = typer.Argument(..., help="New status")
):
    """Update ticket status."""
    ticket = storage.update_status(ticket_id, status)
    if ticket:
        console.print(f"[green]SUCCESS[/green] Ticket #{ticket_id} status updated to {status}!")
        display_ticket(ticket)
    else:
        console.print(f"[red]ERROR[/red] Ticket #{ticket_id} not found.")
        raise typer.Exit(code=1)


@app.command()
def update_priority(
    ticket_id: int = typer.Argument(..., help="Ticket ID"),
    priority: Priority = typer.Argument(..., help="New priority")
):
    """Update ticket priority."""
    ticket = storage.update_priority(ticket_id, priority)
    if ticket:
        console.print(f"[green]SUCCESS[/green] Ticket #{ticket_id} priority updated to {priority}!")
        display_ticket(ticket)
    else:
        console.print(f"[red]ERROR[/red] Ticket #{ticket_id} not found.")
        raise typer.Exit(code=1)


@app.command()
def delete(ticket_id: int = typer.Argument(..., help="Ticket ID")):
    """Delete a ticket."""
    if storage.delete(ticket_id):
        console.print(f"[green]SUCCESS[/green] Ticket #{ticket_id} deleted successfully!")
    else:
        console.print(f"[red]ERROR[/red] Ticket #{ticket_id} not found.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
