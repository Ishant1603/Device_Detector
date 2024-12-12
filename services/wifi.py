import scapy.all as scapy
import os
import ipaddress 
import json
#import socket
#import requests


DEVICE_FILE = "devices.json"
def load_devices():
    if not os.path.exists(DEVICE_FILE):
        with open(DEVICE_FILE, 'w') as file:
            json.dump([],file)
    try:
        with open(DEVICE_FILE,'r') as file:
            devices = json.load(file)
    except json.JSONDecodeError:
        devices = []
    return devices            


def save_devices(devices):
    with open(DEVICE_FILE,'w') as file:
        json.dump(devices,file,indent=4)

# def get_mac_vendor(mac):
#     """
#     Fetch vendor information based on the MAC address using an API.
#     """
#     try:
#         response = requests.get(f"https://macvendors.co/api/{mac}", timeout=5)
#         data = response.json()
#         return data.get("result", {}).get("company", "Unknown Vendor")
#     except Exception as e:
#         print(f"Error fetching vendor: {e}")
#         return "Unknown Vendor"

def scan(ip):
    print("searching...")
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, retry=0,verbose=False)[0]
    client_list = []

    for element in answered_list:
        client_dict = {"ip": element[1].psrc , "mac":element[1].hwsrc}
        client_list.append(client_dict)
    
    return client_list

