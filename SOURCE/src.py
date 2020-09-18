import numpy as np

# read input file
def readFile(myFile):
    with open(myFile, 'r') as f:
        list1 = [] # list1 contains clause_in_query_alpha
        num_clause_query_alpha = f.readline() # read number clause of query alpha
        clause_in_query_alpha = f.readline() # read clause in query alpha
        list1.append(clause_in_query_alpha.strip().split('\n')) # remove character '\n' in list1
        num_clause_kb = f.readline() # read number clause KB
        clause_in_kb = f.readlines() # read to end of file to get clause in KB
        list2 = [element.strip().split(' OR ') for element in clause_in_kb] # remove character 'OR' in list2
    return num_clause_query_alpha, list1, num_clause_kb, list2

# check a merge_clause is pointless or not
def checkPointlessMerge(merge_clause):
    for ci in range(len(merge_clause)):
        for cj in range(len(merge_clause)):
            # after merging Ci, Cj to merge_clause 
            # if merge_clause is pointless, retrun True and start resolving
            if isPointless(merge_clause[ci], merge_clause[cj]): return True
    return False

# convert alpha from '-A' to 'A' and from 'A' to '-A'
def convert_negate(s):
    new_list = []
    s = [str(i) for i in s]
    res = str("".join(s))  
    if res[0] == '-': negate = res[1]
    elif res[0] != '-': negate = '-' + res[0] 
    new_list.append(negate)
    return new_list

# implement propositional logic resolution
def PL_Resolution(KB, alpha, f):
    clauses = KB[:] # claues can change, so copy from original list KB
    # convert negative alpha to positive alpha and else positive alpha to negative alpha
    # because in our test file input.txt, alpha is -A
    # so -A OR B resolve with negative -A = -A OR B resolve with A = B 
    # similarly, example if our alpha is positive B and clause in KB is -A OR B
    # we convert alpha positive B to -B -> -A OR B resolve with -B = -A
    negate_alpha = convert_negate(alpha)
    clauses.append(negate_alpha)
    while True:
        count = 0 # count number of clauses generated in loop
        new_clause = [] # create an empty list for storing new_clause 
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1,n)]
        # for each pair of clauses in Ci, Cj in clauses
        for (ci, cj) in pairs:
            # merge ci, cj and check if's pointless such as ['-A', 'A', '-B']
            if checkPointlessMerge(merge(ci, cj)):
                resolvents = PL_Resolve(ci, cj) # resolve it by keeping -B and remove pointless
                resolvents.sort(key=lambda kv:kv[-1], reverse=False) # sort by alphabet after resolving
                if False in resolvents: return True # if resolvents contains the empty clause then return true
                if Empty(resolvents):
                    count += 1 # increase number of clauses generated in loop after generating all new sentences from KB
                    f.write(str(count)) # write to file number of clauses generated in loop
                    f.write('\n')
                    for i in range(len(new_clause)):
                        result = new_clause[i]
                        # convert list result to str for writing to file
                        listToStr = ' OR '.join([str(elem) for elem in result])
                        f.write(listToStr)
                        f.write('\n')
                    f.write('{}')
                    f.write('\n')
                    f.write('YES')
                    f.write('\n')
                    return True  
                # check if resolvents is not pointless and it not exists in both clauses and new_clause
                if not checkPointlessMerge(resolvents):
                    if resolvents not in clauses and resolvents not in new_clause:
                        new_clause.append(resolvents) # add those sentences to new_clause
                        count += 1 # then increase number of clauses generated in loop
        # if new_clause is empty and can't find any more empty clause
        if Empty(new_clause):
            f.write('0')
            f.write('\n')
            f.write('NO') # print No because in this case, KB doesn't entail by alpha
            f.write('\n')
            return False
        f.write(str(count)) # write to file number of clauses generated in loop
        f.write('\n')
        for i in range(len(new_clause)):
            result = new_clause[i]
            # convert list result to str for writing to file
            listToStr = ' OR '.join([str(elem) for elem in result])
            f.write(listToStr)
            f.write('\n')
        clauses += new_clause # add new_clause to clauses

