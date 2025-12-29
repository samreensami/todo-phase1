"""Demo script to showcase all CLI functionality."""

from src.storage import TicketStorage
from src.models import Priority, Status
from src.cli import display_ticket, display_tickets_table
from rich.console import Console

console = Console()
storage = TicketStorage()

# Create tickets
console.print("\n[bold cyan]Creating tickets...[/bold cyan]\n")
t1 = storage.create("Fix login bug", Priority.HIGH, Status.BACKLOG)
t2 = storage.create("Add dark mode", Priority.MED, Status.BACKLOG)
t3 = storage.create("Update docs", Priority.LOW, Status.DONE)
t4 = storage.create("Refactor auth", Priority.HIGH, Status.BACKLOG)

# List all tickets
console.print("\n[bold cyan]All Tickets:[/bold cyan]")
display_tickets_table(storage.list_all())

# Filter by status
console.print("\n[bold cyan]Backlog Tickets:[/bold cyan]")
display_tickets_table(storage.filter_by_status(Status.BACKLOG))

# Filter by priority
console.print("\n[bold cyan]High Priority Tickets:[/bold cyan]")
display_tickets_table(storage.filter_by_priority(Priority.HIGH))

# Update ticket status
console.print("\n[bold cyan]Updating ticket #1 to DONE...[/bold cyan]")
storage.update_status(1, Status.DONE)
display_ticket(storage.get(1))

# Update ticket priority
console.print("\n[bold cyan]Updating ticket #2 priority to HIGH...[/bold cyan]")
storage.update_priority(2, Priority.HIGH)
display_ticket(storage.get(2))

# Show final state
console.print("\n[bold cyan]Final State:[/bold cyan]")
display_tickets_table(storage.list_all())

console.print("\n[bold green]Demo completed successfully![/bold green]\n")
