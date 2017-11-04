import os, re

# Could expand to see which interface is UP or DOWN
#  also could use to get local mac address as well
def getInterfaces():
	raw = os.popen("ip link show").read()
	interface = re.findall(r"\d: \w+:", raw)
	for i in interface:
		print i[:-1]
