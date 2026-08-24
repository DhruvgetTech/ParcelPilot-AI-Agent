from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.data_service import (
    lookup_account,
    lookup_order,
    lookup_ticket
)

from backend.agent_service import build_context

from backend.access_control import (
    get_user_context,
    check_account_access
)

from backend.escalation_service import (
    create_escalation,
    get_escalations
)


# ================= APP =================

app = FastAPI(
    title="ParcelPilot AI Agent",
    description="AI-powered customer support agent for ParcelPilot",
    version="1.0.0"
)


# ================= CORS =================
# Allows React frontend to communicate with FastAPI backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= REQUEST MODELS =================

class AskRequest(BaseModel):
    question: str


class PrepareEscalationRequest(BaseModel):
    ticket_id: str
    reason: str


class ConfirmEscalationRequest(BaseModel):
    ticket_id: str
    reason: str
    confirmed: bool


# ================= BASIC APIs =================

@app.get("/")
def home():
    return {
        "message": "ParcelPilot AI Agent Backend is Running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ================= ACCESS CONTROL =================

def get_current_user(
    x_user_id: str = Header(default="support_admin")
):
    return get_user_context(x_user_id)


def authorize_context(
    context: dict,
    user_context: dict
):
    """
    Enforce account-level access in backend tool layer.

    Customer users can only access data belonging
    to their own account.

    Internal users can access all customer data.
    """

    # Internal user can access everything
    if user_context["role"] == "internal":
        return context

    allowed_account_id = str(
        user_context["account_id"]
    ).upper()

    # Check account result
    account = context.get("account")

    if account:
        account_id = str(
            account.get("account_id", "")
        ).upper()

        if account_id != allowed_account_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You are not authorized to "
                    "access this account."
                )
            )

    # Check order result
    order = context.get("order")

    if order:
        order_account_id = str(
            order.get("account_id", "")
        ).upper()

        if order_account_id != allowed_account_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You are not authorized to "
                    "access this order."
                )
            )

    # Check ticket result
    ticket = context.get("ticket")

    if ticket:
        ticket_account_id = str(
            ticket.get("account_id", "")
        ).upper()

        if ticket_account_id != allowed_account_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You are not authorized to "
                    "access this ticket."
                )
            )

    return context


# ================= DIRECT API LOOKUPS =================

