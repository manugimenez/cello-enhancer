# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:22:02 2017

@author: Mentat
"""

def caculate(low_off,high_off,low_on,high_on,gate):
    low_off=0.777
    high_off=0.777
    low_on=0.01
    high_on=0.01
    IN=[low_off,high_off,low_on,high_on]
    IN=[low_off,high_on]

    K=gate['K']
    n=gate['n']
    ymax=gate['ymax']
    ymin=gate['ymin']
    increment=K*0.1
    if compare_k(ymax,ymin,K,n,IN)<compare_k(ymax,ymin,K*1.01,n,IN):
        increment=increment
    else:
        increment=-increment
    imporved_K=close(ymax,ymin,K,n,IN,increment)
    
    print(imporved_K,compare_k(ymax,ymin,imporved_K,n,IN))
    return imporved_K,compare_k(ymax,ymin,imporved_K,n,IN)
        
         
def close(ymax,ymin,K,n,IN,increment):
    if compare_k(ymax,ymin,K,n,IN)<compare_k(ymax,ymin,K+increment,n,IN):
        K=K+increment
        return close(ymax,ymin,K,n,IN,increment)
        
    else:        
        return  close_bin(ymax,ymin,K,n,IN,increment)
        
def close_bin(ymax,ymin,K,n,IN,increment):
    if abs(increment) < K*0.005:
        return K
    if compare_k(ymax,ymin,K,n,IN)>compare_k(ymax,ymin,K+increment/2,n,IN):  
        return close_bin(ymax,ymin,K,n,IN,increment/2)
    else:
        K=K+increment/2
        return close_bin(ymax,ymin,K,n,IN,increment/2)
    
def compare_k(ymax,ymin,K,n,IN):
    score=ymin+(ymax-ymin)/(1.0+(IN[1]/(K))**n)/(ymin+(ymax-ymin)/(1.0+(IN[0]/(K))**n))
    return score

gate={}
gate['K']=0.04
gate['n']=2.6
gate['ymin']=0.003
gate['ymax']=2.1

caculate(0.01,0.01,0.777,0.777,gate)

"""
inputs_d={'pBAD':['pBAD',0.0082,2.5,'ACTTTTCATACTCCCGCCATTCAGAGAAGAAACCAATTGTCCATATTGCATCAGACATTGCCGTCACTGCGTCTTTTACTGGCTCTTCTCGCTAACCAAACCGGTAACCCCGCTTATTAAAAGCATTCTGTAACAAAGCGGGACCAAAGCCATGACAAAAACGCGTAACAAAAGTGTCTATAATCACGGCAGAAAAGTCCACATTGATTATTTGCACGGCGTCACACTTTGCTATGCCATAGCATTTTTATCCATAAGATTAGCGGATCCTACCTGACGCTTTTTATCGCAACTCTCTACTGTTTCTCCATACCCGTTTTTTTGGGCTAGC'],
'pTac':['pTac',0.0034,2.8,'AACGATCGTTGGCTGTGTTGACAATTAATCATCGGCTCGTATAATGTGTGGAATTGTGAGCGCTCACAATT'],
'pTet':['pTet',0.0013,4.4,'TACTCCACCGTTGGCTTTTTTCCCTATCAGTGATAGAGATTGACATCCCTATCAGTGATAGAGATAATGAGCAC'],
'pLuxStar':['pLuxStar',0.025,0.31,'ATAGCTTCTTACCGGACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTTACTTTCGAATAAA']}
inputs=[['pBAD',0.0082,2.5,'ACTTTTCATACTCCCGCCATTCAGAGAAGAAACCAATTGTCCATATTGCATCAGACATTGCCGTCACTGCGTCTTTTACTGGCTCTTCTCGCTAACCAAACCGGTAACCCCGCTTATTAAAAGCATTCTGTAACAAAGCGGGACCAAAGCCATGACAAAAACGCGTAACAAAAGTGTCTATAATCACGGCAGAAAAGTCCACATTGATTATTTGCACGGCGTCACACTTTGCTATGCCATAGCATTTTTATCCATAAGATTAGCGGATCCTACCTGACGCTTTTTATCGCAACTCTCTACTGTTTCTCCATACCCGTTTTTTTGGGCTAGC'],
        ['pTac',0.0034,2.8,'AACGATCGTTGGCTGTGTTGACAATTAATCATCGGCTCGTATAATGTGTGGAATTGTGAGCGCTCACAATT'],
['pTet',0.0013,4.4,'TACTCCACCGTTGGCTTTTTTCCCTATCAGTGATAGAGATTGACATCCCTATCAGTGATAGAGATAATGAGCAC'],
['pLuxStar',0.025,0.31,'ATAGCTTCTTACCGGACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTTACTTTCGAATAAA']]

write_in=combinations(inputs,L)
inw=open('Input.txt','w')
strout=' '
print(write_in)
for x in inputs:
    strout=strout+str(x)+' '
    inw.write(strout)
    
"""