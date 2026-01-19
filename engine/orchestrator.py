from engine.localize import localize_error
from engine.fix_selector import select_fix_strategy
from engine.fix_rules import apply_rule_fix
from engine.error_registry import get_error_description


def process_xml(xml: str, error_code: str, confidence: float) -> dict:
    localization = localize_error(xml, error_code)
    strategy = select_fix_strategy(error_code, confidence)

    result = {
        "error_code": error_code,
        "confidence": confidence,
        "fix_strategy": strategy,
        "auto_fix_applied": False,
        "original_value": localization.get("value"),
        "fixed_value": None,
        "explanation": get_error_description(error_code)
    }

    if strategy == "rule":
        fixed = apply_rule_fix(error_code, localization)
        if fixed is not None:
            result["auto_fix_applied"] = True
            result["fixed_value"] = fixed

    return result
