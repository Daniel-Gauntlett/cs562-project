import random

cust_table = ['Mary','John','Stacy','Destiny','Matt','Trace']
prod_table = ['ham','tomato','soup','milk','egg','bread']
state_table = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA","ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO","MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK","OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA","WI","WV", "WY"]

print("INSERT INTO sales (cust,prod,quant,state,day,month,year,date)\nVALUES")

n=100
for i in range(0,n):
    end = ""
    cust = cust_table[random.randint(0, len(cust_table)-1)]
    prod = prod_table[random.randint(0,len(prod_table)-1)]
    state = state_table[random.randint(0,len(state_table)-1 )]
    quant = random.randint(1,20)
    day = random.randint(1,28)
    month = random.randint(1,12)
    year = random.randint(1990,2026)
    date = "\'" + str(year) + "-" + str(month) + "-" + str(day) + "\'"

    if i == n-1:
        end = ";"
    else:
        end = ","

    print("  (\'" + cust + "\', \'" + prod + "\', " + str(quant) + ", \'" + state + "\', " + str(day) + ", " + str(month) + ", " + str(year) + ", " + date + ")" + end)