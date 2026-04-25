#this prompts the user for the query and converts it into arguments for phi
import re #for parsing numbers

def get_input_query():
    # attributes
    attribute_str = input("SELECT ATTRIBUTE(S):\n").split(',')
    for i in range(len(attribute_str)):
        attribute_str[i] = attribute_str[i].strip()

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
    groupingAtt_str = input("GROUPING ATTRIBUTES(V):\n").split(',')
    for i in range(len(groupingAtt_str)):
        groupingAtt_str[i] = groupingAtt_str[i].strip()


    fvect_str = input("F-VECT([F]):\n").split(',')
    for i in range(len(groupingAtt_str)):
        fvect_str[i] = fvect_str[i].strip()

    condvect_str = []
    print("SELECT CONDITION-VECT([σ]):")
    for i in range(groupingNum):
        condvect_str += [input(str(i+1) + ". ").strip()]

    having_str = input("HAVING_CONDITION(G):\n").strip()

    phi = [attribute_str,groupingNum,groupingAtt_str,fvect_str,condvect_str,having_str]
    print(str(phi))

get_input_query()