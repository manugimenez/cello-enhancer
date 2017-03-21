import json
import sys





gates={}


# extracted the information about gates
def read_store_UCF(filepath,gates):
    filepath = 'Eco1C1G1T1.UCF.json'
    filetext = open(filepath, 'r').read()
    filejson = json.loads(filetext)
    
    ucf = []
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
           
           

def threshold(ymax,ymin,K,n):
    y=ymin/2
    x_on=((ymax-y)/(y-ymin))**n
    x_on=K*x_on
    y=ymax/2
    x_off=((ymax-y)/(y-ymin))**n
    x_off=K*x_off   
    return x_on, x_off




filepath = 'Eco1C1G1T1.UCF.json'
def alter_UCF(filepath):
    
    filetext = open(filepath, 'r').read()
    filejson = json.loads(filetext)
    
    
    
    for obj in filejson:
        if obj['collection'] == 'response_functions':       
            for ga in gates:
               if obj['gate_name']==ga:  
                   for k in obj['parameters']:
                       if k['name']=='ymax':
                           k['value']=gates[ga]['parameters']['ymax']
                       if k['name']=='ymin':
                           k['value']=gates[ga]['parameters']['ymin']
                       if k['name']=='K':
                           k['value']=gates[ga]['parameters']['K']
                       if k['name']=='n':
                           k['value']=gates[ga]['parameters']['n']
                   for k in obj['variables']:
                       x_on, x_off =threshold(gates[ga]['parameters']['ymax'],gates[ga]['parameters']['ymin'],gates[ga]['parameters']['K'],gates[ga]['parameters']['n'])
                       if k['name']=='off_threshold':
                           k['value']=x_off
                       if k['name']=='on_threshold':
                           k['value']=x_on                     
                           
                           
                           
            ucf.append(obj)
        else:
            ucf.append(obj)
    
    with open('data.json', 'w') as f:
         json.dump(ucf, f, indent=2)    







