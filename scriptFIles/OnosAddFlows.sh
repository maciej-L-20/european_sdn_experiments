curl --user onos:rocks -X POST "http://$1:8181/onos/v1/flows" -d @$2 -H "Content-Type: application/json" -H "Accept: application/json"
