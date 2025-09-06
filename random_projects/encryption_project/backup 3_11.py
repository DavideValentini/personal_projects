import pickle
from pyDes import *
import math
import random
import re
import sympy
import unicodedata
import os

from RSA import *


#cartella algorithm_exam path   Users/davidevalentini/Desktop/Algorithm_exam



def choice():

    print('would you like to encrypt (0) or decrypt (else) a file.txt?')
    s=str(input())

    if s=='0':
    
        print('be carefull, after this process the original file will be deleted, the only way to retrieve it will be through the key that will be generated, keep it!')
        
        #file_name=str(input('inserisci nome file che vuoi criptare:'))
        file_name=str(input('Insert the name of the clear file you want to encrypt: '))
        file_path='/Users/davidevalentini/Desktop/Algorithm_exam/clear_files'
        #print('sei sicuro del nome? y or n')
        #q=input()
        #while q=='n':
            #print('inserisci nome file che vuoi criptare:')
            #file_name=str(input())
            #print('sei sicuro del nome? y or n')
            #q=input()
        sup=file_reader(file_path, file_name) #since it returns a list, I'm not sure if I can do file_reader(file_name)[0]
        file=sup[0]
        enc_msg(file,file_name)
        print('the file has been encrypted, you will find it on your pc (should be in the same directory of this script)')
        return
    else:
    
        print('you want to decrypt something that is encrypt, hope for you everything goes well...')
        
        dict_name='main'#str(input('insert name of the file you want to decrypt: '))+'.pkl'
        dict=dictionary_reader(dict_name)
        print(dict)
        
        file_name=str(input('file name:'))
        #I check that there exists a file whith this name, if yes I retrieve n and the encrypted file
        while file_name not in dict:
           q=str(input('file not found, do you want to search for another file? yes(0), no(else)'))
           if q != '0':
              exit()
           else:
              file_name=str(input('file name:'))
              
        n=dict[file_name]
        
        dec_msg(n, file_name)
              
        
              
       
  
    
    return
    
   #########################################
   
   #function to ceck that
def password_cecker(file_name):   #Non funziona il controllooooooooo
    
   #To check that this is the right password I don't need the prk, I just check that the trasformation of p_word and c encrypted password coincide
   p_word=str(input('Insert password to decrypt: '))
   ascii_pass=str_to_ascii(p_word)
   
   # I retrieve info over the ecrypted password ### [c, puk] ###
   path='/Users/davidevalentini/Desktop/Algorithm_exam/dictionary'
   sup=dictionary_reader('main')[file_name]
   c=sup[0]; puk=sup[1]
   
   i=0; cp=pow(ascii_pass, puk[1], mod=puk[0])  #p_word^e mod n
   
   
   while cp != c and i<3:
    
    j=3-i
    print(cp)
    print('Look out, you only have another '+str(j)+' trials, then you will be expelled (and maybe in future the file destroyed)')
    p_word=str(input('Insert password to decrypt: '))
    ascii_pass=str_to_ascii(p_word)
    
    cp=pow(ascii_pass, puk[1], mod=puk[0])
    i+=1
    
    if i>=3:
        
        print('You failed to remember the right password, adios')
        exit(1)

   return p_word
    
    
    


#function used to read from files
def file_reader(dir_path, file_name):

  c=os.getcwd()
  os.chdir(dir_path)
  
  file_tmp = open(os.path.join(dir_path, file_name), "r") #in this way we can read files from different directories
  text= file_tmp.read()
  file_tmp.close()
  
  os.chdir(c)
  
  return text
  
  
  
  
#function to write a new file
def file_writer(m,file_name,dir_path, format):

    c=os.getcwd()
    os.chdir(dir_path)

    m=str(m)
    enc_file=re.sub(r'.txt','',file_name)+format
    with open(enc_file, 'w') as file:
        file.write(m)
        
    file.close()
        
    os.chdir(c)
        
    return
    
    
    
