from datetime import datetime

escalations = []


def create_escalation(ticket_id: str, reason: str, created_by: str):
    """Create a mock escalation."""

    escalation = {
        "escalation_id": f"ESC-{len(escalations) + 1:03d}",
        "ticket_id": ticket_id,
        "reason": reason,
        "status": "created",
        "created_by": created_by,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    escalations.append(escalation)

    return escalation


def get_escalations():
    """Return all created escalations."""
    return escalations