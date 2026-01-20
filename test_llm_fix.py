from engine.orchestrator import process_xml

broken_xml = "<KYC><PIN>123</PIN>"

result = process_xml(
    xml=broken_xml,
    error_code="XMLERR-001",
    confidence=0.95
)

print(result)



