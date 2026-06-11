import json
entry={}
id=int(input("Enter id: "))
msg=input("Enter message: ")
entry['id']=id
entry['message']=msg
with open('data.json','r') as f:
    data=json.load(f)
data.append(entry)
with open('data.json','w') as f:    
    json.dump(data, f,indent=4)