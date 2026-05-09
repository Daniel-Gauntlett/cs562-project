#this prompts the user for the query and converts it into arguments for phi
import re #for parsing numbers

def prefixed_with_number(s):
    if s[0] in ['0','1','2','3','4','5','6','7','8','9']:
        s = "q"+s
    return s

def add_equals(s):
    for i in range(len(s)):
        if s[i] == "=" or s[i] == ">" or s[i] == "<" or s[i] :
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

    print(attribute_str)

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


    fvect_str = input("F-VECT([F]):\n")
    fvect_str = process_stringlist(fvect_str)

    condvect_str = []
    print("SELECT CONDITION-VECT([σ]):")
    for i in range(groupingNum):
        condvect_str += [add_equals(prefixed_with_number( input(str(i+1) + ". ").strip()))]

    having_str = input("HAVING_CONDITION(G):\n").strip()

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

    # split the file into each word
    str_list = file_contents.split('\n')
    aggregate = []
    for i in range(0,len(str_list)):
        aggregate += (str_list[i].split(' '))
    
    #remove extra characters
    for i in range(0,len(aggregate)):
        replacable_chars = [',',';',' ']
        for char in replacable_chars:
            aggregate[i] = aggregate[i].replace(char,'')
    
    # check for select at start
    if aggregate[0] != 'select':
        print("select not found")
        return 
    
    #generate lists from the contents of the file

    select_list = []
    from_list = []
    group_by_list = []
    such_that_list = []
    having_list = []
    parsing_mode = 'select'
    groupby_satisfied = False
    suchthat_satisfied = False
    for i in range(1,len(aggregate)):
        #parse all the select items
        if parsing_mode == 'select':
            if aggregate[i] == 'from':
                parsing_mode = 'from'
                continue

            select_list.append(aggregate[i])

        #parse all the from items
        if parsing_mode == 'from':
            if aggregate[i] == 'group' and aggregate[i+1] == 'by':
                parsing_mode = 'groupby'
                continue
            
            from_list.append(aggregate[i])

        #parse all the groupby items
        if parsing_mode == 'groupby':
            # accounts for the by in group by
            if aggregate[i] == 'by' and not groupby_satisfied:
                groupby_satisfied = True
                continue

            if aggregate[i] == 'such' and aggregate[i+1] == 'that':
                parsing_mode = 'suchthat'
                continue
            
            group_by_list.append(aggregate[i])

        #parse all suchthat items
        if parsing_mode == 'suchthat':
            # account for the that in such that
            if aggregate[i] == 'that' and not suchthat_satisfied:
                suchthat_satisfied = True
                continue

            if aggregate[i] == 'having':
                parsing_mode = 'having'
                continue

            such_that_list.append(aggregate[i])

        #parse all having items
        if parsing_mode == 'having':
            if aggregate[i] == 'having':
                parsing_mode = 'having'
                continue
            
            having_list.append(aggregate[i])

        
    print(group_by_list)
    print(len(group_by_list))