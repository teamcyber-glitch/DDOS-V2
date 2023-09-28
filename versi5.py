import os,time

print("""
\033[1;31;40m____  ____   ___  ____     __     ______
|  _ \|  _ \ / _ \/ ___|    \ \   / /___ \  \33[0;32mEXECUTOR TEAM
\033[1;31;40m| | | | | | | | | \___ \ ____\ \ / /  __) |    \33[0;32mDDOS
\033[1;37;40m| |_| | |_| | |_| |___) |_____\ V /  / __/
|____/|____/ \___/|____/       \_/  |_____|\33[0;32m>(setup)
""") 

print("""\33[0;32m[1] Update\n[2] This Dont Update\nWhich one do you use?""")

c = input(">>: ")
if c == "1":
    print("\033[1;93mPROCESS TO UPDATE....")
    time.sleep(2)
    os.system("rm -rf resources")
    os.system("rm -rf randomstring")
    os.system("unzip randomstring.zip")
    os.system("rm -rf randomstring.zip")
    os.system("unzip resources.zip")
    os.system("rm -rf proxy.txt")
    os.system("clear")
    os.system("cd resources && cp proxy.txt /root/DDOS-V2")
    os.system("clear")
    os.system("cd resources && cp proxy.txt /$HOME/DDOS-V2")
    os.system("clear")
    os.system("rm -rf resources.zip")
    time.sleep(0.8)
    print("\033[1;93mSUCCESFULLY TO UPDATE YOUR TOOLS")
    time.sleep(2)
    os.system("pip3 install -r requirements.txt")
    os.system("cd resources && bash install.sh")
    os.system("rm -rf versi5.py")

elif c == "2":
    os.system("exit")
if os.name == "nt":
    pass
else:
    os.system("clear")