def dictionary_uploader(dict_name,pos,n):  #function to save file <-> key c (encrypted)

    c=os.getcwd()
    #os.chdir(dir_path)
    os.chdir('/Users/davidevalentini/Desktop/Algorithm_exam/dictionary')
    
    dict_name=re.sub(r'.pkl','',dict_name)
    dict_file_up=dict_name+'.pkl'
    dict=dictionary_reader(dict_file_up)
    
    dict[pos]=n
    
    with open(dict_file_up, 'wb') as fp:
        pickle.dump(dict, fp)
        
    os.chdir(c)
    
    return
    


def dictionary_reader(dict_name): #function to read a dictionary enc_file <-> c
    
    
    c=os.getcwd()
    #os.chdir(dir_path)
    os.chdir('/Users/davidevalentini/Desktop/Algorithm_exam/dictionary')
    dict_name=re.sub(r'.pkl','',dict_name)
    dict_file_r=dict_name+'.pkl'
    
    with open(dict_file_r, 'rb') as fp:
        dict = pickle.load(fp)
    
    os.chdir(c)
    
    return dict
    
    
    
    
  
  #function to convert string to ascii
def str_to_ascii(m):
    m=str(m)
    tmp_ascii=[ord(char) for char in m]
    m_ascii=''
    for k in tmp_ascii:
        m_ascii=m_ascii+str(k)
    m_len=len(m_ascii)
    m=int(m_ascii)
    return m
    
    
    
def mod_pow(m,e, n):
    if n== 1:
        return 0
    c=1; k=0
    while k<e-1:
        c=(c * m)% n
        k=k+1
        print(k)
    return c
    
    
  
  


#function to find all the divisor of a number n
def divisori(n):
    
    print('numero di cui cerco i divisori',n)
    i=0
    support=sympy.primerange(2,round(math.sqrt(n))) #genero tutti i numeri primi tra 2 e sqrt(n)
    factors=[]
    for i in support:
        if n%i == 0:
            factors.append(i)
            print('divisore',i)
            
    if n > 1:
        factors.append(n)
        
    return factors



#function to compute the invert of a number in modular algebra (algoritmo esteso di euclide)
def mod_inv(e, ph):

    a=e; b =ph
    x1=1; y1=0
    x2=0; y2=1

    while b > 0:

      q = a // b
      a, b = b, a - q * b
      x1, x2 = x2, x1 - q * x2
      y1, y2 = y2, y1 - q * y2

    if a == 1:
        return x1 %ph
    else:
        raise ValueError("Modular inverse does not exist")





#function to generate public and private RSA key
def generate_key(len_pass):
    
  a=pow(10,len_pass)
  b=pow(10,len_pass+1)
  p=sympy.randprime(a,b); q=sympy.randprime(a,b)

  while p==q:
   p=sympy.randprime(a,b); q=sympy.randprime(a,b)
  n=p*q; phi_n=int(p-1)*(q-1); e=sympy.randprime(a,b)
  
  #div_phi=divisori(phi_n) #this operation is really, really slow and since I'm not using div_phi I just comment it :) :)
  
  while (e>phi_n): #and (e in div_phi):  #since we are choosing really big prime I bet on the fact that e will be coprime with phi, if not encryption fails :)
    e=sympy.randprime(a,b)
  
  d=mod_inv(e,phi_n)
  pub_key=[n,e]; pri_key=[n,d]
  return pub_key, pri_key



def rsa_enc(m, file_name):  #function to encrypt a message using rsa

  #m=str(m)  #my password could be alphanumeric, so I convert it in a string and then into ascii
  #tmp_ascii=[ord(char) for char in m]
  #m_ascii=''

  #for k in tmp_ascii:
    #m_ascii=m_ascii+str(k)
    
  #m_len=len(m_ascii)
  #m=int(m_ascii)
  
  m_len=len(str(m))
    
  l=generate_key(m_len)
  
  puk=l[0]; prk=l[1]
  #c=pow(m,puk[1])%puk[0]
  #c=mod_pow(m,puk[1],puk[0]) #m^e mod n
  c=pow(m,puk[1],mod=puk[0]) #built-in function of python which is incredibily fast, discovered by looking for the fastest algorithm to compute it
  
  #Here I write the key file, not used any more ( I do not actually decrypt the password )
  #file_name=re.sub( '\.txt$' , '' ,file_name)
  #key_name=file_name+'_key'
  #file_path='/Users/davidevalentini/Desktop/Algorithm_exam/keys'
  #file_writer(prk[1],key_name ,file_path ,'.txt') #I write in a file the key
  #Voglio salvare c in un database e printare la chiave per decriptare quindi solo prk[1]

  return c, puk






