


def state0(inp):
    if(inp==0):
        return 1
    elif(inp==1):
        return 2
    return 0
def state1(inp):
    if(inp==1):
        return 0
    elif(inp==0):
        return 3
    return 1
def state2(inp):
    if(inp==1):
        return 3
    elif(inp==0):
        return 1
    return 2
def state3(inp):
    return 3

def ex2_state0(inp):
    if(inp=="c"):
        return True
    return False
def ex2_state1(inp):
    if(inp=="a"):
        return True
    return False
def ex2_state2(inp):
    if(inp=="t"):
        return True
    return False

def state_machine1():
    inp=input("Introduceti state-urile:")
    state=0
    while inp:
        match state:
            case 0:
                state=state0(int(inp[0]))
                inp=inp[1:]
            case 1:
                state=state1(int(inp[0]))
                inp=inp[1:]
            case 2:
                state=state2(int(inp[0]))
                inp=inp[1:]
    if(state==3):
        return True
    return False

def state_machine2():
    inp=input("Introduceti state-urile:")
    state=0
    while inp:
        match state:
            case 0:
                if ex2_state0(inp[0]):
                    state+=1
                else:
                    state=0
                inp=inp[1:]
            case 1:
                if ex2_state1(inp[0]):
                    state+=1
                else:
                    state=0
                inp=inp[1:]
            case 2:
                if ex2_state2(inp[0]):
                    return True
                else:
                    state=0
                inp=inp[1:]
    return False


def state_machine3():
    q0 ={
        'a':1,
        'b':0,
        'c':0,
        'd':0,
    }
    q1 ={
        'a':1,
        'b':2,
        'c':1,
        'd':1,
    }
    q2 ={
        'a':2,
        'b':2,
        'c':2,
        'd':3,
    }
    q3 ={
        'a':3,
        'b':3,
        'c':3,
        'd':3,
    }
    state=0
    inp=input("Introduceti cuvantul:")
    if len(inp)>6:
        return False
    
    while inp:
        if not (inp[0]=='a' or inp[0]=='b' or inp[0]=='c' or inp[0]=='d'):
            return False
        match state:
            case 0:
                state=q0[inp[0]]
                inp=inp[1:]
            case 1:
                state=q1[inp[0]]
                inp=inp[1:]
            case 2:
                state=q2[inp[0]]
                inp=inp[1:]
            case 3:
                state=q3[inp[0]]
                inp=inp[1:]
    if state==3:
        return True
    return False

def regexstar(regex,text):
    if text[0]=='*':
        text=text[1:]
    state=0
    for letter in text:
        if letter==regex[state+1]:
            state+=1
        else:
            state=0
        if state>=(len(regex)-1):
            return True
    return False

def getnumarregex(regex,text):
    state=0
    while text:
        if text[0]==regex[state]:
            state+=1
        else:
            state=0
        text=text[1:]
        if state>=len(regex):
            break
    if text=="":
        return "nu este"
    po=1
    nr=""
    while (text and ((text[0]>='0')and(text[0]<='9'))):
        nr+=text[0]
        text=text[1:]
    if nr=="":
        return False
    return int(nr)

def getnumeregex(regex, text):
    state=0
    while text:
        if text[0]==regex[state]:
            state+=1
        else:
            state=0
        text=text[1:]
        if state>=len(regex):
            break
    if text=="":
        return "nu este"
    po=1
    nr=""
    while (text and (((text[0]>='a')and(text[0]<='z')or ((text[0]>='A')and(text[0]<='Z'))or text[0]==" "))):
        nr+=text[0]
        text=text[1:]
    if nr=="":
        return False
    if text and text[0]=='.':
        nr+='.'
    return nr

if __name__ == "__main__":
    file = open("factura.txt", "r")
    text = file.read()
    print("Firma:"+str(getnumeregex("Firma:",text)))
    print("TVA:"+str(getnumarregex("TVA:",text)))
    print("Total:"+str(getnumarregex("Total:",text)))
    print("Bune maniere:"+str(regexstar("*O zi placuta",text)))

