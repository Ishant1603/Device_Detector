import scapy.all as scapy
import os
import ipaddress 
import json
import socket
import requests


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

def get_hostname(ip):
    """
    Resolve the hostname for a given IP address.
    """
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return "Unknown Host"


def scan(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, retry=2, verbose=False)[0]
        client_list = []

        for element in answered_list:
            ip_address = element[1].psrc
            mac_address = element[1].hwsrc
            hostname = get_hostname(ip_address)
            client_dict = {
                "ip": ip_address,
                "mac": mac_address,
                "hostname": hostname,
            }
            client_list.append(client_dict)

        return client_list
    except Exception as e:
        print(f"Error during scanning: {e}")
        return []