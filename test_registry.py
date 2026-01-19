from engine.error_registry import (
    is_known_error,
    is_fixable,
    get_fix_strategy
)

tests = [
    "VALERR-102",
    "AUTHERR-001",
    "XMLERR-001",
    "UNKNOWN-999"
]

for t in tests:
    print(
        t,
        "known:", is_known_error(t),
        "fixable:", is_fixable(t),
        "strategy:", get_fix_strategy(t)
    )
