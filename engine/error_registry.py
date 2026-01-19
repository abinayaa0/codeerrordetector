"""
Central error registry and policy definition.

This file defines:
- which error codes exist
- what type they are
- whether they are auto-fixable
- which fix strategy is allowed

This is the single source of truth for the system.
"""

ERROR_REGISTRY = {
    "SUCCESS": {
        "type": "success",
        "fixable": False,
        "description": "Valid KYC request"
    },

    # -----------------------
    # Validation Errors
    # -----------------------

    "VALERR-002": {
        "type": "validation",
        "field": "PAN",
        "fixable": False,
        "description": "PAN missing or empty"
    },

    "VALERR-102": {
        "type": "validation",
        "field": "PIN",
        "fixable": True,
        "fix_strategy": "rule",
        "description": "Invalid PIN code format"
    },

    "VALERR-103": {
        "type": "validation",
        "field": "DOB",
        "fixable": False,
        "description": "Invalid date format"
    },

    # -----------------------
    # Authentication Errors
    # -----------------------

    "AUTHERR-001": {
        "type": "auth",
        "fixable": False,
        "description": "Authentication failed"
    },

    # -----------------------
    # Business Errors
    # -----------------------

    "BUSERR-310": {
        "type": "business",
        "fixable": False,
        "description": "Business rule violation"
    },

    # -----------------------
    # Network / Web Errors
    # -----------------------

    "WEBERR-005": {
        "type": "network",
        "fixable": False,
        "description": "Upstream service unavailable"
    },

    # -----------------------
    # XML / Structural Errors
    # -----------------------

    "XMLERR-001": {
        "type": "xml",
        "fixable": True,
        "fix_strategy": "llm",
        "description": "Malformed XML structure"
    }
}


def is_known_error(error_code: str) -> bool:
    """
    Check if the error code is known to the system.
    """
    return error_code in ERROR_REGISTRY


def is_fixable(error_code: str) -> bool:
    """
    Check if the error is allowed to be auto-fixed.
    """
    return ERROR_REGISTRY.get(error_code, {}).get("fixable", False)


def get_error_type(error_code: str) -> str:
    """
    Return the high-level error category.
    """
    return ERROR_REGISTRY.get(error_code, {}).get("type", "unknown")


def get_fix_strategy(error_code: str):
    """
    Return allowed fix strategy for the error.
    """
    return ERROR_REGISTRY.get(error_code, {}).get("fix_strategy", None)


def get_error_description(error_code: str) -> str:
    """
    Human-readable error description.
    """
    return ERROR_REGISTRY.get(error_code, {}).get(
        "description", "Unknown error"
    )
