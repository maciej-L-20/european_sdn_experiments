import json
import requests
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

def read_flow_file(roadFile,portMapJson):
    jsonData = {"flows": []}
    flowFile = open(roadFile,"r")
    portMap = json.load(open(portMapJson,'r'))
    for line in flowFile:
        flowData = line.strip().split(" ")
        destination=flowData[len(flowData)-1]
        for device in flowData[:len(flowData)]:
            devIndex = int(device[1:])-1
            nextDevIndex= int(device[1:])-1
            devPorts = portMap[devIndex]["ports"]
            #jak uzyskać następny device, metoda ma printować kolejne porty
            port = devPorts.index()
            print(devPorts)
            #add_flow(jsonData,device,destination,flowData[2])
    #json_data = json.dumps(jsonData, indent=4)
    #return json_data
""""
headers = {
   "Content-Type": "application/json",
    "Accept": "application/json"
}
auth = ("onos", "rocks")
requests.post("http://192.168.67.19:8181/onos/v1/flows",data=read_flow_file("WarsawParis.txt"),headers=headers,auth=auth)
"""

read_flow_file("WarsawParis.txt","portmap.json")