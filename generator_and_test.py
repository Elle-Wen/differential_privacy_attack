
# HW 2 for CS386
import random
import statistics
import attack 

# --------------------------------------------------------------------
# data generator
# data representation is four lists. 
# The first is sequence s 
# The second is a sequence r s.t. r_i = sum_0^i s_i, which is the real total votes at each real time. 
# The third is the released data sequence a 
# The fourth is the guess with 2/3 accuracy for part 2. It is 1 for D, 0 for non-D.

#the first value of the lists is made to be 0 to make things more strightforward

def generate_data(n):
    sequence_s = [0] * (n+1)
    real = [0] * (n+1)
    released = [0] * (n+1)
    guess = [0] * (n+1)

    for i in range(1, n+1):
        if random.random() < 0.5: #vote for democrat
            sequence_s[i] = 1 
            real[i] = real[i-1] + 1
            if random.random() < 0.66:
                guess[i] = 1
            else:
                guess[i] = 0
        else:                    #vote for republican 
            sequence_s[i] = 0
            real[i] = real[i-1]
            if random.random() < 0.66:
                guess[i] = 0
            else:
                guess[i] = 1
        if random.random() < 0.5: #flip coin to decide if needs to adds 1
            released[i] = real[i]
        else:
            released[i] = real[i] + 1
    return (sequence_s, real, released, guess)

# --------------------------------------------------------------------
# accuracy analysis

# performs 1000 run on n=50000 and returns a tuple of the
# accuracy of the attack without and with prior info respectively.

def evaluate(n): # n is the number of bits 
    case1_success_rate_gather = []
    case1_stats = []
    case2_success_rate_gather = []
    case2_stats = []
    for i in range (4): # how many times we perform the attack 
        print(i)
        generaed_list = generate_data(n)
        released = generaed_list[2]
        real = generaed_list[1] 
        g = generaed_list[3]
        print("released", released)
        print("real", real)
        print("g", g)
        case1_guess = attack.attack1(released)
        case2_guess = attack.attack2(released,g)
        print("case2_guess", case2_guess)

        case1_correct = 0
        case2_correct = 0
        for i in range(1,n+1):
            if case1_guess[i] == real[i]:
                case1_correct += 1
            if case2_guess[i] == real[i]:
                case2_correct += 1
        success_rate_1 = case1_correct / n
        success_rate_2 = case2_correct / n
        case1_success_rate_gather.append(success_rate_1)
        case2_success_rate_gather.append(success_rate_2)
    case1_stats.append(statistics.mean(case1_success_rate_gather))
    case1_stats.append(statistics.stdev(case1_success_rate_gather))
    case2_stats.append(statistics.mean(case2_success_rate_gather))
    case2_stats.append(statistics.stdev(case2_success_rate_gather))
    return (case1_stats, case2_stats) 
