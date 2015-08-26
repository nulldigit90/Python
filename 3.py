txt = """g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc 
dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm 
jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""

txtn = ""

for i in txt:
  if ord(i) in range(65,91) or ord(i) in range(97,123):
    txtn += chr(ord(i)+2)
    print i, ord(i)+2, chr(ord(i)+2)
  else:
    txtn += i

print txtn
