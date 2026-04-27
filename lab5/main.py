import random
def mealy(word):
    S0={
        (0,0): '0',
        (1,0): '0',
        (0,1): '1',
        (1,1): '1'
    }
    S1={
        (0,0): '1',
        (1,0): '1',
        (0,1): '0',
        (1,1): '0'
    }
    state='0'
    out=''
    while word:
        match state:
            case '0':
                out+=S0[word[0]]
                state=S0[word[0]]
                word=word[1:]
            case '1':
                out+=S1[word[0]]
                state=S1[word[0]]
                word=word[1:]
            case _:
                print(state)
    return out
def get_random_symbol(symbols):
    nr=(random.randint(len(symbols)))
    return symbols[nr]

def repeat_symbol(symbols, strin,iterations):
    if iterations==0:
        print(strin+'a')
        return
    repeat_symbol(symbols, strin,iterations-1)
    for symbol in symbols:
        repeat_symbol(symbols, strin+symbol,iterations-1)
def ex2():
    repeat_symbol(['a','b'], 'b', 2)
    

if __name__ == "__main__":
    #print(mealy([(0,0), (0,1), (0,0), (1,1), (1,1)]))
    ex2()