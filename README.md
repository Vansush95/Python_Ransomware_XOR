# Python_Ransomware
Simple Encryption/Decryption Script 
This is for demonstration purpose only , not intended for malicious activities 
Basically it is a python based ransomware(ransom.py) , that is capable of encrypting files in your Computer machine , mainly tested on windows .
It is uses XOR cryptography to encrypt the files content and make them unrecognisable and unreadable.
Once the files has been ecnrypted , the same key can be used to decrypt them using the Decryptor.py script .


**HOW IT WORKS ?**

# **ransom.py - ** 

STEP1 : To avoid any unnecessary damage to the mcahine we are perfoming the demonstration to , a _safeguard_ has been put in place to after the program is executed.
To proceed with the experimentation , type _y_ (lowercase) .

STEP 2 : Within the the sample code , when the _os.walk_ function is called , it will grab all the file present in the mentionned directory . so before launching this program be sure to paste there the path of test folder to encrypt .

STEP 3 : When the program is running , we have implemented multi-threading function to execute the listing of all the files within the above mentionned path .

STEP 4 : A random key will be generated to used to encrypt the files ,everytime the progeam run , it changes .

STEP 5 : All the selected files will be encrypted using **_XOR algorithm _** , that means the same file used to encrypt the files is the key used to decrypt the files.

# **decryptor.py -**  
This will decrypt the file using the current generated key .
