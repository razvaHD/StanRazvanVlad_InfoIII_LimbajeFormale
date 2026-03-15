
def concatstrings(str1, str2):
    return str1 + str2
def getreverse(string):
    reverse=""
    for charact in string:
        reverse=charact+reverse
    return reverse
def getlen(string):
    i=0
    for charact in string:
        i=i+1
    return i
def repeat(string, n):
    result=string
    while(n>1):
        result=result+string
        n=n-1
    return result
def reverse(string):
    reverse=""
    isxy=False
    for charact in string:
        if isxy:
            reverse=reverse[0]+charact+reverse[1:]
            isxy=False
        else:
            reverse=charact+reverse
        if charact=='x' or charact=='y':
            isxy=True
    return reverse
def extract(string, i, j):
    inceput=i
    sfarsit=j-i
    rezultat=string[inceput:]
    rezultat=rezultat[:sfarsit]
    print(rezultat)
    return rezultat

def is_palindrom(string):
    for i in range(len(string)):
        if string[i]!=string[-i-1]:
            return False
    return True

def recurs_pal(string, rang, nr):
    if(nr<0):
        return
    else:
        if is_palindrom(string):
            print(string)
        for i in range(rang):
            recurs_pal(string+str(i), rang, nr-1)

def follows_rules(string):
    return is_palindrom(string)

def recurs_gramatica(string, dictA, nr):
    if(nr<0):
        return
    else:
        if follows_rules(string):
            print(string)
        for i in range(len(dictA)):
            recurs_gramatica(string+str(dictA[i]), dictA, nr-1)


def ex1():
    string1="abca"
    string2="xyzxy"
    string3="23123"
    print("concat:"+concatstrings(string1, string2))
    print("reverse:"+getreverse(string1))
    print("substitute:"+string1.replace('a', 'c'))
    print(len(string1))
def ex2():
    string1="578651"
    string2="abacedafa"
    string3="x1x2y1y2y1x1"
    print("concat:"+concatstrings(string1, string2))
    print("repeat:"+repeat(string1, 3))
    print("reverse:"+reverse(string3))
    print("substitute:"+string3.replace('x1', "y2"))
    print(len(string1))

def ex3():
    recurs_pal("", 3, 5)
def ex4():
    a={0:'a', 1:'b'}
    recurs_gramatica("", a, 2)



if __name__ == "__main__":
    # string1=input("String 1: ")
    # string2=input("String 2: ")
    # result = concatstrings(string1, string2)
    # print("rezultat:"+result)
    # reverse=getreverse(result)
    # print("invers:"+reverse)
    # a=input("Simbolul de substituit din rezultat: ")
    # b=input("Simbolul cu care se substituie in rezultat: ")
    # result=result.replace(a, b)
    # print("rezultat:"+result)
    # print("lungime:"+str(getlen(result)))
    #print(reverse(string1))
    #extract("aaabbbcccdddeee", 3,6)
    #print(is_palindrom("abba"))
    #recurs_pal("", 5)
    # print("ex1:")
    # ex1()
    # print("ex2:")
    # ex2()
    # print("ex3:")
    # ex3()
    print("ex4:")
    ex4()

