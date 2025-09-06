import pyDes as pds
import re
import os

from RSA import *
from file_reading import *


def pass_trans(p_word):

    l=len(p_word.encode('utf-8'))
    
    while l!= 8:
    
        if l<8:
            p_word=p_word+'a'
            l=len(p_word.encode('utf-8'))
            
        if l>8:
            p_word=p_word.rstrip(p_word[-1])
            l=len(p_word.encode('utf-8'))

    
    return p_word
    
    
def list_filler(x,data_len):
   
    for k in range(data_len):
        x.append(0)
    
    return x
    
    
    
#function which returns a list of maximum 8 bit lenght for each element
def divide_data(data, byte_length):

#Initialization
    result_list = []
    current_byte_length = 0
    current_substring = ""

    for x in data:
    #I retrieve info over the current lenght of the char in consideration (I'm working with strings
        x_byte_length = len(x.encode('utf-8'))

    #I'm checking if I've already reached the wanted number of bytes, if not I'm adding another character and therefore "enlarging" the byte length of the string
        if current_byte_length + x_byte_length <= byte_length:
            current_substring += x
            current_byte_length += x_byte_length
        else:
            result_list.append(current_substring.encode('utf-8'))
            current_substring = x
            current_byte_length = x_byte_length

    #I'm appending what is left and I need to check that what is left has length 8, if not I add forcefully some bytes
    k='0'
    if current_substring:
        
        str_len=len(current_substring)
    
    while str_len<byte_length:
            current_substring += k
            str_len=len(current_substring)
            
    result_list.append(current_substring.encode('utf-8'))

    return result_list
    
    
def string_byte_completer(b_string, size):
    #Here I'm computing the bytes needed to make the string with the length multiple of what I desire
    str_compl= (size - len(b_string)%size)%size
    #string which will complete the wanted str
    completer_str= b'\x00' * size
    #string completed with the completer by a join
    completed_str= b_string + completer_str
    
    return completed_str

    

#cartella algorithm_exam path   Users/davidevalentini/Desktop/Algorithm_exam
    
 #main function to encrypt our message, password is encrypted using RSA
def enc_msg(file, file_name):

  #General preparation before encryption
  file_name=re.sub(r'.txt','',file_name)
  
  password=str(input('\nInsert a password for this file (do not use a password which is too long) : '))
  
  des_password=pass_trans(password)#.to_bytes(8, byteorder='big')  #Convert the numeric value into an 8-byte string
  
  #Since file is a single string, I'm dividing it in a list of substing each with byte length 8 (already encoded)
  file=file.encode('utf-8'); file=string_byte_completer(file, 8)
  #file=divide_data(file, 8)
  
  key = pds.des(des_password, pds.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pds.PAD_PKCS5)
  
  #I'm encrypting 8-bytes by 8-bytes, since I cannot do all togheter
  #I'm prefilling a list to avoid errors
  #enc_file=[]
  #enc_file=list_filler(enc_file,len(file))
  
  #for x in range(len(file)):
    
  enc_file = key.encrypt(file)

  #I need now to "remove" the list and put all in one variable, in this way when I'm writing over the file I will not have [ , ] all over (which are not part of the encryption
  #I am joining the byte string using "space" as separator since it's a char which do not appear with this encryption
  #enc_file = b' '.join(b for b in enc_file_list)

 
  #here I save the DES encrypted file
  file_path='/Users/davidevalentini/Desktop/Algorithm/enc_files'
  file_name=file_name+'_enc'
  
  file_writer(enc_file, file_name,file_path,'.txt')

  # encryption of the password
  password=str_to_ascii(password)
  enc_pass=rsa_enc(password,file_name)
  
  dict_name='main'; file_name=file_name+'.txt' #file_name lastly unified
  dictionary_uploader( dict_name ,file_name, enc_pass)  #I upload/add a new element to the dictionary with file_name <-> [c,puk]

  return

    #main function used to decrypt
def dec_msg(n,f_name):
  
  dir_path='/Users/davidevalentini/Desktop/Algorithm/enc_files'
  file=file_reader(dir_path,f_name)
  file=file[2:-1]
  

#I need to clean the file, since I've saved a list, therefore there are at the beginning and at the end [ ], then I'm splitting it knowing that between each element there is a ", "
  #file=file[1:-1]
  #file=file.split(", ")
  # now I need to remove all initial b' and last '  equivalently with ", otherwise I have data corruption, therefore I remove from each element the first 2 and the last one
  #for i in range(len(file)):
   # file[i]=file[i][2:-1]
   # file[i]=file[i].encode('utf-8')
 

  #password modelling
  password=password_cecker(f_name)
  password=pass_trans(password)
  des_password=bytes(password, encoding='utf-8')
  
  #I decrypt the des message
  key = pds.des(des_password, pds.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pds.PAD_PKCS5)
  #Initialization of the decryption list
  #dec_file_list=[];
  #dec_file_list=list_filler(dec_file_list, len(file))
    
#I have problem with last element since it has not byte size 5, so what I do is add something,therefore:
 
 # for x in range(len(file)-1):
  
  dec_file = key.decrypt(file, padmode=pds.PAD_PKCS5)

  
  path='/Users/davidevalentini/Desktop/Algorithm/clear_files'
  file_name=f_name+'_decrypted'
  file_writer(dec_file,file_name,path, '.txt')
  
  return
