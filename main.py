import os
import json
import datetime
import time
import re
import requests

webhook_url = "https://discord.com/api/webhooks/1127315513299706076/zLYR4QyosBa9L1ozlXBvJ-DC4a2AeS2qzGyFIBbACNdyNZ4bT1OujuHptZ0SrsKkMcuO"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print( bcolors.OKCYAN + '''
     _  _____   __   ___ _____ ____  
    | |/ _ \ \ / /  / _ \_   _|  _ \ 
 _  | | | | \ V /  | | | || | | |_) |
| |_| | |_| || |   | |_| || | |  __/ 
 \___/ \___/ |_|    \___/ |_| |_|
''')
print(bcolors.BOLD + f"[!] Welcome To Joy SMS Forwarder\n")


def smsforward():
    lastSMS = datetime.datetime.now()
    tmpFile = "tmpLastTime.txt"
    filters = ["minutes", "Valid", "Secret"]  # Add your filters here
    headers = {'Content-Type': 'application/json'}

    if not os.path.exists(tmpFile):
        print(bcolors.WARNING + "[!] Last Time Not found, Setting It Up")
        tfile = open(tmpFile, "w")
        tfile.write(str(lastSMS))
        tfile.close()
    else:
        tfile = open(tmpFile, "r")
        lastSMS = datetime.datetime.fromisoformat(tfile.read())
        tfile.close()

    jdata = os.popen("termux-sms-list").read() 
    jd = json.loads(jdata)

    for j in jd:
        if datetime.datetime.fromisoformat(j['received']) > lastSMS: 
            for f in filters:
                if f in j['body'].lower() and j['type'] == "inbox":  
                    print("[!] Found A Otp Message, Forwarding To Discord...")
                    fullmsg = j['body']
                    numbers = re.findall(r'\d+', j['body']) 
                    numbers_str = ', '.join(numbers)
                    embed = {
                        "title": f"> {fullmsg}",
                        "description": f"```{numbers_str}```",
                        "author": {
                            "name": "OTP SMS FORWARDER BY JOY",
                            "icon_url": "https://cdn.discordapp.com/emojis/1052840053950402600.png"
                        },
                        "thumbnail": {
                            "url": "https://cdn.discordapp.com/emojis/1127296081710039180.png"
                        },
                        "footer": {
                            "text": "Forwarded From Smart Phone by SMS Forwarder",
                            "icon_url": "https://cdn.discordapp.com/emojis/1095997599036739594.png"
                        },
                        "color": 0x00FF00
                    }
                    payload = {
                        "embeds": [embed]
                    }
                    response = requests.post(webhook_url, headers=headers, json=payload) 
                    if response.status_code == 204:
                        print(bcolors.BOLD + bcolors.OKBLUE + "[+] Successfully Forwarded Message To Discord ")
                        tfile = open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()
                    else:
                        print(bcolors.FAIL + "[!] Failed To Forward Message To Discord\n[!] Please Double Check If Everything Is Ok")

smsforward()

while True:
    time.sleep(1)
    smsforward()
