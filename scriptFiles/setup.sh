#!/usr/bin/bash

while getopts ":h:vm" opt; do
  case "$opt" in
    h)
      hostIp="$OPTARG"
      ;;
    vm)
      vmIp="$OPTARG"
      ;;
    \?)
      echo "Nieprawidłowa opcja: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

sudo rm -f main.py 2>/dev/null
sudo rm -f cities 2>/dev/null
sudo rm -f links 2>/dev/null
sudo rm -f /usr/lib/python3.8/prep.py 2>/dev/null
sudo pip3 install requests
sudo pip3 install geopy
sudo wget "http://${hostIp}:8000/main.py"
sudo wget "http://${hostIp}:8000/prep.py"
sudo wget "http://${hostIp}:8000/cities"
sudo wget "http://${hostIp}:8000/links"

sudo mv prep.py /usr/lib/python3.8
