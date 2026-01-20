from datetime import datetime

def fix_valerr_102(value: str):
    """
    Fix PIN by zero-padding to 6 digits.
    """
    if value is None:
        return None

    if not value.isdigit(): 
        return None

    return value.zfill(6)


def fix_valerr_103(value: str):
    try:
        # Known input format
        dt = datetime.strptime(value, "%d-%m-%Y")
        # Convert to expected format
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


RULE_FIXES = {
    "VALERR-102": fix_valerr_102,
    "VALERR-103": fix_valerr_103
}


def apply_rule_fix(error_code: str, localization: dict):
    """
    Apply a rule-based fix if available. maps error code to a localization and fix
    """
    fixer = RULE_FIXES.get(error_code) 

    if not fixer:
        return None
 

    return fixer(localization.get("value"))
    
