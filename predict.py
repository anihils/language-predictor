import math
import string

'''
This function parses e.txt and s.txt to get the  26-dimensional multinomial
parameter vector (characters probabilities of English and Spanish) as
descibed in section 1.2 of the writeup

Returns: tuple of vectors e and s
'''
def get_parameter_vectors():
    # p[0]: the probability of 'A'
    e=[0]*26 # Implementing vectors e,s as lists of length 26
    s=[0]*26

    # s.txt and e.txt only contain letters and avg probabilities
    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            char, prob = line.strip().split(" ")
            #strip: removes the newline character
            #split: returns list of words separated by space
            e[ord(char) - ord('A')] = float(prob)
            #ord(char) gives the ASCII (integer) value of the character
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

e, s = get_parameter_vectors() # don't call function again

'''
Shreds given test file: Returns a list containing frequencies of each alphabetic 
character in the text
'''
def shred(filename):
    freq = dict.fromkeys(string.ascii_uppercase, 0)

    with open(filename, encoding='utf-8') as f:
        for line in f:
            words = line.strip().split(" ")
            # check each characters ASCII
            for word in words:
                word = word.upper()
                for idx in range(0, len(word)):
                    if word[idx].isalpha():
                        freq[word[idx]] = freq[word[idx]] + 1
    return freq

'''
Helper function to calculate conditional probability
'''
def x_logp(idx):
    c = chr(65 + idx)
    x = shred(filename)[c]
    x_loge = x*math.log(e[idx])
    x_logs = x*math.log(s[idx])
    return (x_loge, x_logs)

'''
This function calculates F(Y = y); y = {English, Spanish}
F(y) = log(f(y)) = log(P(Y = y)) +  Summation (X[i] * logp(y[i])
'''
def func_y():
    X = list(shred(filename).values())
    Py_s = 0.4 # P(Y = Spanish)
    Py_e = 0.6 # P(Y = English)
    Fy_e = math.log(Py_e)
    Fy_s= math.log(Py_s)
    for i in range(26):
        sum_e, sum_s = x_logp(i)
        Fy_e += sum_e
        Fy_s += sum_s
    return Fy_e, Fy_s

'''
 Returns the probability of given .txt file being in English
'''
def predict():
    Fy_e, Fy_s = func_y()
    if Fy_e - Fy_s >= 100:
        return 0
    elif Fy_e - Fy_s <= -100:
        return 1
    else:
        return 1/(1 + math.exp(Fy_s - Fy_e))

'''
Function printing readable output for confident predictions
'''
def print_predict():
    if predict() > 0.7:
        print('Language: English')
    elif predict() < 0.3:
        print('Language: Spanish')

filename = input("Enter .txt filename: ")
print('Probability that given text is English:', format(predict(), '.4f'))
print_predict()
