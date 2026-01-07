import json
import random
import uuid
from copy import deepcopy

BASE_REQUEST = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
 <Body>
 <InsertUpdateKYCRecord xmlns="https://pancheck.www.kracvl.com">
  <webApi>
   <inputXml><![CDATA[
<ROOT>
  <HEADER>
    <COMPANY_CODE>1500000021</COMPANY_CODE>
    <BATCH_DATE>24/12/2025</BATCH_DATE>
  </HEADER>
  <KYCDATA>
    <APP_PAN_NO>{pan}</APP_PAN_NO>
    <APP_NAME>{name}</APP_NAME>
    <APP_COR_PINCD>{pincode}</APP_COR_PINCD>
    <APP_DOB_INCORP>{dob}</APP_DOB_INCORP>
    <APP_UID_NO>{uid}</APP_UID_NO>
  </KYCDATA>
</ROOT>
]]></inputXml>
   <pan>{pan}</pan>
   <userName>{user}</userName>
   <posCode>1500000021</posCode>
   <password>{pwd}</password>
   <passKey>{key}</passKey>
  </webApi>
 </InsertUpdateKYCRecord>
</Body>
</Envelope>"""

ERROR_TYPES = [
 ("VALERR-002","PAN MANDATORY","validation", lambda r: r.replace("{pan}", "")),
 ("VALERR-102","INVALID PINCODE","validation", lambda r: r.replace("{pincode}", "ABCDEF")),
 ("VALERR-103","INVALID DATE FORMAT","validation", lambda r: r.replace("{dob}", "1983/05/22")),
 ("AUTHERR-001","INVALID USER/PASSWORD","auth", lambda r: r.replace("{user}", "BADUSER")),
 ("BUSERR-310","APPLICATION NO DUPLICATE","business", lambda r: r),
 ("WEBERR-005","UNKNOWN ERROR","web", lambda r: r),
 ("XMLERR-001","MALFORMED XML","syntax", lambda r: r.replace("</KYCDATA>","")),
]

BASE_RESPONSE = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
 <Body>
  <InsertUpdateKYCRecordResponse xmlns="https://pancheck.www.kracvl.com">
    <InsertUpdateKYCRecordResult>
      <ROOT>
       <ERROR>
         <ERROR_CODE>{code}</ERROR_CODE>
         <ERROR_MSG>{msg}</ERROR_MSG>
       </ERROR>
      </ROOT>
    </InsertUpdateKYCRecordResult>
  </InsertUpdateKYCRecordResponse>
 </Body>
</Envelope>"""

def make_valid():
    return (
        BASE_RESPONSE.replace(
            "<ERROR>", "<SUCCESS><KYC_STATUS>ACCEPTED</KYC_STATUS>"
        ).replace("</ERROR>", "</SUCCESS>"),
        "success",
        "OK"
    )

def random_line():
    pan = random.choice(["ALIPD4849D","", "ABCDE1234F"])
    name = random.choice(["PANKAJ R DERE","", "TEST USER"])
    pincode = random.choice(["421202","000000","ABCDE"])
    dob = random.choice(["22/05/1983","1983/05/22",""])
    uid = random.choice(["1687","", "123"])
    user = "CVL_MFU"
    pwd = "NhCMnZ2AIWCUwWbF8vkYuQ!3d!3d"
    key = "ed9094b83db04ac18940b5170a02ce24"

    request = BASE_REQUEST.format(
        pan=pan, name=name, pincode=pincode, dob=dob, uid=uid,
        user=user, pwd=pwd, key=key
    )

    if random.random() < 0.3:
        # valid case
        resp, t, msg = make_valid()
        code = "SUCCESS"
    else:
        err = random.choice(ERROR_TYPES)
        code, msg, t, mutator = err
        request = mutator(request)  # inject error
        resp = BASE_RESPONSE.format(code=code, msg=msg)

    return {
        "id": str(uuid.uuid4()),
        "type": t,
        "error_label": code,
        "request_xml": request,
        "response_xml": resp,
        "notes": msg
    }

with open("kyc_errors.jsonl","w",encoding="utf8") as f:
    for _ in range(100):
        json.dump(random_line(), f)
        f.write("\n")

print("✔ Generated kyc_errors.jsonl with 100 samples")
