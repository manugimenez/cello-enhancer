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

import argparse

def main():
    parser = argparse.ArgumentParser(description="Cello Design Optimizer")
    # parser.add_argument('-x', '--x-center', type=float, required=True)
    # parser.add_argument('-y', '--y-center', type=float, required=True)
    # parser.add_argument('values', type=float, nargs='*')
    parser.add_argument("verilog", help="path to the verilog file describing the circuit")
    parser.add_argument("ucf", help="path to the UCF file listing parts available")
    parser.add_argument("n", help="max number of components that can be modified during optimization",type=int)
    args = parser.parse_args()
    return args




# FOR Storing the compoent in the circuit, have parameter like below, K,n, ymax,
# and also the input information (only the max,min of the ON and OFF)
#

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

    def translate_1(self):
        return [self.high_on,self.low_on,self.high_off,self.low_off]

    def __str__(self):
        return 'Node ['+str(self.name)+str(self.score)+str(self.num_input)+'] '+str(self.low_on)+'to'+str(self.high_on)+'-'+str(self.low_off)+'to'+str(self.high_off)

"""
    this part is basically record the way the connection is presented in the result
    compoentlis
"""
# compoent_list stores the gates inputs, outputs, 1 input seen as a component. index of a compoent is seen as a id that can be used in connection_list
# connection_list store the connection information,  for gate number 3, connetion[3], the value is the gate it output to
#inputs outputs,notg, norg,are the list contains the indexes of the gates, for categrize compoent
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

            
        #interprate the parameters passed in, decide the type(inputs,not gate, and so on)
        for yy in IN:
            print(yy)
        if num_in == 0:         #inputs
            self.inputs.append(index)
        elif num_in == 1:       #
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
            for in1 in range(1,len(self.connection)):
                
                if self.connection[in1]==-1:
                    break
                elif self.connection[in1]== None:
                    break
                out+=str(in1)+'-'+str(self.connection[in1]) +'||'      
            return out + ']'
        return 'LinkedList []'




#send design and retreieve the design_id_A000_logic_circuit.txt

def run_retreieve(de_id,verilog):

    # change the corresponding instance, generate command line 
    
    design_id=de_id
    design_input='Input.txt'
    design_output='Outputs.txt'
    design_verilog=verilog
    
    lalala='curl -u "Mentats:cf10293" -X POST http://cellocad.org:8080/submit \ --data-urlencode "id='+design_id+'" \ --data-urlencode "verilog_text@'+design_verilog+'" \ --data-urlencode "input_promoter_data@'+design_input+'" \ --data-urlencode "output_gene_data@'+design_output+'"'
    zzz='curl -u "Mentats:cf10293" -X GET http://cellocad.org:8080/results/'+design_id+'/'+design_id+'_A000_logic_circuit.txt'
    
    T = subprocess.run(lalala,stdout=subprocess.PIPE) # POST DESIGN
    Files = T.stdout.decode().splitlines()

    T = subprocess.run(zzz,stdout=subprocess.PIPE)  #GET THE RESULT
    Files = T.stdout.decode().splitlines()
    return Files

#the function that reads the result from run_retreieve 
def interprate(Files):
    #c
    Gates={}
    temp_change=0
    
    for over_cir in range(2,200):
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
    return circuit.compoent_list[0].score
        
def get(design_id):
    zzz='curl -u "Mentats:cf10293" -X GET http://cellocad.org:8080/results/'+design_id+'/'+design_id+'_A000_logic_circuit.txt'
    T = subprocess.run(zzz,stdout=subprocess.PIPE)  #GET THE RESULT
    Files = T.stdout.decode().splitlines()
    return Files
#from cello_client import CtxObject

#try every input combinations

#--------------------------------------------------------------------
def caculate(low_off,high_off,low_on,high_on,gate):
    #low_off=0.777
    #high_off=0.777
    #low_on=0.01
    #high_on=0.01
    IN=[low_off,high_off,low_on,high_on]
    IN=[high_off,low_on]

    K=gate['K']
    n=gate['n']
    ymax=gate['ymax']
    ymin=gate['ymin']
    print(ymax,ymin,K,n,compare_k(ymax,ymin,K,n,IN),circuit.compoent_list[nor].score,circuit.compoent_list[circuit.come[nor][0]].score)
    print(' ')
    print('you want original or crispy?')
    increment=K*0.1
    print('npoooooooooooooo',compare_k(ymax,ymin,K,n,IN),ymax/ymin)
    if compare_k(ymax,ymin,K,n,IN)<compare_k(ymax,ymin,K*1.01,n,IN):
        increment=increment
    else:
        increment=-increment

    imporved_K=close(ymax,ymin,K,n,IN,increment)

    return imporved_K,compare_k(ymax,ymin,imporved_K,n,IN)
        
