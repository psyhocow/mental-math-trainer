import random as rnd

a = rnd.randint(1, 10)
b = rnd.randint(1, 10)   

def replacing(a):
    s = a.replace('*', '')
    s = s.replace(' ', '')
    return(s)

def squaresDifference(a, b):
    
    print(f"{a}² - {b}² = ?")
    
    try: c = input()
    except: print('You must input a string!')
    
    st = replacing(c)
    if st == str(f'({a}-{b})({a}+{b})'): print(True)
    elif st == f'({a}+{b})({a}-{b})': print(True)
    else: print(False)    
    
squaresDifference(a, b)