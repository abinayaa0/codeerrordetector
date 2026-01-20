from engine.orchestrator import process_xml

xml = "<KYC><DOB>25-12-1990</DOB></KYC>"

result = process_xml(
    xml=xml,
    error_code="VALERR-103",
    confidence=0.95
)

print(result)
