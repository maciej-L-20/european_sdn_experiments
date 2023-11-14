curl --user onos:rocks -X POST "http://192.168.67.19:8181/onos/v1/flows/" -d @h2h3.json -H "Content-Type: application/json" -H "Accept: application/json"
curl --user onos:rocks -X POST "http://192.168.67.19:8181/onos/v1/flows/" -d @h4h10.json -H "Content-Type: application/json" -H "Accept: application/json"
curl --user onos:rocks -X POST "http://192.168.67.19:8181/onos/v1/flows/" -d @h8h9.json -H "Content-Type: application/json" -H "Accept: application/json"

pause