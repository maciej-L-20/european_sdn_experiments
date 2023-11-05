import json
import requests
def add_flow(jsonData,switchId, destHost, outPort):
    switchNumber=int(switchId[1:])
    switchHex=hex(switchNumber)[2:]
    deviceId = f'of:000000000000000{switchHex}'
    destHost=f'10.0.0.{destHost[1:]}/32'
    port = outPort
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

def read_flow_file(roadFile,portMapJson):
    jsonData = {"flows": []}
    flowFile = open(roadFile,"r")
    portMap = json.load(open(portMapJson,'r'))
    for line in flowFile:
        flowData = line.strip().split(" ")
        destination=flowData[len(flowData)-1]
        print(destination)
        for i in range(len(flowData)-1):
            device = flowData[i]
            nextDevice = flowData[i+1]
            outPort = findOutPort(device,nextDevice,portMap)
            add_flow(jsonData,device,destination,outPort)
    json_data = json.dumps(jsonData, indent=4)
    return json_data

def findOutPort(device,nextDevice,portMap):
    devIndex = int(device[1:])
    print(devIndex)
    devPorts = portMap[devIndex - 1]["ports"]
    for port in devPorts:
        if port == nextDevice:
            return devPorts.index(port)
    return 0

def postFlow(flowFile,portMap,ip):
    headers = {
   "Content-Type": "application/json",
    "Accept": "application/json"
    }
    auth = ("onos", "rocks")
    requests.post(f'http://{ip}:8181/onos/v1/flows',data=read_flow_file(flowFile,portMap),headers=headers,auth=auth)

portMap = "portmap.json"
postFlow("VilniusDublin.txt",portMap,"192.168.67.19")