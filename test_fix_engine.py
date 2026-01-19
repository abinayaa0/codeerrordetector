from engine.orchestrator import process_xml

xml = "<KYC><PIN>123</PIN></KYC>"

result = process_xml(
    xml=xml,
    error_code="VALERR-102",
    confidence=0.97
)

print(result)
