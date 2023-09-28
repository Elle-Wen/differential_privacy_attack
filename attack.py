import random
from collections import Counter
# fix assured values if {a} contains 2 special cases: 
# 1. a_{i+1}-a_i = 2 -> a_i = r_i, a_{i+1}-1 = r_{i+1}
# 2. a_i - a_x = 1 for x>i -> a_i - 1 = r_i, a_x = r_x
# given input sequence a, output modified sequence p s.t. p_i is either = r_i or -0.1(using an impossible value to represent unsured r_i)
# as other lists in this project, we set p[0] = 0 for convenience 
def fix_special_case(a): # a got changed here!
    length = len(a)
    p = [0]+ [-0.1]* (length-1)
    #check case 1
    for i in range (0,length-1):
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

# let {f_i} be the set of fixed points that we get from the special case calculted above. p = ... f_1 ... f_2 ...  
# let interval = [f_1 ... f_2] ]
# all_possible gets "interval" as input and return a list of all possible fillings of bits in between f_1 and f_2 eg. the output for interval = [1,_,_,2] is [[1,1],[1,2],[2,2]]
def all_possible(list):
    def backtrack(current, index):
        if current[-1] > last:
            return
        if index == len(list) - 2:
            if last - current[-1] > 1:
                return 
            else:
                result.append(current.copy())
                return
        if list[index] == -0.1:
            for next_val in [current[-1], current[-1] + 1]:
                current.append(next_val)
                backtrack(current, index + 1)
                current.pop()
    result = []
    first, last = list[0], list[-1]
    for int in [first, first + 1]:
        backtrack([int], 1)
    return result
def all_possible_with_endpoints(list):
    def backtrack(current, index):
        if current[-1] > last:
            return
        if index == len(list) - 2:
            if last - current[-1] > 1:
                return 
            else:
                result.append(current.copy())
                return
        if list[index] == -0.1:
            for next_val in [current[-1], current[-1] + 1]:
                current.append(next_val)
                backtrack(current, index + 1)
                current.pop()
    result = []
    first, last = list[0], list[-1]
    for int in [first, first + 1]:
        backtrack([int], 1)
    for item in result:
        item.append(last)
        item.insert(0,first)
    return result
# pick_highest gets nested_list = [[a_1,a_2,...,a_n],[b_1,b_2,...,b_n],...,[m_1,...,m_n]] and return ls = [x_1,x_2,...,x_n] s.t. x_1 occurs the most in a_1,b_1,...,m_1, x_2 occurs the most in a_2,b_2,...,m_2, ..., break tie by choosing the greater one (because it has more chance to be "leagl")
def pick_highest(nested_list):
    ls = []
    for col in zip(*nested_list): #zip transpose the nested list 
        col_counter = Counter(col)
        # Get the most common element(s)
        most_common = col_counter.most_common()
        # If there is only one element, add it to the result
        if len(most_common) == 1:
            ls.append(most_common[0][0])
        else:
            # If there is a tie, choose the greater one
            max_count = most_common[0][1]
            max_element = most_common[0][0]
            for element, count in most_common[1:]:
                if count > max_count or (count == max_count and element > max_element):
                    max_count = count
                    max_element = element
            ls.append(max_element)
    return ls

def pick_highest_weight(nested_list,guess): #nested_list=all possible fillings + fixed endpoints [[f_1,possible,possible,...f_n],[f_1,possible,possible,...f_n],...], guess = [-0.2,1,0,0,...,-0.2], same length as inner lists, return only the inner guess
    ls = [] # votes excluding endpoints [0,1,1,0,...]
    first = nested_list[0][0]
    last = nested_list[0][-1]
    votes_all_possible = [] # votes excluding endpoints [[1,0,1],[0,1,0],...]
    #first turn all increments to votes 
    for item in nested_list:
        votes_all_possible.append(increment_to_votes(item))    
    index = 1
    for col in zip(*votes_all_possible): #zip transpose the nested list 
        col_counter = Counter(col)
        if guess[index] == 1:
            if col_counter.get(1) != None:
                col_counter[1] = col_counter[1] * 2 # +1 for each correct matching
        elif guess[index] == 0:
            if col_counter.get(0) != None:
                col_counter[0] = col_counter[0] * 2
        # Get the most common element(s)
        most_common = col_counter.most_common()
        # If there is only one element, add it to the result
        if len(most_common) == 1:
            ls.append(most_common[0][0])
        else:
            # If there is a tie, choose the greater one, more chance to be legal
            max_count = most_common[0][1]
            max_element = most_common[0][0]
            for element, count in most_common[1:]:
                if count > max_count or (count == max_count and element > max_element):
                    max_count = count
                    max_element = element
            ls.append(max_element)
        index += 1
    # now convert back the votes to increments ls is votes exclusing endpoints, first is the first fixed point
    result = votes_to_increment(ls,first)
    return result 

