# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 11:27:05 2017

@author: Mentat
"""
from collections import OrderedDict 
import subprocess
import json
import csv
from itertools import combinations
#from cello_client import CtxObject
a=0
L=2



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
for x in inputs:
    strout=strout+str(x)+' '
    inw.write(strout)
    
#above  can can can  can   only can be write as generator of inputs, different combination of 4 inputs, L=1 4 situation,L=2  4*3/2 situations    
    
    
    
aa=open('takashi003_A000_logic_circuit.txt','r')
saa=aa.read()
print(saa)


fin=open('gates_Eco1C1G1T1.csv','r')
drt = csv.DictReader(fin)
print(type(drt))

dr=sorted(drt,key=lambda x:float(x['n']))

# dr.fieldnames contains values from first row of `f`.
with open('copy.csv','w',newline='') as fou:
    dw = csv.DictWriter(fou, fieldnames=drt.fieldnames)
    headers = {} 
    for n in dw.fieldnames:
        headers[n] = n
    dw.writerow(headers)
    for row in dr:
        row['ymax']=99   # can be changed
        
        dw.writerow(row)
        
# can be write as generator of the ucf file, it reads the original csv file line by line
# modify the row then write in a new csv file
# we should generate a dictionary for the gate
# the following call the ucf_writer turn the new csv file to json

T = subprocess.run(['python','ucf_writer.py','copy.csv'],stdout=subprocess.PIPE)
Files = T.stdout.decode().splitlines()




# change the corresponding instance, generate command line 
de_id='demo998'
design_id='demo997'
design_input='Inputs.txt'
design_output='Outputs.txt'
design_verilog='0xFE.v'


#design_id='"id="'+design_id+'"'
#design_inputs='"input_promoter_data@'+design_inputs+'"'
#design_outputs='"output_gene_data@'+design_outputs+'"'
#design_verilog='"verilog_text'+design_verilog+'"'
lalala='curl -u "username:password" -X POST http://cellocad.org:8080/submit \ --data-urlencode "id='+design_id+'" \ --data-urlencode "verilog_text@'+design_verilog+'" \ --data-urlencode "input_promoter_data@'+design_input+'" \ --data-urlencode "output_gene_data@'+design_output+'"'
#post_design=['curl','-u','"username:password"','-X','POST','http://cellocad.org:8080/submit','\ --data-urlencode',design_id,'\ --data-urlencode',design_verilog,'\ --data-urlencode',design_inputs,'\ --data-urlencode',design_outputs]

#T = subprocess.run(lalala,stdout=subprocess.PIPE)
#Files = T.stdout.decode().splitlines()
#print(Files)
zzz='curl -u "username:password" -X GET http://cellocad.org:8080/results/'+design_id+'/'+design_id+'_A000_logic_circuit.txt'
#get_file=['curl','-u','"username:password"','-X','POST','http://cellocad.org:8080/results/'+de_id+'/'+de_id+'_A000_logic_circuit.txt']


T = subprocess.run(zzz,stdout=subprocess.PIPE)
Files = T.stdout.decode().splitlines()

with open('lalala.txt','w') as adc:
    adc.write('\n'.join(Files))
    
 
#write the result balala_logic_circuit.txt into    




Files[3]
for i in range(len(Files[3])):
    print(i,Files[3][i])
    
#for i in range(2,1000):
#    if Files[i][0]

print('_____---------______')
print(Files[3])
print(Files[3].find(':'))
part=Files[3].find('(')
part1=Files[3].find(',')
part2=Files[3].find(')')
print(part1)

index=Files[3][part-10:part].strip() #index of the gate or something
index=eval(index)

part=Files[3].find('(')         #find the input of the gate, deal with nor 
part1=Files[3].find(',')
part2=Files[3].find(')')
if part==-1:
    input1_1=-1
    input1_2=-1
elif part1==-1:
    input1_1=Files[3][part+1:part2]
    input1_2=-1
else:
    input1_1=Files[3][part+1:part1]
    input1_2=Files[3][part2+1:part2]   


name=Files[3][30:40].strip()    # name

score=eval(Files[3][60:70])    # score

print(name)

Gates={}



temp_change=0

for over_cir in range(3,200):
    if len(Files[over_cir])==0:

        temp_change=over_cir
        break
        
    index=Files[over_cir][part-10:part].strip() #index of the gate or something
    index=eval(index)
        
    part=Files[over_cir].find('(')         #find the input of the gate, deal with nor 
    part1=Files[over_cir].find(',')
    part2=Files[over_cir].find(')')
    if part==-1:
        input1_1=-1
        input1_2=-1
    elif part1==-1:
        input1_1=Files[over_cir][part+1:part2]
        input1_2=-1
    else:
        input1_1=Files[over_cir][part+1:part1]
        input1_2=Files[over_cir][part2+1:part2]   
        
        
    name=Files[over_cir][30:40].strip()    # name
        
    score=eval(Files[over_cir][60:70])    # score   

temp_start=0     
temp_name=''
for over_i in range(temp_change,len(Files)):
    if Files[over_i].find('Gate')==-1:
        continue
    temp_start=over_i
    temp_name=Files[over_i][0:Files[over_i].find('G')].strip()
    break



list_off=[]
list_on=[]
for over_para in range(temp_start,len(Files)):
    if len(Files[over_para])==0:
        temp_change=over_cir
        break    
    depart=Files[over_para].find(':')+1
    test_str=Files[over_para][depart:len(Files[over_para])]
    number=eval(test_str[Files[over_para].find(':')+1:Files[over_para].find(':')+10])
    if eval(test_str[depart:5])==1:
        list_on.append(number)
    else:
        list_off.append(number)
        
min(list_off)
max(list_off)
min(list_on)
max(list_on)

Gates[temp_name]=[min(list_off),max(list_off),min(list_on),max(list_on)]




print(Files[temp_start])
print (Files[temp_start+1].find(':'))        