def flattenMerge(clause):
    return sorted(set(clause)) # sort merge_clause
        
def merge(ci, cj):
    merge_clause = ci + cj # merge two clause
    flattenMerge(merge_clause) # then flatten it
    return merge_clause

def NegativeCharacter(character):
    return '-{}'.format(character) # check if a character is negative, ex: '-A'

def isPointless(ci, cj):
    # if has a negative character of a character in list, return True, ex: ['-A', 'A', '-B'] 
    if ci == NegativeCharacter(cj) or NegativeCharacter(ci) == cj: return True
    return False

def Empty(clause):
    return len(clause) == 0 # check if a clause is empty

def unique(list1):
    # get unique values from a list, ex original list: 1 2 1 1 3 4 3 3 5 
    # list contains all unique values: 1 2 3 4 5 
    x = np.array(list1) 
    return np.unique(x)

def PL_Resolve(ci, cj):
    new_clause = merge(ci, cj) # merge pair of clauses Ci, Cj in clauses 
    empty_clause = False # check if clause is empty or not
    for x in ci:
        for y in cj:
            # example if our clause is: ['-B', 'C', 'C']
            # we'll remove a character 'C' in list
            # because if first C = second C = true/false
            # first C ^ second C or first C v second C also has result true/false
            if x == y: new_clause.remove(unique(x)) 
            # else if list is not an empty clause 
            # example if our clause is: ['-A', 'A', '-B']
            # we'll remove both -A and A
            # because -A v A = True -> -B v True -> it's pointless
            # so we just keep -B and remove both -A and A
            elif isPointless(x, y) and empty_clause == False:
                new_clause.remove(unique(x)) # remove -A
                new_clause.remove(unique(y)) # remove A
                empty_clause = True
            # else if clause is empty, retrun empty_clause = True
            elif Empty(new_clause): empty_clause = True
    return new_clause

def main():
    # write to file test case 1
    num_clause_query_alpha, list1, num_clause_kb, list2 = readFile("../INPUT/input1.txt")
    with open("../OUTPUT/Output1.txt", 'w') as f:
        for i in range(len(list1)): PL_Resolution(list2, list1[i], f)
    
    # write to file test case 2
    _num_clause_query_alpha, _list1, _num_clause_kb, _list2 = readFile("../INPUT/input2.txt")
    with open("../OUTPUT/Output2.txt", 'w') as _f:
        for i in range(len(_list1)): PL_Resolution(_list2, _list1[i], _f)
    
    # write to file test case 3
    __num_clause_query_alpha, __list1, __num_clause_kb, __list2 = readFile("../INPUT/input3.txt")
    with open("../OUTPUT/Output3.txt", 'w') as __f:
        for i in range(len(__list1)): PL_Resolution(__list2, __list1[i], __f)
    
    # write to file test case 4
    ___num_clause_query_alpha, ___list1, ___num_clause_kb, ___list2 = readFile("../INPUT/input4.txt")
    with open("../OUTPUT/Output4.txt", 'w') as ___f:
        for i in range(len(___list1)): PL_Resolution(___list2, ___list1[i], ___f)
        
    # write to file test case 5
    ____num_clause_query_alpha, ____list1, ____num_clause_kb, ____list2 = readFile("../INPUT/input5.txt")
    with open("../OUTPUT/Output5.txt", 'w') as ____f:
        for i in range(len(____list1)): PL_Resolution(____list2, ____list1[i], ____f)
        
    #_____num_clause_query_alpha, _____list1, _____num_clause_kb, _____list2 = readFile("../INPUT/input_test.txt")
    #with open("../OUTPUT/output_test.txt", 'w') as _____f:
        #for i in range(len(_____list1)): PL_Resolution(_____list2, _____list1[i], _____f)
            
if __name__ == '__main__':
    main()