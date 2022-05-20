# pyta cie o haslo wstepu, wczytuje hasla z pliku, wyswietla hasla
from cryptography.fernet import Fernet
from os import path

def loadKey():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

fileaccess = True
firstTime = False
with open('psw.txt', 'r') as file:
    firstline = file.readline().strip()
    if firstline == "":
        firstTime = True
    else:
        psw = input('Enter password: ')
        if psw == file.readline().strip():
            fileaccess = True

if fileaccess:
    passwords = []
    if firstTime:
        psw = ""
        while not psw:
            psw = input("Set password: ")
        passwords.append(psw)
    else:
        with open('psw.txt', 'r') as file:
            passwords.append(file.readline().strip())
        
    if not path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as file:
            file.write(key)
            
    key = loadKey() + passwords[0].encode()
    fr = Fernet(key)
            
    with open('psw.txt', 'r') as file:
        for k,v in enumerate(file.readlines()):
            if k == 0:
                continue
            thisline = v.split()
            thisline[2] = fr.decrypt(thisline[2].encode()).decode()
            print("({}) {} {}:{}".format(k, thisline[0], thisline[1], thisline[2]))
            passwords.append(thisline)
            
    # functions
    def showPasswords():
        if len(passwords) > 1:
            for k,v in enumerate(passwords):
                if k!=0: print("({}) {} {}:{}".format(k,v[0], v[1], v[2]))
            
    def showNotify(msg):
        print("=======================================")
        print(msg)
        print("=======================================")
        
    def updatePasswords():
        with open("psw.txt", "w") as file:
            for k,v in enumerate(passwords):
                if k == 0:
                    file.write("{}\n".format(v))
                    continue
                file.write("{} {} {}\n".format(v[0], v[1], fr.encrypt(v[2].encode()).decode()))
            
    while True:
        print('Actions: Add account (A) / Delete account (D) / Edit account (G) / Change password (X) / Exit (E)')
        act = input()
        if act and act.isalpha():
            act = act.lower()
            if act == "a" or act == "add":
                nickname, passw, label = "", "", ""
                while not label:
                  label = input("Enter label: ").upper().strip()
                while not nickname:
                  nickname = input("Enter name/email: ").strip()
                while not passw:
                    passw = input("Enter password: ").strip()
                passwords.append([label, nickname, passw])
                showNotify("Succesfully added - {} {}:{}".format(label, nickname, passw))
                updatePasswords()
                showPasswords()
            elif act == "d" or act == "delete":
                index = ""
                while not index:
                    index = int(input("Enter index to delete: "))
                showNotify("Succesfully removed - {} {}:{}".format(passwords[int(index)][0], passwords[int(index)][1], passwords[int(index)][2]))
                passwords.pop(index)
                showPasswords()
                updatePasswords()
            elif act == "e" or act == "exit":
                break
            elif act == "g" or act == "edit":
                index = ""
                while not index:
                    index = int(input("Enter index to edit: "))
                    try:
                        passwords[index] = passwords[index]
                    except IndexError:
                        index = ""
                while True:
                    print(passwords[index])
                    optioners = input("Edit label (L) / Edit name/email (N) / Edit password (P) / Return (R)").lower()
                    if optioners == "l" or optioners == "label":
                        passwords[index][0] = input("Enter new label: ").upper()
                        updatePasswords()
                        showNotify("Changed label succesfully.")
                    elif optioners == "n" or optioners == "name":
                        passwords[index][1] = input("Enter new name/email: ")
                        updatePasswords()
                        showNotify("Changed name/email succesfully.")
                    elif optioners == "p" or optioners == "password":
                        passwords[index][2] = input("Enter new password: ")
                        updatePasswords()
                        showNotify("Changed password succesfully.")
                    elif optioners == "r" or optioners == "return":
                        showPasswords()
                        break
            elif act == "x" or act == "change":
                passwords[0][0] = input("Enter new secret password: ")
                updatePasswords()
                showNotify("Changed secret password succesfully.")
else:
    print('Access denied.')