#this prompts the user for the query and converts it into arguments for phi
import re #for parsing numbers

def prefixed_with_number(s):
    if s[0] in ['0','1','2','3','4','5','6','7','8','9']:
        s = "q"+s
    return s

def add_equals(s):
    for i in range(len(s)):
        if s[i] == "=" or s[i] == ">" or s[i] == "<" or s[i] == '!':
            if i >= 1:
                if s[i-1] != " ":
                    s = s[:(i-1)] + " " + s[(i-1):]
            if i < len(s):
                if s[i+1] != " " and s[i] == "=":
                    return s[:i] + "= " + s[i:]
                elif s[i+1] != " " and s[i+1] == "=":
                    return s[:i] + " " + s[i:]
                else:
                    return s[:i] + "=" + s[i:]
    return s

def process_stringlist(s):
    s = s.split(',')
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
        parse = re.findall(r'\d+',groupingNum_str)
        if len(parse) > 0 and len(parse) < 2:
            groupingNum = int(parse[0])
            if groupingNum >= 0:
                break
        print("please supply a single integer")

    # grouping attributes
    groupingAtt_str = input("GROUPING ATTRIBUTES(V):\n")
    groupingAtt_str = process_stringlist(groupingAtt_str)

    #fvect conditions
    fvect_str = input("F-VECT([F]):\n")
    fvect_str = process_stringlist(fvect_str)

    condvect_str = []
    print("SELECT CONDITION-VECT([σ]):")
    for i in range(groupingNum):
        condvect_str += [add_equals(prefixed_with_number( input(str(i+1) + ". ").strip()))]

    having_str = ""
    having_str = fix_having_prefixes( input("HAVING_CONDITION(G):\n").strip() )

    phi = [attribute_str,groupingNum,groupingAtt_str,fvect_str,condvect_str,having_str]
    
    return phi



def get_test_input_query():
    query = [['cust', 'q1_sum_quant', 'q2_sum_quant', 'q3_sum_quant'], 3, ['cust'], ['q1_sum_quant', ' q1_avg_quant', ' q2_sum_quant', ' q3_sum_quant', ' q3_avg_quant'], ["month = 1", "month = 2", "month = 3"], 
    'q1_sum_quant > 2 * q2_sum_quant or q1_avg_quant > q3_avg_quant']

    for i in range(len(query[4])):
        query[4][i] = add_equals(query[4][i])

    return query

def read_file_query(file_path):
    file = open(file_path)
    file_contents = file.read()

    #split each into input
    file_query = file_contents.split('\n')

    attribute_str = process_stringlist(file_query[0])

    groupingNum = int(file_query[1])

    groupingAtt_str = process_stringlist(file_query[2])

    fvect_str = process_stringlist(file_query[3])

    i=4
    condvect_str = []
    while True:
        if (len(file_query[4]) == 0):
            i+=1
            break
        if file_query[i][1] == '.' and file_query[i][0].isnumeric():
            condvect_str = file_query[i][2:(len(file_query[i]))]
            i+=1
        else:
            break
    
    having_str = ""
    if i < len(file_query):
        if len(file_query[i].strip()) > 0:
            having_str = fix_having_prefixes(file_query[i].strip())

    retval = [attribute_str,groupingNum,groupingAtt_str,fvect_str,condvect_str,having_str]

    return retval


#prevents number_prefixed variables in having condition
def fix_having_prefixes(str):
    for i in range(0,len(str)-1):
        if str[i].isnumeric() and str[i+1] != ' ' and not str[i+1].isnumeric():
            if i == 0:
                str = 'q' + str
            else:
                if str[i-1] == ' ':
                    str = str[:i] + 'q' + str[i:]
    return str