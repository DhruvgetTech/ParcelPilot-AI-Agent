import re

from backend.data_service import (
    lookup_account,
    lookup_order,
    lookup_ticket
)

from backend.knowledge_service import search_knowledge


def build_context(question: str):
    # IDs find karo
    account_match = re.search(r"ACCT-\d+", question, re.IGNORECASE)
    order_match = re.search(r"ORD-\d+", question, re.IGNORECASE)
    ticket_match = re.search(r"TKT-\d+", question, re.IGNORECASE)

    account_id = account_match.group(0).upper() if account_match else None
    order_id = order_match.group(0).upper() if order_match else None
    ticket_id = ticket_match.group(0).upper() if ticket_match else None

    # Data lookup
    account = lookup_account(account_id) if account_id else None
    order = lookup_order(order_id) if order_id else None
    ticket = lookup_ticket(ticket_id) if ticket_id else None

    # Relevant PDF knowledge search
    knowledge_results = search_knowledge(question)

    # Final context
    context = {
        "question": question,
        "account": account,
        "order": order,
        "ticket": ticket,
        "relevant_knowledge": knowledge_results
    }

    return context