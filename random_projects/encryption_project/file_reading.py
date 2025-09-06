import pickle
import re
import os



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




#cartella algorithm_exam path   Users/davidevalentini/Desktop/Algorithm_exam
  
   #function to ceck that passwords coincide
def password_cecker(file_name):
    
   #To check that this is the right password I don't need the prk, I just check that the trasformation of p_word and c encrypted password coincide
   key=str(input('Insert password to decrypt: '))
   key = key.ljust(32,'0')[:32]
   key= key.encode()

   ascii_pass=str_to_ascii(key)
   
   # I retrieve info over the ecrypted password ### [c, puk] ###
   path='/Users/davidevalentini/Desktop/Algorithm/dictionary'
   sup=dictionary_reader('main')[file_name]
   c=sup[0]; puk=sup[1]
   
   i=0; cp=pow(ascii_pass, puk[1], mod=puk[0])  #p_word^e mod n
   
   
   while cp != c and i<3:
    
    j=3-i

    print('\nLook out, you only have another '+str(j)+' trials, then you will be expelled (and maybe in future the file destroyed)\n')
    key=str(input('Insert password to decrypt: '))
    key = key.ljust(32,'0')[:32]
    key= key.encode()
    ascii_pass=str_to_ascii(key)
    
    cp=pow(ascii_pass, puk[1], mod=puk[0])
    i+=1
    
    if i>=3:
        
        print('\n You failed to remember the right password, adios')
        exit(1)
  
   return key
    
    
    


#function used to read from files
def file_reader(dir_path, file_name, is_byte):
    c = os.getcwd()
    os.chdir(dir_path)
    
    try:
        with open(os.path.join(dir_path, file_name), "rb" if is_byte else "r") as file_tmp:
            text = file_tmp.read()
    except Exception as e:
        print(f"An error occurred: {e}")
        text = None
    
    os.chdir(c)
    
    return text

  
  
  
  
#function to write a new file
def file_writer(m, file_name, dir_path, format):
    c = os.getcwd()
    os.chdir(dir_path)

    m = str(m)
    enc_file = re.sub(r'.txt', '', file_name) + format

    with open(enc_file, 'wb' if isinstance(m, bytes) else 'w') as file:
        file.write(m)

    os.chdir(c)
    
    return
    
    
def dictionary_uploader(dict_name,pos,n):  #function to save file <-> key c (encrypted)

    c=os.getcwd()
    #os.chdir(dir_path)
    os.chdir('/Users/davidevalentini/Desktop/Algorithm/dictionary')
    
    dict_name=re.sub(r'.pkl','',dict_name)
    dict_file_up=dict_name+'.pkl'
    
    if not os.path.isfile(dict_file_up):
        
        a={pos:n}
        with open(dict_file_up, 'wb') as handle:
            pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        
        dict=dictionary_reader(dict_file_up)
        dict[pos]=n
    
        with open(dict_file_up, 'wb') as fp:
            pickle.dump(dict, fp)
        
        os.chdir(c)
    
        return
    


def dictionary_reader(dict_name): #function to read a dictionary enc_file <-> c
    
    
    c=os.getcwd()
    #os.chdir(dir_path)
    os.chdir('/Users/davidevalentini/Desktop/Algorithm/dictionary')
    dict_name=re.sub(r'.pkl','',dict_name)
    dict_file_r=dict_name+'.pkl'
    
    with open(dict_file_r, 'rb') as fp:
        dict = pickle.load(fp)
    
    os.chdir(c)
    
    return dict
