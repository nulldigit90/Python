#! /usr/bin/python2
import os, sys

if os.getuid() != 0:
    print "must be root"
    sys.exit()

if len(sys.argv) == 2:
    if sys.argv[1] != "-on" and sys.argv[1] != "-off":
        print "Usage: script.py <-on, -off>"
    elif sys.argv[1] == "-on":
        dest = raw_input("Destination ip and port. <ip:port> ")
        os.system("sysctl net.ipv4.ip_forward=1")
        os.system("iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination %s" % dest)
        os.system("iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination %s" % dest)
    else:
        os.system("sysctl net.ipv4.ip_forward=0")
        os.system("iptables -F")
        os.system("iptables -X")
        os.system("iptables -t nat -F")
        os.system("iptables -t nat -X")
else:
    print "Usage: script.py <-on, -off>"