# first try out         
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

#caculate the score    
def compare_k(ymax,ymin,K,n,IN):
    #print('-------------')
    #print(ymax,ymin,K,n)
    #print(IN[0],IN[1])

    #print(ymax,ymin,K,n)
    #print(IN[0],IN[1])

    #print((ymin+(ymax-ymin)/(1.0+(IN[1]/(K))**n))/(ymin+(ymax-ymin)/(1.0+(IN[0]/(K))**n)))
    
    score=(ymin+(ymax-ymin)/(1.0+(IN[1]/(K))**n))/(ymin+(ymax-ymin)/(1.0+(IN[0]/(K))**n))
    return score






# extracted the information about gates
def read_store_UCF(filepath,gates):
    #filepath = 'Eco1C1G1T1.UCF.json'
    filetext = open(filepath, 'r').read()
    filejson = json.loads(filetext)
    
    for obj in filejson:
        if obj['collection'] == 'response_functions':
            name=obj['gate_name']
            gates[obj['gate_name']]={'parameters':{'ymax':0,'ymin':0,'K':0,'n':0,},'variables':{'off_threshold':0,'on_threshold':0}}
            for k in obj['parameters']: #save in 
                if k['name']=='ymax':
                    gates[name]['parameters']['ymax']=k['value']
                if k['name']=='ymin':
                    gates[name]['parameters']['ymin']=k['value']
                if k['name']=='K':
                    gates[name]['parameters']['K']=k['value']
                if k['name']=='n':
                    gates[name]['parameters']['n']=k['value'] 
            for k in obj['variables']:
                if k['name']=='off_threshold':
                    gates[name]['variables']['off_threshold']=k['value']
                if k['name']=='on_threshold':
                    gates[name]['variables']['on_threshold']=k['value'] 
           
           


def try_inputs(L,verilog):          
    inputs=[['pBAD',0.0082,2.5,'ACTTTTCATACTCCCGCCATTCAGAGAAGAAACCAATTGTCCATATTGCATCAGACATTGCCGTCACTGCGTCTTTTACTGGCTCTTCTCGCTAACCAAACCGGTAACCCCGCTTATTAAAAGCATTCTGTAACAAAGCGGGACCAAAGCCATGACAAAAACGCGTAACAAAAGTGTCTATAATCACGGCAGAAAAGTCCACATTGATTATTTGCACGGCGTCACACTTTGCTATGCCATAGCATTTTTATCCATAAGATTAGCGGATCCTACCTGACGCTTTTTATCGCAACTCTCTACTGTTTCTCCATACCCGTTTTTTTGGGCTAGC'],
            ['pTac',0.0034,2.8,'AACGATCGTTGGCTGTGTTGACAATTAATCATCGGCTCGTATAATGTGTGGAATTGTGAGCGCTCACAATT'],
    ['pTet',0.0013,4.4,'TACTCCACCGTTGGCTTTTTTCCCTATCAGTGATAGAGATTGACATCCCTATCAGTGATAGAGATAATGAGCAC'],
    ['pLuxStar',0.025,0.31,'ATAGCTTCTTACCGGACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTTACTTTCGAATAAA']]
    #this is for list of input,     
    
    input_index=[0,1,2]
    write_in=combinations(input_index,L)

    
    times=3
    for x in write_in:  #list of combinations with order
        if times !=0:
            times=times-1
        else:
            break
        inw=open('Input.txt','w')
        strout=' '
        design_id='aigelT'
        for y in x:     #x is (index1,index2), use index to access the inputs and generate string to write
            design_id+=str(y)
            for s in inputs[y]:
                strout=strout+str(s)+' '
            strout=strout+'\n'
                
        inw.write(strout)
        inw.close()
        print('-------------------------',str(x),'--------------------------')  
        print(design_id)

        result[design_id]=run_retreieve(design_id,verilog)
        scores[design_id]=interprate(result[design_id])
        FILETO[design_id]=strout
        print('-------------------------ending-------------------------------')
    key=max(scores, key=scores.get)
    return key
    