# this function split the list but cutting off all -0.1s at the end of the list (if any)
def split_list(ls): # ls = [a_1,a_2,...,a_n] where a_i is either a fixed point or -0.1, return a list of intervals [[a_1,a_2,...,a_n],[b_1,b_2,...,b_n],...,[m_1,...,m_n]] where a_1,b_1,...,m_1 and a_n,b_n,...,m_n are all fixed points
    p = []  # Resulting list of intervals
    interval = []  # Current interval
    for item in ls:
        if item != -0.1:
            if interval: # a python thing... [] is falsy, [x] is truthy 
                interval.append(item)
                p.append(interval)
                interval = [item]
            else:
                interval.append(item)
        else:
            interval.append(item)
    return p 

def split_guess(ls): # ls = [a_1,a_2,...,a_n] where a_i is either a non-negative value or -0.2, return a list of intervals [[a_1,a_2,...,a_n],[b_1,b_2,...,b_n],...,[m_1,...,m_n]] where a_1,b_1,...,m_1 and a_n,b_n,...,m_n are -0.2s
    p = []  # Resulting list of intervals
    interval = []  # Current interval
    for item in ls:
        if item == -0.2:
            if interval: # a python thing... [] is falsy, [x] is truthy 
                interval.append(item)
                p.append(interval)
                interval = [item]
            else:
                interval.append(item)
        else:
            interval.append(item)
    return p 

def last_interval_hanlder (mid_result,last_fixed_point,fix_mid_result): # return the final guess, fix_mid_result is [0,....,last_fixed]
    if mid_result[-1] != -0.1:
        return mid_result
    else:
        count = 0 
        if fix_mid_result == []:
            last_interval = mid_result
            for i in range(len(mid_result)-1,-1,-1): 
                if mid_result[i] == -0.1:
                    count += 1
        else: 
            last_interval = [] 
            # get the count and get the last_interval
            for i in range(len(mid_result)-1,-1,-1): 
                if mid_result[i] == -0.1:
                    last_interval.insert(0,-0.1)
                    count += 1
                else: 
                    last_interval.insert(0,last_fixed_point)
                    break 
        possibles = [] 
        j = 0 
        for i in range (count+2): 
            possibles.extend(all_possible(last_interval+[last_fixed_point+j]))
            j = j + 1 
        last_interval_guess = pick_highest(possibles)
        result = fix_mid_result +[last_fixed_point] + last_interval_guess
        return result 
def last_interval_hanlder_weight(mid_result,last_fixed_point,fix_mid_result,guess): # return the final guess, fix_mid_result is [0,....,last_fixed]
    print("mid_result",mid_result)
    print("last_fixed_point",last_fixed_point)
    print("fix_mid_result",fix_mid_result)
    print("guess",guess)
    guess_endpoint = guess + [-0.2]
    if mid_result[-1] != -0.1:
        return mid_result
    else:
        count = 0 
        if fix_mid_result == []:
            last_interval = mid_result
            for i in range(len(mid_result)-1,-1,-1): 
                if mid_result[i] == -0.1:
                    count += 1
        else: 
            last_interval = [] 
            # get the count and get the last_interval
            for i in range(len(mid_result)-1,-1,-1): 
                if mid_result[i] == -0.1:
                    last_interval.insert(0,-0.1)
                    count += 1
                else: 
                    last_interval.insert(0,last_fixed_point)
                    break 
        possibles = [] 
        j = 0 
        for i in range (count+2): 
            possibles.extend(all_possible_with_endpoints(last_interval+[last_fixed_point+j]))
            j = j + 1 
        print("possibles",possibles)
        last_interval_guess = pick_highest_weight(possibles,guess_endpoint) 
        print("last_interval_guess",last_interval_guess)
        result = fix_mid_result +[last_fixed_point] + last_interval_guess
        return result 
