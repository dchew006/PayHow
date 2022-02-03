#libraries
import numpy as np
import pandas as pd

#user input
numofpeople = int(input('enter number of people involved: '))
friends = []
paid = []

for i in range(numofpeople):
    name = str(input("enter name of friend: "))
    amt = float(input('enter the amount {} paid: '.format(name)))
        
    friends.append(name)
    paid.append(amt)

spent = np.array(paid).reshape(-1,1)
per_person = spent / len(paid)
table = (per_person.T - per_person).clip(min=0)

#make a df
cols = [f"to {person}" for person in friends]
index = [f"{person} owes" for person in friends]
df = pd.DataFrame(data=table, columns=cols, index=index).round(2)

#turning df to array
myarray = df.to_numpy()

#LEAST CF ALGO

#people involved
n = numofpeople

#return index of person who owes the most
def getmin(arg):
    
    minInd = 0
    for i in range(1, n):
        if (arg[i] < arg[minInd]):
            minInd = i
    return minInd
# returns the index of person who owes the least
def getmax(arg):
    
    maxInd = 0
    for i in range(1, n):
        if (arg[i] > arg[maxInd]):
            maxInd = i
            
    return maxInd

#return min of the two values
def minof2(x,y):
    if x < y:
        return x
    else:
        return y
    
#LEAST CF ALGORITHM
def mincashflowrec(amount):
    
    #Maxcr is the person with the least debt
    #maxDr is the person who owes the most
    maxCr = getmax(amount)
    MaxDr = getmin(amount)
    
    #if balance, amounts sesddttled.
    if (amount[maxCr] < 0.00001 and amount[MaxDr] < 0.00001):
        return 0
    
    #finding who to settled first
    min = minof2(-amount[MaxDr], amount[maxCr]) #the highest about of debt/credit to be settled first
    amount[maxCr] = amount[maxCr] - min
    amount[MaxDr] = amount[MaxDr] + min
    
    Payer = friends[MaxDr] #person with most debt
    Payee = friends[maxCr] #person with least debt to be paid first
    
    #if min != 0:
        
    print(Payer, "pays", min.round(2),"to", Payee )
    #else:
    #    exit
    #repeats within array until either maxdr or maxcr becomes 0
    
    mincashflowrec(amount)

#input[a][b] where a needs to pay b
def cashflow(input):
    amount = [0 for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            amount[i] += (input[j][i] - input[i][j])
    
    mincashflowrec(amount)


input = myarray

cashflow(input)
#where the 3 lists corresp to person 0 , 1 , 2
# and value 0 = person 0, value 1 = person 1 owed etc
#algo assigns least possible transactions to balance

print(df)