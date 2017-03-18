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
print(write_in)
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


















#####From here is the class for the compoent and calss for circuit
#plus the reading part


############################################################



class Node:
    def __init__(self):
        self.value = 0
        self.num_input=0
        
        self.low_off=0
        self.high_off=0
        self.low_on=0
        self.high_on=0
        
        self.K=0
        self.n=0
        self.ymax=0
        self.ymin=0

        self.score=0
        self.name=''
    
    def update(self,l_off,h_off,l_on,h_on):
        self.low_off=l_off
        self.high_off=h_off
        self.low_on=l_on
        self.high_on=h_on         

    def __str__(self):
        return 'Node ['+str(self.name)+str(self.score)+str(self.num_input)+']'+str(self.low_on)+'to'+str(self.high_on)

class Circuit:
    def __init__(self):

        
        self.compoent_list=[]
        self.connection=[]
        self.come=[]
        for emp in range(200):
            self.connection.append(-1)
            self.come.append([])
        self.inputs=[]
        self.outputs=[]
        self.notg=[]
        self.norg=[]
        self.dict_comp={}
        
    def new_compoent(self,num_in,score,IN,index,name):  
        current=Node()
        current.num_input=num_in
        

        current.score=score
        current.name=name
        
        self.dict_comp[name]=current
        self.compoent_list.append(current)     
        for input_g in IN:
            self.connection[input_g]=index
            
            
        if num_in == 0:
            self.inputs.append(index)
        elif num_in == 1:
            self.notg.append(index)
        elif num_in == 2:
            self.norg.append(index)
        else:
            self.outputs.append(index)

    def __str__(self):
        if self.compoent_list != None:
            
            out='lai'
            count=0
            for current in self.compoent_list:
                if current==0:
                    break
                out +=  str(current) +'-'+str(count)+' '
                count+=1
            out+=']/n inputs_index'
            for in1 in self.inputs:
                out+=str(in1)+' '
            out+='connection'
            print(self.connection[4])
            for in1 in range(1,len(self.connection)):
                
                if self.connection[in1]==-1:
                    break
                elif self.connection[in1]== None:
                    break
                out+=str(in1)+'-'+str(self.connection[in1]) +'||'      
            return out + ']'
        return 'LinkedList []'








######################################################




print('----------start')

circuit=Circuit()
Gates={}
temp_change=0

for over_cir in range(2,200):
    if len(Files[over_cir])==0:

        temp_change=over_cir
        break
        
    index=Files[over_cir][part-10:part].strip() #index of the gate or something
    index=eval(index)
    num_in=0
    part=Files[over_cir].find('(')         #find the input of the gate, deal with nor 
    part1=Files[over_cir].find(',')
    part2=Files[over_cir].find(')')

    if part==-1:
        input1_1=-1
        input1_2=-1
        num_in=0
        index=Files[over_cir][40:55].strip()        
    elif part1==-1:
        input1_1=eval(Files[over_cir][part+1:part2])
        input1_2=-1
        index=Files[over_cir][part-10:part].strip()
        num_in=1
    else:
        input1_1=eval(Files[over_cir][part+1:part1])
        input1_2=eval(Files[over_cir][part1+1:part2])   
        num_in=2       
        index=Files[over_cir][part-10:part].strip()      


    if Files[over_cir][0]=='O':
        num_in=-1        
    
    name=Files[over_cir][30:40].strip()    # name

    score=eval(Files[over_cir][60:70])    # score   
    circuit.new_compoent(num_in,score,[input1_1,input1_2],index,name)
    print(name)
print('-------')
for wiwi in circuit.dict_comp:
    print(wiwi)
print('this is the end')
counttoend=0
for seven in range(0,len(circuit.compoent_list)): 


    
    circuit.come[int(circuit.connection[int(seven)])].append(int(seven))
while counttoend<len(circuit.compoent_list):

    temp_start=0     
    temp_name=''
    for over_i in range(temp_change,len(Files)):
        if Files[over_i].find('Gate')==-1:
            continue
        temp_start=over_i
        temp_name=Files[over_i][0:Files[over_i].find('G')].strip()
        print('888',Files[over_i])
        break
    print('tell me why the fuck is YFP',temp_name)
    

    list_off=[]
    list_on=[]
    for over_para in range(temp_start+1,len(Files)):
        if len(Files[over_para])==0:
            temp_change=over_para

            break    
        depart=Files[over_para].find(':')+1
        test_str=Files[over_para][depart:len(Files[over_para])]
        print(test_str)
        print('-'+test_str[test_str.find(':')+1:test_str.find(':')+7]+'-')
        number=eval(test_str[test_str.find(':')+1:test_str.find(':')+10])
        if eval(test_str[0:5])==1:
            list_on.append(number)
        else:
            list_off.append(number)
        temp_change=over_para
    for wiwi in circuit.dict_comp:
        print(wiwi)
    print(temp_name,len(list_off),len(list_on),min(list_off),max(list_off),min(list_on),max(list_on))
    circuit.dict_comp[temp_name].update(min(list_off),max(list_off),min(list_on),max(list_on))
    counttoend+=1
    



print(Files)
for a in circuit.compoent_list:
    print(a)

print(len(circuit.compoent_list))
for ele in circuit.inputs:

    print(circuit.compoent_list[eval(ele)],'yourenma')
    print('preshant')
print('outnode')
for ele in circuit.outputs:
    print(str(ele))
    print(circuit.compoent_list[eval(ele)])


"""    
Gates[temp_name]=[min(list_off),max(list_off),min(list_on),max(list_on)]
print(Gates)



print(Files[temp_start])
print (Files[temp_start+1].find(':'))        

"""