def attack1 (a):
    sequence_fixed_points = fix_special_case(a)
    sequence_intervals = split_list(sequence_fixed_points) # without of the last few -0.1s 
    if sequence_intervals == []: # if sequence_fixed_points is [0,-0.1,-0.1,...], sequence_intervals will be []
        fix_mid_result = [] 
        result = last_interval_hanlder(sequence_fixed_points,0,fix_mid_result)
        return result 
    mid_result = [] 
    for item in sequence_intervals: 
        if len(item) == 2: 
            guess_intervals = [] # deal with eg. [1,2], [1,1]
        else:
            guess_intervals = pick_highest(all_possible(item)) 
        mid_result.append(item[0])
        mid_result = mid_result + guess_intervals
    last_fixed_point = sequence_intervals[-1][-1]
    fix_mid_result = mid_result.copy() 
    mid_result.append(last_fixed_point)
    for i in range(len(sequence_fixed_points)-1,-1,-1): # append potential -0.1s 
        if sequence_fixed_points[i] == -0.1:
            mid_result.append(-0.1)
        else:
            break
    # now mid_result is the guess [a,b,c,d,...,(-0.1,-0.1)]
    #now we deal with the remaining -0.1s 
    result = last_interval_hanlder(mid_result,last_fixed_point,fix_mid_result) 
    return result

def increment_to_votes(ls): # ls are legal jumps [fix,_,_,_,fix], outputs [0,1,1]
    length = len(ls)
    vote = [] 
    for i in range (1,length-1):
        if ls[i] - ls[i-1] == 0:
            vote.append(0)
        else: # ls[i] - ls[i-1] == 1
            vote.append(1) 
    return vote
def votes_to_increment(ls,first):
# now convert back the votes to increments 
    result = []
    for i in range(len(ls)):
        if i == 0:
            if ls[i] == 0:
                result.append(first)
            else:
                result.append(first + 1)
        else:
            if ls[i]  == 0:
                result.append(result[-1])
            else:
                result.append(result[-1] + 1)
    return result
def attack2 (a,g):
    length = len(g)
    sequence_fixed_points = fix_special_case(a) # [0,-0.1,...2,-0.1,...]
    print("sequence_fixed_points",sequence_fixed_points)
    sequence_intervals = split_list(sequence_fixed_points) # without of the last few -0.1s 
    print("sequence_intervals",sequence_intervals)
    # now modify g s.t. g[i] = -0.2 if a[i] != 0.1 eg. a = [0,-0.1,-0.1,2], g = [0,1,1,0], g' = [-0.2,1,1,-0.2]
    for i in range(length):
        if sequence_fixed_points[i] != -0.1:
            g[i] = -0.2
    print("new_g",g)
    g_intervals = split_guess(g) # [[-0.2,...,-0.2],[-0.2,...,-0.2],...] cutting off last guesses
    print("g_intervals",g_intervals)
    g_last_interval = []
    for i in range(len(g)-1,-1,-1): 
                if g[i] != -0.2:
                    g_last_interval.insert(0,g[i])
                else: 
                    g_last_interval.insert(0,-0.2)
                    break
    print("g_last_interval",g_last_interval)
    if sequence_intervals == []: # if sequence_fixed_points is [0,-0.1,-0.1,...], sequence_intervals will be [], that is, if inly first value is assured
        fix_mid_result = [] 
        result = last_interval_hanlder_weight(sequence_fixed_points,0,fix_mid_result,g_last_interval) 
        return result 
    mid_result = [] 
    for i in range(len(sequence_intervals)): 
        item1 = sequence_intervals[i]
        item2 = g_intervals[i]
        print("item1",item1)
        print("item2",item2)
        if len(item1) == 2: 
            guess_intervals = [] # deal with eg. [1,2], [1,1]
        else:
            a = all_possible_with_endpoints(item1)
            guess_intervals = pick_highest_weight(a,item2) 
            print("guess_intervals",guess_intervals)
        mid_result.append(item1[0])
        mid_result = mid_result + guess_intervals
    last_fixed_point = sequence_intervals[-1][-1]
    fix_mid_result = mid_result.copy() 
    mid_result.append(last_fixed_point)
    for i in range(len(sequence_fixed_points)-1,-1,-1): # append potential -0.1s 
        if sequence_fixed_points[i] == -0.1:
            mid_result.append(-0.1)
        else:
            break
    # now mid_result is the guess [a,b,c,d,...,(-0.1,-0.1)]
    #now we deal with the remaining -0.1s 
    result = last_interval_hanlder_weight(mid_result,last_fixed_point,fix_mid_result,g_last_interval) 
    return result



