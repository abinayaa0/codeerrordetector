from engine.localize import localize_error

xml_valid = "<KYC><PIN>123</PIN></KYC>"
xml_invalid = "<KYC><PIN>123</PIN>"

tests = [
    ("VALERR-102", xml_valid),
    ("XMLERR-001", xml_invalid),
    ("AUTHERR-001", xml_valid),
    ("SUCCESS", xml_valid),
]

for error, xml in tests:
    print(error, "→", localize_error(xml, error))
