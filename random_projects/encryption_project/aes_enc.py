import re
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


from RSA import *
from file_reading import *
  
#cartella algorithm_exam path   Users/davidevalentini/Desktop/Algorithm_exam


def pkcs7_pad(data,size):
    
    pad_value = size - len(data) % size
    padded_data = data + '0' * pad_value
    
    return padded_data



def enc_msg(file, file_name):

  #General preparation before encryption
  file_name=re.sub(r'.txt','',file_name)
  
  key=str(input('\nInsert a password for this file (do not use a password which is too long) : '))

  #Ensure the key is 16, 24, or 32 bytes in length (AES-128, AES-192, or AES-256)
  key = key.ljust(32,'0')[:32]
  key=key.encode()
  
  #Generate a random initialization vector, aka I'm getting ready to pad both the key and file that I want to encrypt
  iv =b'\x00' * 16 #os.urandom(16)
#creates a cipher to encrypt the file
  cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
  encryptor = cipher.encryptor()
  
  #pad the file to be a multiple of 16 bytes
  file = pkcs7_pad(file, 16).encode()
  
  #Encrypt the padded and encoded text
  enc_file = encryptor.update(file) + encryptor.finalize()
  
  #enc_file= iv + enc_file
   #here I save the AES encrypted file
  file_path='/Users/davidevalentini/Desktop/Algorithm/enc_files'
  file_name=file_name+'_enc'
  
  file_writer(enc_file, file_name,file_path,'.txt')

    
    
      # encryption of the password
  key=str_to_ascii(key)
  enc_pass=rsa_enc(key,file_name)
  
  dict_name='main'; file_name=file_name+'.txt' #file_name lastly unified
  dictionary_uploader( dict_name ,file_name, enc_pass)  #I upload/add a new element to the dictionary with file_name <-> [c,puk]
  
  return

def dec_msg(f_name):

  dir_path='/Users/davidevalentini/Desktop/Algorithm/enc_files'
  file=file_reader(dir_path,f_name, 1)
   
  #password modelling, I have all inside password cecker, also the padding
  key=password_cecker(f_name)
  #I need to retrive the initialization vector and the actual file
  iv =b'\x00' * 16 #file[:16]
  #file=file[16:]

  cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
  decryptor = cipher.decryptor()
 
  # Decrypt the ciphertext
  dec_msg = decryptor.update(file) + decryptor.finalize()

  dec_msg= dec_msg.decode(errors='ignore')
  print("Final Decrypted Content:", dec_msg)
    
  path='/Users/davidevalentini/Desktop/Algorithm/clear_files'
  file_name=f_name+'_decrypted'
  file_writer(dec_msg,file_name,path, '.txt')

  return
