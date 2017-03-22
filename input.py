# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 00:37:00 2017

@author: Mentat
"""

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
from itertools import permutations




class Node:
    def __init__(self):
        self.value = 0
        self.num_input=0
        
        self.low_off=0
        self.high_off=0
        self.low_on=0
        self.high_on=0
        
        #self.K=0
        #self.n=0
        #self.ymax=0
        #elf.ymin=0

        self.score=0
        self.name=''
    
    def update(self,l_off,h_off,l_on,h_on):     #write seprately since this part is updated in a different place
        self.low_off=l_off
        self.high_off=h_off
        self.low_on=l_on
        self.high_on=h_on         

    def __str__(self):
        return 'Node ['+str(self.name)+str(self.score)+str(self.num_input)+']'+str(self.low_on)+'to'+str(self.high_on)

"""
    this part is basically record the way the connection is presented in the result
    compoentlis
"""

class Circuit:
    def __init__(self):

        
        self.compoent_list=[]   
        self.connection=[]
        self.come=[]
        for emp in range(100):
            self.connection.append(None)
            self.compoent_list.append(None)
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
        index=eval(index)
        self.dict_comp[name]=current
        self.compoent_list[index]=current    

            
        print(index,name)    
        for yy in IN:
            print(yy)
        if num_in == 0:
            self.inputs.append(index)
        elif num_in == 1:
            self.notg.append(index)
            for input_g in IN:
                if input_g==-1:
                    continue
                self.connection[input_g]=index
        elif num_in == 2:
            self.norg.append(index)
            for input_g in IN:
                if input_g==-1:
                    continue
                self.connection[input_g]=index
        else:
            self.outputs.append(index)
            for input_g in IN:
                if input_g==-1:
                    continue
                self.connection[input_g]=index
                
        
        for a in IN:
            if a!=None:
                self.come[index].append(a)
        

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






def run_retreieve(de_id,verilog):

    # change the corresponding instance, generate command line 
    
    design_id=de_id
    design_input='Inputs.txt'
    design_output='Outputs.txt'
    design_verilog=verilog
    
    lalala='curl -u "username:password" -X POST http://cellocad.org:8080/submit \ --data-urlencode "id='+design_id+'" \ --data-urlencode "verilog_text@'+design_verilog+'" \ --data-urlencode "input_promoter_data@'+design_input+'" \ --data-urlencode "output_gene_data@'+design_output+'"'
    zzz='curl -u "username:password" -X GET http://cellocad.org:8080/results/'+design_id+'/'+design_id+'_A000_logic_circuit.txt'
    
    T = subprocess.run(lalala,stdout=subprocess.PIPE) # POST DESIGN
    Files = T.stdout.decode().splitlines()
    print(Files)    
    T = subprocess.run(zzz,stdout=subprocess.PIPE)  #GET THE RESULT
    Files = T.stdout.decode().splitlines()
    print(Files)
    return Files


def interprate(Files):
    #c
    Gates={}
    temp_change=0
    
    for over_cir in range(2,200):
        print(len(Files),over_cir)
        if len(Files[over_cir])==0:
    
            temp_change=over_cir
            break
            
    
        num_in=0
        part=Files[over_cir].find('(')         #find the input of the gate, deal with nor 
        part1=Files[over_cir].find(',')         
        part2=Files[over_cir].find(')')
    
        if part==-1:        #no '(' means this line is input
            input1_1=-1
            input1_2=-1
            num_in=0
            index=Files[over_cir][40:55].strip()        
        elif part1==-1:     #no ',' means this line is not gate or output, output is being handled later
            input1_1=eval(Files[over_cir][part+1:part2])
            input1_2=-1
            index=Files[over_cir][part-10:part].strip()
            num_in=1
        else:   #this is nor gate
            input1_1=eval(Files[over_cir][part+1:part1])
            input1_2=eval(Files[over_cir][part1+1:part2])   
            num_in=2       
            index=Files[over_cir][part-10:part].strip()      
    
    
        if Files[over_cir][0]=='O':    #here is to check if it was output
            num_in=-1        
        
        name=Files[over_cir][30:40].strip()    # name relative fixed position
    
        score=eval(Files[over_cir][60:70])    # score   
        circuit.new_compoent(num_in,score,[input1_1,input1_2],index,name)
    
    counttoend=0
        
     #get rid of redundancy 
    for b in range(len(circuit.compoent_list)-1,-1,-1):
        if circuit.compoent_list[b] == None:
            del circuit.compoent_list[b]
    for b in range(len(circuit.connection)-1,len(circuit.compoent_list)-1,-1):
        
        if circuit.connection[b] == None:
            del circuit.connection[b] 
    for b in range(len(circuit.come)-1,len(circuit.compoent_list)-1,-1):

        if circuit.come[b] == []:
            del circuit.come[b]   
    for b in range(len(circuit.come)):
        for k in [1,0]:
            if circuit.come[b][k]==-1:
                del circuit.come[b][k]        

    for b in range(len(circuit.connection)):
        if circuit.connection[b]==None:
            circuit.connection[b]=-1

        

    while counttoend<len(circuit.compoent_list):
    
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
        for over_para in range(temp_start+1,len(Files)):
            if len(Files[over_para])==0:
                temp_change=over_para
    
                break    
            depart=Files[over_para].find(':')+1
            test_str=Files[over_para][depart:len(Files[over_para])]
    
            number=eval(test_str[test_str.find(':')+1:test_str.find(':')+10])
            if eval(test_str[0:5])==1:
                list_on.append(number)
            else:
                list_off.append(number)
            temp_change=over_para
    
        circuit.dict_comp[temp_name].update(min(list_off),max(list_off),min(list_on),max(list_on))
        counttoend+=1
        
    print(len(circuit.compoent_list))
    for ele in circuit.inputs:
    
        print(circuit.compoent_list[ele],'yourenma')
    print('outnode')
    for a in Files:
        print(a)
    for cao in circuit.connection:
        
        print(cao)
    for b in circuit.compoent_list:
        print(b)
    
    for ele in circuit.outputs:
    
        print(circuit.compoent_list[ele])
        return circuit.compoent_list[ele].score
#from cello_client import CtxObject
a=0
L=3
result={}   
scores={}
Filetowrite={}
verilog='0xFE.v'  
#try every input combinations
def try_inputs(L):          
    inputs_d={'pBAD':['pBAD',0.0082,2.5,'ACTTTTCATACTCCCGCCATTCAGAGAAGAAACCAATTGTCCATATTGCATCAGACATTGCCGTCACTGCGTCTTTTACTGGCTCTTCTCGCTAACCAAACCGGTAACCCCGCTTATTAAAAGCATTCTGTAACAAAGCGGGACCAAAGCCATGACAAAAACGCGTAACAAAAGTGTCTATAATCACGGCAGAAAAGTCCACATTGATTATTTGCACGGCGTCACACTTTGCTATGCCATAGCATTTTTATCCATAAGATTAGCGGATCCTACCTGACGCTTTTTATCGCAACTCTCTACTGTTTCTCCATACCCGTTTTTTTGGGCTAGC'],
    'pTac':['pTac',0.0034,2.8,'AACGATCGTTGGCTGTGTTGACAATTAATCATCGGCTCGTATAATGTGTGGAATTGTGAGCGCTCACAATT'],
    'pTet':['pTet',0.0013,4.4,'TACTCCACCGTTGGCTTTTTTCCCTATCAGTGATAGAGATTGACATCCCTATCAGTGATAGAGATAATGAGCAC'],
    'pLuxStar':['pLuxStar',0.025,0.31,'ATAGCTTCTTACCGGACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTTACTTTCGAATAAA']}
    inputs=[['pBAD',0.0082,2.5,'ACTTTTCATACTCCCGCCATTCAGAGAAGAAACCAATTGTCCATATTGCATCAGACATTGCCGTCACTGCGTCTTTTACTGGCTCTTCTCGCTAACCAAACCGGTAACCCCGCTTATTAAAAGCATTCTGTAACAAAGCGGGACCAAAGCCATGACAAAAACGCGTAACAAAAGTGTCTATAATCACGGCAGAAAAGTCCACATTGATTATTTGCACGGCGTCACACTTTGCTATGCCATAGCATTTTTATCCATAAGATTAGCGGATCCTACCTGACGCTTTTTATCGCAACTCTCTACTGTTTCTCCATACCCGTTTTTTTGGGCTAGC'],
            ['pTac',0.0034,2.8,'AACGATCGTTGGCTGTGTTGACAATTAATCATCGGCTCGTATAATGTGTGGAATTGTGAGCGCTCACAATT'],
    ['pTet',0.0013,4.4,'TACTCCACCGTTGGCTTTTTTCCCTATCAGTGATAGAGATTGACATCCCTATCAGTGATAGAGATAATGAGCAC'],
    ['pLuxStar',0.025,0.31,'ATAGCTTCTTACCGGACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTTACTTTCGAATAAA']]
    #this is for list of input,     
    
    input_index=[0,1,2,3]
    write_in=combinations(input_index,L)

    
 
    for x in write_in:  #list of combinations with order
        inw=open('Inputs.txt','w')
        strout=' '
        design_id='aige'
        for y in x:     #x is (index1,index2), use index to access the inputs and generate string to write
            design_id+=str(y)
            for s in inputs[y]:
                strout=strout+str(s)+' '
        inw.write(strout)
        inw.close()
        print('-------------------------',str(x),'--------------------------')  
        print(design_id)
        print(strout)
        result[design_id]=run_retreieve(design_id,verilog)
        scores[design_id]=interprate(result[design_id])
        Filetowrite[design_id]=strout
        print('-------------------------ending-------------------------------')
    key=max(scores, key=scores.get)
    return key
    

#above  can can can  can   only can be write as generator of inputs, different combination of 4 inputs, L=1 4 situation,L=2  4*3/2 situations    
circuit=Circuit()
de_id=try_inputs(L)
print(de_id,scores[de_id])

with open('Inputs.txt','w') as kk:
    kk.write(Filetowrite[design_id])

for a in scores:
    print(a,scores[a])

'''
with open('lalala.txt','w') as adc:
    adc.write('\n'.join(Files))
''' 
 
#write the result balala_logic_circuit.txt into    







#####From here is the class for the compoent and calss for circuit
#plus the reading part


############################################################








######################################################




print('----------start')

for a in circuit.come:
    print('_'.join(str(a)))

"""    
Gates[temp_name]=[min(list_off),max(list_off),min(list_on),max(list_on)]
print(Gates)



print(Files[temp_start])
print (Files[temp_start+1].find(':'))        

"""

