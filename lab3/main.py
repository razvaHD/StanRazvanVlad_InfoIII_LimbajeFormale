import time


def ex1():
    state=0
    q0={
        "C":1,
        "T":2,
        "A":3,
        "H":4,
        "c":1,
        "t":2,
        "a":3,
        "h":4
    }
    choice=False
    inp=""
    while not choice:
        inp=input("Alegeti optiunea:\n-Cafea:c\n-Ceai:t\n-Cappuccino:a\n-Ciocolata calda:h\n->")
        if((inp=='c')or(inp=="C")or(inp=='t')or(inp=="T")or(inp=='a')or(inp=="A")or(inp=='h')or(inp=="H")):
            choice=True
    state+=q0[inp]
    choice=False
    while not choice:
        inp=input("Alegeti optiunea:\n-OK:1\n-Cancel:2\n->")
        if inp=='1':
            choice=True
            state=5
        if  inp=="2":
            return False
    print("Se prepara")
    time.sleep(5)

def ex2(parcari):
    state=1
    q1={
        '1':1,
        '0':0
    }
    ocupat={
        0:"Liber",
        1:"Ocupat"
    }
    choice=False
    inp=""
    while not choice:
        inp=input("Alegeti optiunea:\n-Intrati in parcare:1\n-Plecati:0\n->")
        if((inp=='1')or(inp=='0')):
            choice=True
    state+=q1[inp]
    if state==1:
        return parcari
    choice=False
    parcaretmp=0
    while not choice:
        print("Alegeti parcarea:\n-0:inapoi")
        i=0
        for parcare in parcari:
            print("-Parcarea "+str(i+1)+" "+ ocupat[parcare])
            i+=1
        inp=input("->")
        if inp.isnumeric() and int(inp)<=len(parcari):
            parcaretmp=int(inp)-1
            choice=True
    if parcaretmp<0:
        return parcari
    choice=False
    state+=1
    while not choice:
        inp=input("Alegeti optiunea:\n-0:iesiti\n-1:eliberati\n-2:ocupati\n->")
        if inp.isnumeric() and (inp=='1' or inp=='2') and inp!=str(parcari[parcaretmp]-1):
            parcari[parcaretmp]=(parcari[parcaretmp]+1)%2
            return parcari
        if inp.isnumeric() and (inp=='0'):
            return parcari


def con(str1, str2):
    for c in str2:
        if c not in str1:
            str1.append(c)
    return str1

def ex3(inp):
    q0={
        '0':[0,1,2],
        '1':[1,2],
        '2':[2]
    }
    q1={
        '0':[],
        '1':[1,2],
        '2':[2]
    }
    q2={
        '0':[],
        '1':[],
        '2':[2]
    }
    states=[0]
    while inp:
        tmpstate=[]
        while states:
            match states[0]:
                case 0:
                    tmpstate=con(tmpstate, q0[inp[0]])
                    states=states[1:]
                case 1:
                    tmpstate=con(tmpstate, q1[inp[0]])
                    states=states[1:]
                case 2:
                    tmpstate=con(tmpstate, q2[inp[0]])
                    states=states[1:]
        states=tmpstate
        inp=inp[1:]
    if 2 in states:
        return True
    return False

if __name__ == "__main__":
    print(ex3("02000011"))