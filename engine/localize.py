import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.error_registry import ERROR_REGISTRY
from utils.xml_utils import safe_parse_xml, extract_field_value


def localize_error(xml: str, error_code: str) -> dict:
    """
    Locate where the error occurred in the XML.

    Returns a dictionary with localization details.
    """
    meta = ERROR_REGISTRY.get(error_code)

    # Unknown error — nothing to localize
    if not meta:
        return {"localization": "unknown"}

    error_type = meta.get("type")

    # SUCCESS — no error
    if error_type == "success":
        return {"localization": "none"}

    # XML / structural errors
    if error_type == "xml":
        _, parse_error = safe_parse_xml(xml)
        return {
            "localization": "xml_structure",
            "detail": parse_error
        }

    # Validation errors — field-level
    if error_type == "validation":
        field = meta.get("field")
        root, parse_error = safe_parse_xml(xml)

        if parse_error:
            return {
                "localization": "xml_structure",
                "detail": parse_error
            }

        value = extract_field_value(root, field)

        return {
            "localization": "field",
            "field": field,
            "value": value
        }

    # Auth / business / network errors
    return {
        "localization": "non_localizable",
        "detail": "Error not tied to XML content"
    }
