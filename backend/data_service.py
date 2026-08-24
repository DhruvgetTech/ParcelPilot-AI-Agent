import pandas as pd
from pathlib import Path


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Excel file path
EXCEL_FILE = BASE_DIR / "data" / "ParcelPilot_Assessment_Data.xlsx"


# Load Excel sheets
accounts_df = pd.read_excel(EXCEL_FILE, sheet_name="accounts")
orders_df = pd.read_excel(EXCEL_FILE, sheet_name="orders")
tickets_df = pd.read_excel(EXCEL_FILE, sheet_name="tickets")


def lookup_account(account_id: str):
    """Find an account by account ID."""

    if not account_id:
        return None

    account_id = str(account_id).strip().upper()

    result = accounts_df[
        accounts_df["account_id"]
        .astype(str)
        .str.strip()
        .str.upper() == account_id
    ]

    if result.empty:
        return None

    return result.iloc[0].fillna("").to_dict()


def lookup_order(order_id: str):
    """Find an order by order ID."""

    if not order_id:
        return None

    order_id = str(order_id).strip().upper()

    result = orders_df[
        orders_df["order_id"]
        .astype(str)
        .str.strip()
        .str.upper() == order_id
    ]

    if result.empty:
        return None

    return result.iloc[0].fillna("").to_dict()


def lookup_ticket(ticket_id: str):
    """Find a ticket by ticket ID."""

    if not ticket_id:
        return None

    ticket_id = str(ticket_id).strip().upper()

    result = tickets_df[
        tickets_df["ticket_id"]
        .astype(str)
        .str.strip()
        .str.upper() == ticket_id
    ]

    if result.empty:
        print(f"Ticket not found: {ticket_id}")
        print("Available ticket IDs:")
        print(tickets_df["ticket_id"].tolist())
        return None

    return result.iloc[0].fillna("").to_dict()