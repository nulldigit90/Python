from scapy.all import *
				
def pk_handler(packet):
	if packet.haslayer(TCP) and packet.haslayer(Raw):
		print packet.getlayer(Raw).load
	
sniff(filter="tcp", prn=pk_handler)
