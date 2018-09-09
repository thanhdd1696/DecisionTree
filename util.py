import math
'''
This file contains utilities for the implementation of Decision Tree
@author: Dac Thanh Doan
'''

'''
This function returns the most common output among a set of examples
'''
def plurality_value(list):
    zeroes = 0
    ones = 0
    for i in range(0, len(list)):
        if (list[i] == 0):
            zeroes += 1
        else:
            ones += 1
    if (zeroes > ones):
        return 0
    else:
        return 1


'''
This function checks if all classifications of the set of examples are the same or not
'''
def same_classification(Y_examples):
    for i in range(0, len(Y_examples) - 1):
        if (Y_examples[i] != Y_examples[i+1]):
            return False
    return True

'''
This function checks if all attributes are selected or not
'''
def no_attributes(attr_list):
    for i in range(0, len(attr_list)):
        if (attr_list[i] == False):
            return False
    return True
'''
Calculate entropy, referencing to page 704 of text book
'''
def B(n):
    if (n == 0 or n == 1):
        return 0
    else:
        return -((n)*math.log(n,2) + (1-n)*math.log(1-n,2))
