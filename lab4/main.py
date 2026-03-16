
def con(str1, str2):
    for c in str2:
        if c not in str1:
            str1.append(c)
    return str1

def epsilon(word):
    q0={
        'a': [1,2],
        'b':[]
    }
    q1={
        'a':[1, 2],
        'b':[],
    }
    q2={
        'a':[3,4],
        'b':[2,3,4]
    }
    q3={
        'a':[3,4],
        'b':[1,2]
    }
    q4={
        'a':[],
        'b':[]
    }
    states=[0]
    while word:
        tmpstate=[]
        while states:
            match states[0]:
                case 0:
                    tmpstate=con(tmpstate, q0[word[0]])
                    states=states[1:]
                case 1:
                    tmpstate=con(tmpstate, q1[word[0]])
                    states=states[1:]
                case 2:
                    tmpstate=con(tmpstate, q2[word[0]])
                    states=states[1:]
                case 3:
                    tmpstate=con(tmpstate, q3[word[0]])
                    states=states[1:]
                case 4:
                    tmpstate=con(tmpstate, q4[word[0]])
                    states=states[1:]
        states=tmpstate
        word=word[1:]
    if 4 in states:
        return True
    return False

def moore(word):
    S1={
        'A': 1,
        'B': 2
    }
    S2={
        'A': 1,
        'B': 2
    }
    mapping={
        1:"O1",
        2:"O2"
    }
    state=1
    out=mapping[1]
    while word:
        match state:
            case 1:
                state=S1[word[0]]
                out+=mapping[state]
                word=word[1:]
            case 2:
                state=S2[word[0]]
                out+=mapping[state]
                word=word[1:]
    return out
def mealy(word):
    S1={
        'X': 2,
        'Y': 1
    }
    S2={
        'X': 1,
        'Y': 2
    }
    mapping={
        (1,'X'):"O2",
        (1,'Y'):"O1",
        (2,'X'):"O2",
        (2,'Y'):"O1"
    }
    state=1
    out=''
    while word:
        match state:
            case 1:
                out+=mapping[(state, word[0])]
                state=S1[word[0]]
                word=word[1:]
            case 2:
                out+=mapping[(state, word[0])]
                state=S2[word[0]]
                word=word[1:]
    return out




if __name__ == "__main__":
    print(moore("ABAB"))
    print(mealy("XYXY"))
    print(epsilon("aba"))