def enc_msg(file, file_name):#Des encryption of a file + encryption of the key  # https://gist.github.com/avishekp4/5fb646e3cc3d84c290e1   github for DES encryption


  #unicodedata.normalize('NFKD', file).encode('ascii', 'ignore')
  password=str(input('Insert a password for this file (do not use a password which is too long) : '))
  password=str_to_ascii(password)
  des_password=password.to_bytes(8, byteorder='big')  #Convert the numeric value into an 8-byte string

  key = des(des_password, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
  enc_file = key.encrypt(file)
  
  #here I save the DES encrypted file
  file_path='/Users/davidevalentini/Desktop/Algorithm_exam/enc_files'
  file_name=file_name+'_enc'
  
  file_writer(enc_file, file_name,file_path,'.txt')

  # encryption of the password
  enc_pass=rsa_enc(password,file_name)
  
  dict_name='main'
  dictionary_uploader( dict_name ,file_name, enc_pass)  #I upload/add a new element to the dictionary with file_name <-> [c,puk]

  return



def rsa_dec(d ,c ,n): #algorithm to decrypt an rsa_encrypted message
  
  m=pow(c,d,mod=n)#c^d mod n

  return m





def dec_msg(n,f_name):
    
    #I retrieve info over the key ### d ###
  #path='/Users/davidevalentini/Desktop/Algorithm_exam/keys'
  #file_name=f_name+'_key.txt'
  #d=int(file_reader(path,file_name)[0])
  
  #I decrypt the password
  #password=rsa_dec(d ,c ,puk[0])
  
  
  dir_path='/Users/davidevalentini/Desktop/Algorithm_exam/enc_files'
  sup=file_reader(dir_path,f_name)
  file=sup[0]
  
  password=str_to_ascii(password_cecker(f_name))
  
    
  #I decrypt the des message
  des_password=password.to_bytes(8, byteorder='big')  #Convert the numeric value into an 8-byte string

  key = des(des_password, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
  dec_file = key.decrypt(file)
  
  
  
  path='/Users/davidevalentini/Desktop/Algorithm_exam/clear_files'
  file_name=f_name+'_decrypted'
  file_writer(dec_file,file_name,path)
  
  return
    
    
    





########################################################################################################################
#int main(){} #or something like that

choice()














#in this section I choose a password whose lenght is 8 and extrapolate it's ascii code,
#thanks to that I will be able to encrypt the message
#password='pino ino'#str(input())

#while len(password) != 8:
  #print("Please choose a password of 8 character")
 # password=str(input())

#tmp_ascii=[ord(char) for char in password]
#password_ascii=''

#for k in tmp_ascii:
  #password_ascii=password_ascii+str(k)

#len_password=len(password_ascii)
#m=int(password_ascii)

#generate_key(len_password)

#l=generate_key(len_password)
#puk=l[0]; prk=l[1]
##crf=pow(m,puk[1])%puk[0]
#print(crf)
#clr=pow(crf,prk[1])%prk[0]











#https://gist.github.com/avishekp4/5fb646e3cc3d84c290e1
#print ("Decrypted: %r" % key.decrypt(enc_data))





#enc_file=re.sub(r'.txt','',nome_file)+'_encrypted.txt'  #do il nome al file su cui stamperò le cose criptate

#with open(enc_file, 'w') as file:  #scrivo sul file

    #file.write(enc_mess)


