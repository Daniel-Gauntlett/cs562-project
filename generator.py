import subprocess, parser

# Stuff up here is being put in python format for generation

def editcondition(precond, cond, attrs):
    if len(cond) == 0:
        return "True"
    havingcond = "" 
    havinglist = cond.split(" ")
    for i in range(len(havinglist)):
        if havinglist[i] in attrs:
            havingcond = havingcond + f"{precond}[\"{havinglist[i]}\"] "
        else:
            havingcond = havingcond + havinglist[i] + " "
    havingcond = havingcond.strip()
    return havingcond


SCHEMA = ["cust", "prod", "day", "month", "year", "state", "quant", "date"]

def getcol(agg):
    part = agg.split("_")[-1]
    return part

def main(phi):
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """
    for x in range(len(phi)):
        if isinstance(phi[x], list):
            for y in range(len(phi[x])):
                phi[x][y] = phi[x][y].strip()
    S = phi[0]
    n = phi[1]
    V = phi[2]
    FVECT = phi[3]
    PRED_LIST = phi[4]
    HAVING = phi[5]
    if HAVING:
        havingcond = editcondition("mf_struct[i]", HAVING, V + FVECT)
    else:
        havingcond = "True"

    aggfuncs = ""
    fvects = {}
    avg_pairs = []
    added_vects = []
    for i in range(len(FVECT)):
        if "sum" in FVECT[i]:
            aggfuncs = aggfuncs + f"\"{FVECT[i]}\": 0,\n        "
        elif "count" in FVECT[i]:
            aggfuncs = aggfuncs + f"\"{FVECT[i]}\": 0,\n        "
        elif "avg" in FVECT[i]:
            aggfuncs = aggfuncs + f"\"{FVECT[i]}\": 0,\n        "
            splitfunc = FVECT[i].split("_")
            countfunc = splitfunc[0] + "_" + "count" + "_" + splitfunc[2]
            if countfunc not in FVECT:
                added_vects.append(countfunc)
            avg_pairs.append((FVECT[i], countfunc))
        elif "max" in FVECT[i]:
            aggfuncs = aggfuncs + f"\"{FVECT[i]}\": float(\"-inf\"),\n        "
        elif "min" in FVECT[i]:
            aggfuncs = aggfuncs + f"\"{FVECT[i]}\": float(\"inf\"),\n        "
        num = FVECT[i].split("_")[0]
        if num not in fvects:
            fvects[num] = []
        fvects[num].append(FVECT[i])
    for vect in added_vects:
        aggfuncs = aggfuncs + f"\"{vect}\": 0,\n        "
    FVECT = FVECT + added_vects
    groupingattrs = ""
    for i in range(len(V)):
        groupingattrs = groupingattrs + f"\"{V[i]}\": \"\",\n        "
    
    groupadd = ""
    for i in range(len(V)):
        groupadd = groupadd + f"newrow[\"{V[i]}\"] = cur_row[\"{V[i]}\"]\n    "
    
    outputlist = ""
    outputstring = ""
    for i in range(len(S)):
        outputlist = outputlist + "mf_struct[i][\"" + S[i] + "\"], "
        outputstring = outputstring + "%s\t"
    
    lookupcondition = []
    for i in range(len(V)):
        lookupcondition.append(f"mf_struct[i][\"{V[i]}\"] == cur_row[\"{V[i]}\"]")
    lookupcondition = " and ".join(lookupcondition)
    
    processgroupvars = ""
    for i in range(n):
        action = ""
        if "q" + str(i+1) in fvects:
            for j in fvects["q" + str(i+1)]:
                if "sum" in j:
                    action = action + f"mf_struct[pos][\"{j}\"] += row[\"{getcol(j)}\"]\n                "
                elif "avg" in j:
                    action = action + f"mf_struct[pos][\"{j}\"] += row[\"{getcol(j)}\"]\n                "
                elif "count" in j:
                    action = action + f"mf_struct[pos][\"{j}\"] += 1\n                "
                elif "max" in j:
                    action = action + f"""
                if row[\"{getcol(j)}\"] > mf_struct[pos][\"{j}\"]:
                    mf_struct[pos][\"{j}\"] = row[\"{getcol(j)}\"]
                """
                elif "min" in j:
                    action = action + f"""
                if row[\"{getcol(j)}\"] < mf_struct[pos][\"{j}\"]:
                    mf_struct[pos][\"{j}\"] = row[\"{getcol(j)}\"]
                """
        if action == "":
            continue
        processgroupvars = processgroupvars + f"""
    for row in table:
        if {editcondition("row", PRED_LIST[i], SCHEMA)}:
            pos = lookup(row)
            if pos != -1:
                {action}
    """
    if avg_pairs != []:
         processgroupvars = processgroupvars + f"""
    for i in range(NUM_OF_ENTRIES):
        """
    for avg_pair in avg_pairs:
        processgroupvars = processgroupvars + f"""
        if mf_struct[i][\"{avg_pair[1]}\"] != 0:
            mf_struct[i][\"{avg_pair[0]}\"] /= mf_struct[i][\"{avg_pair[1]}\"]
    """

    methods = f"""
mf_struct = []
NUM_OF_ENTRIES = 0
def get_new_row():
    # max should be initialized as -1 instead of 0
    return {{
        {groupingattrs}
        {aggfuncs}
    }}

def lookup(cur_row):
    for i in range(NUM_OF_ENTRIES):
        if ({lookupcondition}):
            return i
    return -1

def add(cur_row, mf_struct):
    global NUM_OF_ENTRIES
    newrow = get_new_row()
    {groupadd}
    mf_struct.append(newrow)
    NUM_OF_ENTRIES = NUM_OF_ENTRIES + 1

def output():
    print(". . . . .\\n"); # header of the output (from operand S)
    for i in range(NUM_OF_ENTRIES):
        if {havingcond}:
            print("{outputstring}\\n" % ({outputlist}))
"""
    body = f"""
    
    # TABLE SCAN 1
    table = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    table = [dict(zip(columns, row)) for row in table]
    for row in table:
        pos = lookup(row)
        if pos == -1:
            add(row, mf_struct)
    
    {processgroupvars}        

    output()

"""
    # Note: The f allows formatting with variables.
    #       Also, note the indentation is preserved.
    tmp = f"""
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv

# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py

{methods}

def query():
    load_dotenv()

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    dbname = os.getenv('DBNAME')

    conn = psycopg2.connect("dbname="+dbname+" user="+user+" password="+password,
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    
    _global = []
    {body}
    cur.close()
    conn.close()
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    """

    # Write the generated code to a file
    with open("_generated.py", "w") as f:
        f.write(tmp)
    # Execute the generated code
    subprocess.run(["python", "_generated.py"])


if "__main__" == __name__:
    args = sys.argv[1:]
    phi = parser.read_file_query("test_query2.txt")
    main(phi)    
