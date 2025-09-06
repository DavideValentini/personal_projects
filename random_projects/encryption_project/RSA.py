import random
import sympy
import math


    #faster modular power than classic % but slower than pow(, mod=...)
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
    
    i=0
    support=sympy.primerange(2,round(math.sqrt(n))) #genero tutti i numeri primi tra 2 e sqrt(n)
    factors=[]
    for i in support:
        if n%i == 0:
            factors.append(i)
            
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


def rsa_dec(d ,c ,n): #algorithm to decrypt an rsa_encrypted message
  
  m=pow(c,d,mod=n)#c^d mod n

  return m

