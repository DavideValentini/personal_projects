
from aes_enc import *




#cartella algorithm_exam path   Users/davidevalentini/Desktop/Algorithm_exam



def choice():

    s=str(input('\n Would you like to encrypt (0) or decrypt (else) a file.txt?\t'))

    if s=='0':
    
        print('\n Be carefull, after this process the original file will be deleted, the only way to retrieve it will be through the key that will be generated, keep it! \n')
        
        file_name='prova.txt'#str(input('Insert the name of the clear file you want to encrypt: '))
        file_path='/Users/davidevalentini/Desktop/Algorithm/clear_files'
        #print('sei sicuro del nome? y or n')
        #q=input()
        #while q=='n':
            #print('inserisci nome file che vuoi criptare:')
            #file_name=str(input())
            #print('sei sicuro del nome? y or n')
            #q=input()
        file=file_reader(file_path, file_name, 0) 
        enc_msg(file,file_name)
        print('\n The file has been encrypted, you will find it on your pc (should be in the same directory of this script)\n')
        return
    else:
    
        print('\nyou want to decrypt something that is encrypted, hope for you everything goes well...   \n')
        
        dict_name='main'#str(input('insert name of the file you want to decrypt: '))+'.pkl'
        dict=dictionary_reader(dict_name)
        
        file_name='prova_enc.txt'#str(input('file name:'))
        #I check that there exists a file whith this name, if yes I retrieve n and the encrypted file
        while file_name not in dict:
           q=str(input('\nfile not found, do you want to search for another file? yes(0), no(else)\n'))
           if q != '0':
              exit()
           else:
              file_name=str(input('file name:'))
              
       # n=dict[file_name]
        
        dec_msg(file_name)
    
    return
    
choice()

