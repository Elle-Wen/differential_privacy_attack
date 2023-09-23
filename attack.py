import random

# fix assured values if {a} contains 2 special cases: 
# 1. a_{i+1}-a_i = 2 -> a_i = r_i, a_{i+1}-1 = r_{i+1}
# 2. a_i - a_x = 1 for x>i -> a_i - 1 = r_i, a_x = r_x
# given input sequence a, output modified sequence p s.t. p_i is either = r_i or -0.1(using an impossible value to represent unsured r_i)
# as other lists in this project, we set p[0] = 0 for convenience 
def special_case(a):
    length = len(a)
    p = [0]+ [-0.1]* (length-1)
    #check case 1
    for i in range (1,length-1):
        if a[i+1] - a[i] == 2:
            p[i] = a[i]
            p[i+1] = a[i+1] - 1
            a[i+1] = a[i+1] - 1 
    #check case 2
    while True: 
        mark = True # a indicator showing that if there is still case 2 in sequence a 
        for i in range (1,length-1):
            if a[i] - a[i+1] == 1:
                mark = False 
                p[i+1] = a[i+1]
                p[i] = a[i] - 1 
                a[i] = a[i] - 1
                for j in range (i+1, length):
                    if a[j] == a[i+1]: 
                        p[j] = a[j]
        if mark == True:
            break 
    return p 