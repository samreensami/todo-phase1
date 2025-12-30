"""Tests for CLI commands."""

import pytest
from typer.testing import CliRunner
from backend.cli import app
from backend.models import Priority, Status


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


class TestCreateCommand:
    """Test create command."""

    def test_create_basic_ticket(self, runner):
        """Test creating a basic ticket."""
        result = runner.invoke(app, ["create", "Test task"])
        assert result.exit_code == 0
        assert "SUCCESS" in result.stdout
        assert "Ticket created successfully" in result.stdout
        assert "Test task" in result.stdout

    def test_create_with_high_priority(self, runner):
        """Test creating a ticket with HIGH priority."""
        result = runner.invoke(app, ["create", "Important task", "--priority", "HIGH"])
        assert result.exit_code == 0
        assert "HIGH" in result.stdout

    def test_create_with_low_priority(self, runner):
        """Test creating a ticket with LOW priority."""
        result = runner.invoke(app, ["create", "Minor task", "--priority", "LOW"])
        assert result.exit_code == 0
        assert "LOW" in result.stdout

    def test_create_with_done_status(self, runner):
        """Test creating a ticket with DONE status."""
        result = runner.invoke(app, ["create", "Completed task", "--status", "DONE"])
        assert result.exit_code == 0
        assert "DONE" in result.stdout


class TestListCommand:
    """Test list command."""

    def test_list_shows_tickets(self, runner):
        """Test that list command works."""
        # Note: Storage is shared across test invocations in the same session
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        # Should show either tickets or "No tickets found" depending on test order
        assert "Tickets" in result.stdout or "No tickets found" in result.stdout


class TestGetCommand:
    """Test get command."""

    def test_get_nonexistent_ticket(self, runner):
        """Test getting a non-existent ticket."""
        result = runner.invoke(app, ["get", "999"])
        assert result.exit_code == 1
        assert "ERROR" in result.stdout
        assert "not found" in result.stdout


class TestUpdateStatusCommand:
    """Test update-status command."""

    def test_update_status_nonexistent_ticket(self, runner):
        """Test updating status of non-existent ticket."""
        result = runner.invoke(app, ["update-status", "999", "DONE"])
        assert result.exit_code == 1
        assert "ERROR" in result.stdout
        assert "not found" in result.stdout


class TestUpdatePriorityCommand:
    """Test update-priority command."""

    def test_update_priority_nonexistent_ticket(self, runner):
        """Test updating priority of non-existent ticket."""
        result = runner.invoke(app, ["update-priority", "999", "HIGH"])
        assert result.exit_code == 1
        assert "ERROR" in result.stdout
        assert "not found" in result.stdout


class TestDeleteCommand:
    """Test delete command."""

    def test_delete_nonexistent_ticket(self, runner):
        """Test deleting a non-existent ticket."""
        result = runner.invoke(app, ["delete", "999"])
        assert result.exit_code == 1
        assert "ERROR" in result.stdout
        assert "not found" in result.stdout


class TestCLIHelp:
    """Test CLI help functionality."""

    def test_main_help(self, runner):
        """Test main help command."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Dev-Ops Ticket Management CLI" in result.stdout

    def test_create_help(self, runner):
        """Test create command help."""
        result = runner.invoke(app, ["create", "--help"])
        assert result.exit_code == 0
        assert "Create a new ticket" in result.stdout

    def test_list_help(self, runner):
        """Test list command help."""
        result = runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
        assert "List all tickets" in result.stdout

    def test_get_help(self, runner):
        """Test get command help."""
        result = runner.invoke(app, ["get", "--help"])
        assert result.exit_code == 0
        assert "Get a specific ticket" in result.stdout

    def test_update_status_help(self, runner):
        """Test update-status command help."""
        result = runner.invoke(app, ["update-status", "--help"])
        assert result.exit_code == 0
        assert "Update ticket status" in result.stdout

    def test_update_priority_help(self, runner):
        """Test update-priority command help."""
        result = runner.invoke(app, ["update-priority", "--help"])
        assert result.exit_code == 0
        assert "Update ticket priority" in result.stdout

    def test_delete_help(self, runner):
        """Test delete command help."""
        result = runner.invoke(app, ["delete", "--help"])
        assert result.exit_code == 0
        assert "Delete a ticket" in result.stdout
