import json

def add_flow(jsonData,switchId, destHost, outPort):
    switchNumber=int(switchId[1:])
    switchHex=hex(switchNumber)[2:]
    deviceId = f'of:000000000000000{switchHex}'
    destHost=f'10.0.0.{destHost[1:]}/32'
    port = outPort[1:]
    nowy_flow = {
        "priority": 40000,
        "timeout": 0,
        "isPermanent": True,
        "deviceId": deviceId,
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": port
                }
            ]
        },
        "selector": {
            "criteria": [
                {
                    "type": "ETH_TYPE",
                    "ethType": "0x0800"
                },
                {
                    "type": "IPV4_DST",
                    "ip": destHost
                }
            ]
        }
    }
    jsonData["flows"].append(nowy_flow)

def read_flow_file(inputFile,outPutFile):
    jsonData = {"flows": []}
    flowFile = open(inputFile,"r")
    for line in flowFile:
        flowData = line.strip().split(" ")
        add_flow(jsonData,flowData[0],flowData[1],flowData[2])
    json_data = json.dumps(jsonData, indent=4)
    json_file = open(outPutFile,"w")
    json_file.write(json_data)

read_flow_file("WarsawParis.txt","h2h3.json")