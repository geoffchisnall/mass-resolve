#!/usr/bin/python3
#MASS RESOLVER
#Author: Geoffrey Chisnall
#2020

import subprocess,os,ipaddress,sys
from subprocess import Popen, PIPE, STDOUT

#file with the list
iplist = "list.txt"

#open the file as ipfile
ipfile = open(iplist,'r')
lines = ipfile.readlines()
ipfile.close()

print("Enter DNS server you would like to resolve against.")
#gets the current nameserver the system is using
getcurrentdns = subprocess.Popen("cat /etc/resolv.conf | grep nameserver | awk {'print $2'}",shell=True, stdout=subprocess.PIPE).stdout
currentdns = getcurrentdns.read()
print("Default DNS is %s" % currentdns.strip().decode("UTF-8"))
print("Press ENTER for the default")
dnsserver=input("DNS Server => ")

#open file for writing
dnsresults = open('resolved.txt','w')

#start looping through the 'ipfile' line by line
for ip in lines:
	ip = ip.strip()
	try:
		#this will check if the line is an IP address
		ip = ipaddress.ip_address(ip)
		#checks if IP is IVP4 or IVP6
		if (ip.version == 4) or (ip.version == 6):
			#run the nslookup command for IPs
			nslookup="nslookup %s %s | grep name" % (ip,dnsserver)
			#capture the output
			nslookupresult = subprocess.run(nslookup, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
			#result = (nslookupresult.stdout).strip("\n")
			result = (nslookupresult.stdout).split("\n")
			for line in result:
				if line != '':
					a = (line.split())
					#write to file
					dnsresults.write("%s %s\n" % (ip,a[3]))
		#if no reverse 
		else:
			#write to file
			dnsresults.write("%s %s\n" % (ip, "No reverse found"))
	#this will now take care of the hostnames
	except:
		try:
			#run the nslookup command for addresses
			nslookup="nslookup %s %s | grep Address" % (ip,dnsserver)
			#capture the output
			nslookupresult = subprocess.run(nslookup, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
			result = (nslookupresult.stdout).split("\n")
			for line in result:
				#strip blank lines
				if line != '':
					#strip the nameserver line
					if not ("#53") in line:
						a = (line.split())
						test = (a[1])
						#verify if the IP is valid
						verip = ipaddress.ip_address(test)
						#check if IP is IPV4 or IPV6
						if (verip.version == 4) or (verip.version == 6):
							#write results to file
							dnsresults.write("%s %s\n" % (ip, verip))
		#if no reverse
		except:
			#write to file
			dnsresults.write("%s %s\n" % (ip, "No reverse found"))
#close the file we are writing to
dnsresults.close()
