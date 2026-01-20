from engine.localize import localize_error
from engine.fix_selector import select_fix_strategy
from engine.fix_rules import apply_rule_fix
from engine.llm_fix import repair_xml_with_llm
from engine.xml_validator import is_valid_xml
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

    # RULE FIX
    if strategy == "rule":
        fixed = apply_rule_fix(error_code, localization)
        if fixed is not None:
            result["auto_fix_applied"] = True
            result["fixed_value"] = fixed

    # LLM FIX
    elif strategy == "llm":
        llm_result = repair_xml_with_llm(xml)
        repaired_xml = llm_result["repaired_xml"]

        if repaired_xml and is_valid_xml(repaired_xml):
            result["auto_fix_applied"] = True
            result["fixed_value"] = repaired_xml
            result["explanation"] = llm_result["explanation"]
        else:
            result["explanation"] = llm_result.get("explanation", "LLM output rejected")



    return result

def auto_correct_xml(xml: str, error_code: str, confidence: float):
    return process_xml(xml, error_code, confidence)
