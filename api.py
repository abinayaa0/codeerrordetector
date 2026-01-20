from fastapi import FastAPI
from pydantic import BaseModel
from engine.orchestrator import process_xml

app = FastAPI()


class XMLRequest(BaseModel):
    xml: str
    error_code: str
    confidence: float


@app.post("/auto-fix-xml")
def auto_fix_xml(req: XMLRequest):
    return process_xml(
        xml=req.xml,
        error_code=req.error_code,
        confidence=req.confidence
    )
