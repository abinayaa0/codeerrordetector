from engine.error_registry import (
    is_known_error,
    is_fixable,
    get_fix_strategy
)

CONFIDENCE_THRESHOLD = 0.90


def select_fix_strategy(error_code: str, confidence: float) -> str:
    """
    Decide how (or if) an error should be fixed.
    Returns: "rule", "llm", or "none"
    """

    if not is_known_error(error_code):
        return "none"

    if not is_fixable(error_code):
        return "none"

    if confidence < CONFIDENCE_THRESHOLD:
        return "none"

    strategy = get_fix_strategy(error_code)
    return strategy if strategy else "none"
