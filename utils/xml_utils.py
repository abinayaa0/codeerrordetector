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


def replace_field_value(xml: str, field_name: str, new_value: str) -> str:
    """
    Replace text value of a field in the XML string.
    Returns the updated XML string or original if failed.
    """
    try:
        root = ET.fromstring(xml)
        elem = root.find(f".//{field_name}")
        if elem is not None:
            elem.text = new_value
            return ET.tostring(root, encoding="unicode")
        return xml
    except:
        return xml
