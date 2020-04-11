#!/usr/bin/python
#MASS RESOLVER
#Version 2.1
#Author: Geoffrey Chisnall
#2018

import subprocess,os,ipaddress
from subprocess import Popen, PIPE, STDOUT

iplist = "list.txt"

ipfile = open(iplist,'rb')
lines = ipfile.readlines()
ipfile.close()

print ("Enter DNS server you would like to resolve against.")
getcurrentdns = subprocess.Popen("cat /etc/resolv.conf | grep nameserver | awk {'print $2'}",shell=True, stdout=subprocess.PIPE).stdout
currentdns = getcurrentdns.read()
print ("Default DNS is %s" % currentdns.strip())
print ("Press ENTER for the default")
dnsserver=raw_input("DNS Server => ")

dnsresults = open('resolved.txt','w')
for ip in lines:
    ip = ip.strip()
    try:
      ip = unicode(ip, "utf-8")
      ip = ipaddress.ip_address(ip)
      if (ip.version == 4) or (ip.version == 6):
        nslookup="nslookup %s %s | grep name" % (ip,dnsserver)
        nslookupresult = subprocess.check_output(nslookup, shell=True).split("\n")
        for line in nslookupresult:
          if line != '':
            a = line.split()
            if len(a) == 4:
              dnsresults.write("%s %s\n" % (ip,a[3]))
      else:
        dnsresults.write("%s %s\n" % (ip, "No reverse found"))
    except:
      try:
        nslookup="nslookup %s %s | grep Address" % (ip,dnsserver)
        nslookupresult = subprocess.check_output(nslookup, shell=True).split("\n")
        for line in nslookupresult:
          if line != '':
            if not ("#53") in line:
              b = line.split()
              if len(b) == 2:
                ip2 = ip,b[1]
                test = b[1]
                test = unicode(test, "utf-8")
                verip = ipaddress.ip_address(test)
                if (verip.version == 4) or (verip.version == 6):
                  ip3 = ip2[0],ip2[1]
                  dnsresults.write("%s %s\n" % (ip3))
      except:
        dnsresults.write("%s %s\n" % (ip, "No reverse found"))
print ("Results have been saved to resolved.txt")
dnsresults.close()
