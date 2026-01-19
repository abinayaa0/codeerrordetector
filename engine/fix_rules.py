def fix_valerr_102(value: str):
    """
    Fix PIN by zero-padding to 6 digits.
    """
    if value is None:
        return None

    if not value.isdigit():
        return None

    return value.zfill(6)

RULE_FIXES = {
    "VALERR-102": fix_valerr_102
}


def apply_rule_fix(error_code: str, localization: dict):
    """
    Apply a rule-based fix if available.
    """
    fixer = RULE_FIXES.get(error_code)
    if not fixer:
        return None

    return fixer(localization.get("value"))
