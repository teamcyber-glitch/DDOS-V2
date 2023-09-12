import os

print("""
\033[1;31;40m____  ____   ___  ____     __     ______
|  _ \|  _ \ / _ \/ ___|    \ \   / /___ \  \33[0;32mEXECUTOR TEAM
\033[1;31;40m| | | | | | | | | \___ \ ____\ \ / /  __) |    \33[0;32mDDOS
\033[1;37;40m| |_| | |_| | |_| |___) |_____\ V /  / __/
|____/|____/ \___/|____/       \_/  |_____|\33[0;32m>(setup)
""") 

print("""\33[0;32m[0] pip\n[1] pip3\nWhich one do you use?""")

c = input(">>>: ")
if c == "0":
    os.system("unzip resources.zip")
    os.system("rm -rf resources.zip")
    os.system("pip install cloudscraper")
    os.system("pip install socks")
    os.system("pip install pysocks")
    os.system("pip install colorama")
    os.system("pip install undetected_chromedriver")
    os.system("pip install httpx")
    os.system("cd resources && mv proxy.txt /$HOME/DDOS-V2")
    os.system("cd resources && mv proxy.txt /root/DDOS-V2")
    os.system("cd resources && mv proxy.txt /home/kali/DDOS-V2")
    os.system("rm -rf powerup.py")

elif c == "1":
    os.system("unzip resources.zip")
    os.system("rm -rf resources.zip")
    os.system("pip3 install cloudscraper")
    os.system("pip3 install socks")
    os.system("pip3 install pysocks")
    os.system("pip3 install colorama")
    os.system("pip3 install undetected_chromedriver")
    os.system("pip3 install httpx")
    os.system("cd resources && mv proxy.txt /$HOME/DDOS-V2")
    os.system("cd resources && mv proxy.txt /root/DDOS-V2")
    os.system("cd resources && mv proxy.txt /home/kali/DDOS-V2")
    os.system("rm -rf powerup.py")
if os.name == "nt":
    pass
else:
    os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    os.system("apt-get install ./google-chrome-stable_current_amd64.deb")

print("\33[0;32m[ √ ] S U C C E S S F U L L Y")
