#this prompts the user for the query and converts it into arguments for phi
import re #for parsing numbers

def prefixed_with_number(s):
    if [0,1,2,3,4,5,6,7,8,9].contains( s.char_at(0) ):
        s = "q"+s
    return s

def add_equals(s):
    for i in range(len(s)):
        if s[i] == "=":
            return s[:i] + "=" + s[i:]
    return s

def process_stringlist(s):
    s.split(',')
    for i in range(len(s)):
        s[i] = s[i].strip()
        s[i] = prefixed_with_number(s[i])
    return s

def get_input_query():
    # attributes
    attribute_str = input("SELECT ATTRIBUTE(S):\n")
    attribute_str = process_stringlist(attribute_str)

    #loop for input validation
    groupingNum = 0
    while True:
        groupingNum_str = input("NUMBER OF GROUPING VARIABLES(n):\n")
        parse = re.findall('\d+',groupingNum_str)
        if len(parse) > 0 and len(parse) < 2:
            groupingNum = int(parse[0])
            if groupingNum >= 0:
                break
        print("please supply a single integer")

    # grouping attributes
    groupingAtt_str = input("GROUPING ATTRIBUTES(V):\n")
    groupingAtt_str = process_stringlist(groupingAtt_str)


    fvect_str = input("F-VECT([F]):\n").split(',')
    groupingAtt_str = process_stringlist(fvect_str)

    condvect_str = []
    print("SELECT CONDITION-VECT([σ]):")
    for i in range(groupingNum):
        condvect_str += [add_equals(prefixed_with_number( input(str(i+1) + ". ").strip()))]

    having_str = input("HAVING_CONDITION(G):\n").strip()

    phi = [attribute_str,groupingNum,groupingAtt_str,fvect_str,condvect_str,having_str]
    
    return phi

def get_test_input_query():
    query = [['cust', 'q1_sum_quant', 'q2_sum_quant', 'q3_sum_quant'], 3, ['cust'], ['q1_sum_quant', ' q1_avg_quant', ' q2_sum_quant', ' q3_sum_quant', ' q3_avg_quant'], ["state='NY'", "state='NJ'", "state='CT'"], 
    'q1_sum_quant > 2 * q2_sum_quant or q1_avg_quant > q3_avg_quant']

    for i in range(len(query[4])):
        query[4][i] = add_equals(query[4][i])

    return query