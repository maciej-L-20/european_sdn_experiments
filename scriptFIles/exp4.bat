curl --user onos:rocks -X POST "http://192.168.1.111:8181/onos/v1/flows/" -d @h1_h2TCP.json -H "Content-Type: application/json" -H "Accept: application/json"
curl --user onos:rocks -X POST "http://192.168.1.111:8181/onos/v1/flows/" -d @h1_h2UDP.json -H "Content-Type: application/json" -H "Accept: application/json"

pause