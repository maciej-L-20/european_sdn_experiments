#!/usr/bin/bash


sudo rm -f main.py 2>/dev/null
sudo rm -f cities 2>/dev/null
sudo rm -f links 2>/dev/nul
sudo rm -f /usr/lib/python3.8/prep.py 2>/dev/null
sudo pip3 install requests
sudo pip3 install geopy
sudo wget "http://$1:8000/main.py"
sudo wget "http://$1:8000/prep.py"
sudo wget "http://$1:8000/cities"
sudo wget "http://$1:8000/links"

sudo mv prep.py /usr/lib/python3.8
sudo -E mn --custom=main.py --topo mytopo --link tc