#above  can can can  can   only can be write as generator of inputs, different combination of 4 inputs, L=1 4 situation,L=2  4*3/2 situations    
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
if __name__ == '__main__':
    args = main()
    # n=3
    # file_ucf='Eco1C1G1T1.UCF.json'
    # verilog='0xFE.v'  
    # n=parser.parse_args(['n'])
    # file_ucf=parser.parse_args(['ucf'])
    # verilog=parser.parse_args(['verilog'])
    n = args.n
    verilog = args.verilog
    file_ucf = args.ucf

    a=0
    L=3
    result={}   
    scores={}
    FILETO={}
    

    
    gates={}
    circuit=Circuit()
    de_id=try_inputs(L,verilog)
    print('best score of the swap inputs',de_id,scores[de_id])
    fil=get(de_id)
    interprate(fil)
    
    gates_origin={}
    read_store_UCF(file_ucf,gates_origin)
    
    current_s=0
    start_para=[]
    for a in circuit.outputs:
        current_s=circuit.compoent_list[a].score
        l=1
        chain=[]
        nor=None
        while l!=2:
            l=len(circuit.come[a])
    
            a=circuit.come[a][0]
            for k in circuit.norg:
                if a==k:
                    nor=k
                    l=2
    
                    start_para.append(circuit.compoent_list[a].high_on)
                    start_para.append(circuit.compoent_list[a].low_on)
                    start_para.append(circuit.compoent_list[a].high_off)
                    start_para.append(circuit.compoent_list[a].low_off)
                                    
            for k in circuit.inputs:
                if a== k:
                    l=2
    
                    start_para.append(circuit.compoent_list[a].high_on)
                    start_para.append(circuit.compoent_list[a].low_on)  
                    start_para.append(circuit.compoent_list[a].high_off)
                    start_para.append(circuit.compoent_list[a].low_off)                
            if l!=2:
                chain.append(a)
            else:
                break
    def x_to_y(ymax,ymin,K,n,x):
        return ymin+(ymax-ymin)/(1.0+(x/(K))**n)
    def combine(left,right):
        return [max([left[0]+right[2],left[2]+right[0]]),min([left[1]+right[3],left[3]+right[1]]),left[2]+right[2],left[3]+right[3]]
        
                
            
    print('----------------------------------------')
    
    
    
    chain_c=[]
    for a in chain:
        chain_c.append(circuit.compoent_list[a])
      #  gates_origin[chain_c[k].name]
    
    # get a copy of gates that havn't been used
    gate_poten={}
    gate_left={}
    used=[]
    judge_2=True
    for n in circuit.compoent_list:
        judge_2=True
        for k in chain_c:
            
            if n.name==k.name:
                judge_2=False
                
        if judge_2:
            used.append(n)
    
                
    for nmae in gates_origin:
        judge=True            
    
        for n in used:
    
            if nmae==n.name:
                judge=False
                break
        if judge:
            gate_left[nmae]={'ymax':gates_origin[nmae]['parameters']['ymax'],'ymin':gates_origin[nmae]['parameters']['ymin'],'K':gates_origin[nmae]['parameters']['K'],'n':gates_origin[nmae]['parameters']['n']}
            gate_poten[nmae]={'ymax':gates_origin[nmae]['parameters']['ymax'],'ymin':gates_origin[nmae]['parameters']['ymin'],'K':gates_origin[nmae]['parameters']['K'],'n':gates_origin[nmae]['parameters']['n']}
    
    for k in range(len(chain_c)):
        gate_poten[chain_c[k].name]={'ymax':gates_origin[chain_c[k].name]['parameters']['ymax'],'ymin':gates_origin[chain_c[k].name]['parameters']['ymin'],'K':gates_origin[chain_c[k].name]['parameters']['K'],'n':gates_origin[chain_c[k].name]['parameters']['n']}
    k=0
    gate={'ymax':gates_origin[chain_c[k].name]['parameters']['ymax'],'ymin':gates_origin[chain_c[k].name]['parameters']['ymin'],'K':gates_origin[chain_c[k].name]['parameters']['K'],'n':gates_origin[chain_c[k].name]['parameters']['n']}
    
    
    
        
    
    caculate(start_para[0],start_para[1],start_para[2],start_para[3],gate)
    
    
    
    
    """
    here is trying to convert the inputs
    the output of a gate should be transformed in other order 
    since the not gate flip everthing, low_bound_off will turn into high_bound_on
    low turn into high
    on turn into off
    
    """
    a=1
    b=0
    right=[]
    left=[]
    if circuit.compoent_list[circuit.come[nor][0]].score<circuit.compoent_list[circuit.come[nor][1]].score:
        a=0
        b=1
        circuit.compoent_list[circuit.come[nor][1]]
        right=circuit.compoent_list[circuit.come[nor][1]].translate_1() 
    
    else:    
        right.circuit.compoent_list[circuit.come[nor][0]].translate_1()   
    before=circuit.come[nor][a]
    if len(circuit.come[before])!=2:
        left=circuit.compoent_list[circuit.come[before][0]].translate_1()
      
    else:
        befor_right=[]
        befor_left=[]
        temp_a=circuit.compoent_list[circuit.come[before][0]].translate_1()
        temp_b=circuit.compoent_list[circuit.come[before][1]].translate_1()
    
        left=combine[temp_a,temp_b]
     
     
    """
    from here is where we try to imporve the K and ymax&ymin to imporve the score
    the changed parameter is saved in the gates_origin which can be write into ucf 
    which we haven't sure about it
    
    
    
    change K is similiar to change ymax&ymin
    difference is that change K make one gate match the inputs
    while changing ymax&ymin make one gate's outputs match the next gate
    the changed ymax&ymin value can be caculate by the same method for K, BUT applied to the next gate
    what we meant 'match' is that imporve the  score
    
    x/K
    
    
    the algorithms is limited, tested on 0xFE.v
    it focus on the last nor gate before the outputs
    change the nor gate itself and one of its input gate, one with lower score
    
    """
    wait=gates_origin[circuit.compoent_list[circuit.come[nor][a]].name]['parameters']
    changed={'ymax':wait['ymax'],'ymin':wait['ymin'],'K':wait['K'],'n':wait['n']}
    K,sc=caculate(left[0],left[1],left[2],left[3],changed)
    new=x_to_y(changed['ymax'],changed['ymin'],K,changed['n'],left[2])
    dna_factor=right[1]/new        
    
    for a in range(4):
        left[a]=x_to_y(dna_factor*changed['ymax'],dna_factor*changed['ymin'],K,changed['n'],left[a])
    
    pp=[left[3],left[2],left[1],left[0]]
    left=pp
    
    left=combine(left,right)
    
    wait=gates_origin[circuit.compoent_list[nor].name]['parameters']
    changed={'ymax':wait['ymax'],'ymin':wait['ymin'],'K':wait['K'],'n':wait['n']}
    K1,sc1=caculate(left[0],left[1],left[2],left[3],changed)
    
    for a in range(4):
    
        left[a]=x_to_y(changed['ymax'],changed['ymin'],K1,changed['n'],left[a])
    pp=[left[3],left[2],left[1],left[0]]
    left=pp
    
    
    
    last=gates_origin[circuit.compoent_list[1].name]['parameters']
    
    left=pp
    
    K2,sc2=caculate(left[0],left[1],left[2],left[3],last)
    
    print(K2,sc2)
    
    
    print(circuit.come[nor])
    
    circuit.come[nor][a]
    circuit.compoent_list[circuit.come[nor][a]].name
    circuit.compoent_list[1].name
    
    gates_origin[circuit.compoent_list[nor].name]['parameters']['K']=K1
    gates_origin[circuit.compoent_list[nor].name]['parameters']['ymax']=(K2/gates_origin[circuit.compoent_list[nor].name]['parameters']['K'])*gates_origin[circuit.compoent_list[nor].name]['parameters']['ymax']
    gates_origin[circuit.compoent_list[nor].name]['parameters']['ymin']=(K2/gates_origin[circuit.compoent_list[nor].name]['parameters']['K'])*gates_origin[circuit.compoent_list[nor].name]['parameters']['ymin']
    
    gates_origin[circuit.compoent_list[circuit.come[nor][a]].name]['parameters']['K']=K
    gates_origin[circuit.compoent_list[circuit.come[nor][a]].name]['parameters']['ymax']=dna_factor*gates_origin[circuit.compoent_list[nor].name]['parameters']['ymax']
    gates_origin[circuit.compoent_list[circuit.come[nor][a]].name]['parameters']['ymin']=dna_factor*gates_origin[circuit.compoent_list[nor].name]['parameters']['ymin']
    
    print('imporved score, at least i think so......')
    print(sc2)