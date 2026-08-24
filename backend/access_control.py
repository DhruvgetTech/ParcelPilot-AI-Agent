from fastapi import HTTPException


# Mock logged-in users
USERS = {
    "customer_northstar": {
        "role": "customer",
        "account_id": "ACCT-001"
    },
    "customer_lumenworks": {
        "role": "customer",
        "account_id": "ACCT-002"
    },
    "support_admin": {
        "role": "internal",
        "account_id": None
    }
}


def get_user_context(user_id: str):
    user = USERS.get(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized user"
        )

    return user


def check_account_access(user_context: dict, requested_account_id: str):
    # Internal support user can access all accounts
    if user_context["role"] == "internal":
        return True

    # Customer can access only own account
    if (
        user_context["role"] == "customer"
        and user_context["account_id"] == requested_account_id
    ):
        return True

    raise HTTPException(
        status_code=403,
        detail="You are not authorized to access this account's data."
    )