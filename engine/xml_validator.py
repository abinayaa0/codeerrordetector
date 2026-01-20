from utils.xml_utils import safe_parse_xml


def is_valid_xml(xml: str) -> bool:
    root, error = safe_parse_xml(xml)
    return root is not None