@app.get("/accounts/{account_id}")
def get_account(
    account_id: str,
    x_user_id: str = Header(default="support_admin")
):
    user = get_user_context(x_user_id)

    check_account_access(
        user,
        account_id.upper()
    )

    result = lookup_account(account_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return result


@app.get("/orders/{order_id}")
def get_order(
    order_id: str,
    x_user_id: str = Header(default="support_admin")
):
    user = get_user_context(x_user_id)

    result = lookup_order(order_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    check_account_access(
        user,
        str(
            result.get("account_id", "")
        ).upper()
    )

    return result


@app.get("/tickets/{ticket_id}")
def get_ticket(
    ticket_id: str,
    x_user_id: str = Header(default="support_admin")
):
    user = get_user_context(x_user_id)

    result = lookup_ticket(ticket_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    check_account_access(
        user,
        str(
            result.get("account_id", "")
        ).upper()
    )

    return result


# ================= PREPARE ESCALATION =================

@app.post("/prepare-escalation")
def prepare_escalation(
    request: PrepareEscalationRequest,
    x_user_id: str = Header(default="support_admin")
):
    """
    Prepare an escalation but DO NOT create it.
    Explicit confirmation is required.
    """

    user = get_user_context(x_user_id)

    ticket_id = request.ticket_id.upper()

    ticket = lookup_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    check_account_access(
        user,
        str(
            ticket.get("account_id", "")
        ).upper()
    )

    return {
        "status": "confirmation_required",
        "message": (
            f"Escalation for ticket {ticket_id} has been "
            "prepared but NOT created yet. "
            "Please confirm the action to create the escalation."
        ),
        "ticket_id": ticket_id,
        "reason": request.reason,
        "action": "create_escalation"
    }


# ================= CONFIRM ESCALATION =================

@app.post("/confirm-escalation")
def confirm_escalation(
    request: ConfirmEscalationRequest,
    x_user_id: str = Header(default="support_admin")
):
    """
    Create escalation only after explicit confirmation.
    """

    user = get_user_context(x_user_id)

    ticket_id = request.ticket_id.upper()

    # If user does not confirm
    if not request.confirmed:
        return {
            "status": "cancelled",
            "message": (
                "Escalation was not created because "
                "confirmation was not provided."
            ),
            "ticket_id": ticket_id
        }

    # Verify ticket exists
    ticket = lookup_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Access control
    check_account_access(
        user,
        str(
            ticket.get("account_id", "")
        ).upper()
    )

    # State-changing action happens ONLY here
    escalation = create_escalation(
        ticket_id=ticket_id,
        reason=request.reason,
        created_by=x_user_id
    )

    return {
        "status": "success",
        "message": (
            f"Escalation for ticket {ticket_id} "
            "was created successfully."
        ),
        "escalation": escalation
    }


# ================= VIEW ESCALATIONS =================

@app.get("/escalations")
def list_escalations(
    x_user_id: str = Header(default="support_admin")
):
    """
    Only internal users can view all escalations.
    """

    user = get_user_context(x_user_id)

    if user["role"] != "internal":
        raise HTTPException(
            status_code=403,
            detail=(
                "Only internal users can view all escalations."
            )
        )

    escalations = get_escalations()

    return {
        "count": len(escalations),
        "escalations": escalations
    }


# ================= ANSWER GENERATION =================

def generate_answer(context: dict) -> str:

    answers = []

    account = context.get("account")
    order = context.get("order")
    ticket = context.get("ticket")

    knowledge = context.get(
        "relevant_knowledge",
        []
    )

    # ================= ACCOUNT ANSWER =================

    if account:

        account_name = account.get(
            "account_name",
            "the customer"
        )

        account_id = account.get(
            "account_id",
            ""
        )

        plan = account.get(
            "plan",
            ""
        )

        status = account.get(
            "status",
            ""
        )

        csm = account.get(
            "csm",
            ""
        )

        premium_support = account.get(
            "premium_support",
            False
        )

        notes = account.get(
            "notes",
            ""
        )

        answer = (
            f"Account {account_id} belongs to "
            f"{account_name}."
        )

        if status:
            answer += (
                f" Its current status is {status}."
            )

        if plan:
            answer += (
                f" The account is on the {plan} plan."
            )

        if premium_support:
            answer += (
                " It has premium support."
            )

        if csm:
            answer += (
                f" The account is managed by {csm}."
            )

        if notes:
            answer += (
                f" Notes: {notes}"
            )

        answers.append(answer)

    # ================= ORDER ANSWER =================

    if order:

        order_id = order.get(
            "order_id",
            ""
        )

        status = order.get(
            "status",
            ""
        )

        shipment_status = order.get(
            "shipment_status",
            ""
        )

        cancellation_requested_at = order.get(
            "cancellation_requested_at",
            None
        )

        cancellation_reason = order.get(
            "cancellation_reason",
            ""
        )

        answer = (
            f"Order {order_id} was found."
        )

        if status:
            answer += (
                f" Its status is {status}."
            )

        if shipment_status:
            answer += (
                f" Shipment status: {shipment_status}."
            )

        if cancellation_requested_at:
            answer += (
                f" A cancellation was requested at "
                f"{cancellation_requested_at}."
            )

        if cancellation_reason:
            answer += (
                f" Reason: {cancellation_reason}."
            )

        answers.append(answer)

    # ================= TICKET ANSWER =================

    if ticket:

        ticket_id = ticket.get(
            "ticket_id",
            ""
        )

        status = ticket.get(
            "status",
            ""
        )

        priority = ticket.get(
            "priority",
            ""
        )

        subject = ticket.get(
            "subject",
            ""
        )

        description = ticket.get(
            "description",
            ""
        )

        answer = (
            f"Support ticket {ticket_id} was found."
        )

        if subject:
            answer += (
                f" Subject: {subject}."
            )

        if status:
            answer += (
                f" Current status: {status}."
            )

        if priority:
            answer += (
                f" Priority: {priority}."
            )

        if description:
            answer += (
                f" Details: {description}"
            )

        answers.append(answer)

    # ================= KNOWLEDGE SOURCES =================

    if knowledge:

        filenames = [
            item.get("filename")
            for item in knowledge[:3]
            if item.get("filename")
        ]

        if filenames:
            answers.append(
                "I also found relevant information in: "
                + ", ".join(filenames)
                + "."
            )

    # ================= NO RESULT =================

    if not answers:
        return (
            "I could not find enough information to answer "
            "this request. Please provide a valid account, "
            "order, or ticket ID."
        )

    return " ".join(answers)


# ================= AI AGENT =================

@app.post("/ask")
def ask_agent(
    request: AskRequest,
    x_user_id: str = Header(default="support_admin")
):
    """
    Main AI Agent endpoint.
    """

    user = get_user_context(x_user_id)

    # Build context
    context = build_context(
        request.question
    )

    # Enforce access control
    context = authorize_context(
        context,
        user
    )

    # Generate answer
    answer = generate_answer(context)

    return {
        "question": request.question,
        "answer": answer,
        "user_role": user["role"],
        "account": context.get("account"),
        "order": context.get("order"),
        "ticket": context.get("ticket"),
        "knowledge_sources": [
            {
                "filename": item.get("filename"),
                "score": item.get("score")
            }
            for item in context.get(
                "relevant_knowledge",
                []
            )
        ]
    }