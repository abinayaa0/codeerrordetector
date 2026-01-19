import xml.etree.ElementTree as ET


def safe_parse_xml(xml: str):
    """
    Safely parse XML.
    Returns:
        (root, None) on success
        (None, error_message) on failure
    """
    try:
        root = ET.fromstring(xml)
        return root, None
    except ET.ParseError as e:
        return None, str(e)


def extract_field_value(root, field_name: str):
    """
    Extract text value of a field from XML.
    Returns None if not found.
    """
    if root is None or field_name is None:
        return None

    elem = root.find(f".//{field_name}")
    return elem.text if elem is not None else None
