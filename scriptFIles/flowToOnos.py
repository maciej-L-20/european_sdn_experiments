import json
import requests
def add_flow(jsonData,switchId, destHost, outPort,connection_type, src_host):
    switchNumber=int(switchId[1:])
    switchHex=hex(switchNumber)[2:]
    deviceId = f'of:000000000000000{switchHex}'
    destHost=f'10.0.0.{destHost[1:]}/32'
    src_host=f'10.0.0.{src_host[1:]}/32'
    port = outPort
    new_flow = {
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
                },
                {
                    "type": "IP_PROTO",
                    "protocol": connection_type
                },
                {
                    "type": "IPV4_SRC",
                    "ip": src_host
                }
            ]
        }
    }
    if connection_type == '0':
        new_flow["selector"]["criteria"].pop(2)
    jsonData["flows"].append(new_flow)

def read_flow_file(roadFile,portMapJson,connectionType='0'):
    jsonData = {"flows": []}
    flowFile = open(roadFile,"r")
    portMap = json.load(open(portMapJson,'r'))
    for line in flowFile:
        flowData = line.strip().split(" ")
        destination=flowData[len(flowData)-1]
        src = flowData[0]
        for i in range(len(flowData)-1):
            device = flowData[i]
            nextDevice = flowData[i+1]
            outPort = find_port(device, nextDevice, portMap)
            add_flow(jsonData,device,destination,outPort,connectionType,src)
    json_data = json.dumps(jsonData, indent=4)
    return json_data

def find_port(device, nextDevice, portMap):
    devIndex = int(device[1:])
    devPorts = portMap[devIndex - 1]["ports"]
    for port in devPorts:
        if port == nextDevice:
            return devPorts.index(port)
    return 0

def flow_to_json_data(flowData,type="0"):
    connection_criteria = "0"
    if type=='TCP':
        connection_criteria = "6"
    elif type == 'UDP':
        connection_criteria = "17"

    portMap = json.load(open('portmap.json','r'))
    jsonData = {"flows": []}
    destination=flowData[len(flowData)-1]
    src=flowData[0]
    for i in range(len(flowData)-1):
        device = flowData[i]
        nextDevice = flowData[i+1]
        outPort = find_port(device, nextDevice, portMap)
        add_flow(jsonData,device,destination,outPort,connection_criteria,src)
    json_data = json.dumps(jsonData, indent=4)
    return json_data


def send_to_onos(flow_data,ip):
    headers = {
   "Content-Type": "application/json",
    "Accept": "application/json"
    }
    auth = ("onos", "rocks")
    requests.post(f'http://{ip}:8181/onos/v1/flows',data=flow_data,headers=headers,auth=auth)

def post_flow(flow,type,ip):
    flow_data = flow_to_json_data(flow,type)
    send_to_onos(flow_data,ip)
    flow_reverse = flow[::-1]
    flow_reverse.pop(0)
    #always send two-way connection because iperf requires thems
    last_index = flow_reverse[len(flow_reverse)-1][1:]
    flow_reverse.append(f'h{last_index}')
    send_to_onos(flow_to_json_data(flow_reverse,type),ip)

def flow_file_to_json_file(flow_file,output_file):
    json_data=read_flow_file(flow_file,'portmap.json')
    output = open(output_file,'w')
    output.write(json_data)

#tcp = read_flow_file("h1_h2TCP.txt","portmap.json",'6')
#udp = read_flow_file("h1_h2UDP.txt","portmap.json",'17')

#tcp_file = open("../lab2/exp/h1_h2/h1_h2TCP.json", "w")
#tcp_file.write(tcp)

#udp_file = open("../lab2/exp/h1_h2/h1_h2UDP.json", "w")
#udp_file.write(udp)