import hashlib
import json
from datetime import datetime

def calc_hash(id,ts,msg,prvhsh):
    data=str(id)+ts+msg+prvhsh
    hash=hashlib.sha256(data.encode()).hexdigest()
    return hash
try:
    with open("/home/zxan/log_tamper_detection_using_sha256/data.json",'r') as f:
        logs=json.load(f)
except FileNotFoundError:
    logs=[]


for i in range(3):
    ordin=["First","Second","Third"]
    id=len(logs)+1
    ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg=input(f"Enter the {ordin[i]} log entry: ")
    prvhsh= "0" if len(logs)==0 else logs[-1]["current_hash"]
    crrhsh=calc_hash(id,ts,msg,prvhsh)
    log={
        "index": id,
        "timestamp": ts,
        "message": msg,
        "previous_hash": prvhsh,
        "current_hash": crrhsh
    }
    logs.append(log)


with open("/home/zxan/log_tamper_detection_using_sha256/data.json",'w') as f:
    json.dump(logs,f,indent=4)

print("Logs saved.")


    
