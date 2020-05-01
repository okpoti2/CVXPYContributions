
import cvxpy as cp
import sys
import numpy as np

problemName = 'instance/64-4-1'
nodeFile = problemName+'.nod'
arcFile = problemName+'.arc'
mutFile = problemName+'.mut'
supFile = problemName+'.sup'
instanceInfo = [] # [commodity, nodes, arcs, cap_arcs]
numNodes = 0
numCommodity = 0
numArcs = 0
numCapacitatedArcs = 0
bigM = 99999999

#Read the node file
nodeFileData = open(nodeFile, "r")

for eachLine in nodeFileData:
    instanceInfo.append(int(eachLine))
numCommodity = instanceInfo[0]
numNodes = instanceInfo[1]
numArcs = instanceInfo[2]
nodeFileData.close()

#Read mutual capacity pointer file
mutualCapacityPointer = {}
mcpFileData = open(mutFile, "r")

for eachLine in mcpFileData:
    data = eachLine.split("	")
    mutualCapacityPointer[int(data[0])] = int(data[1])

mcpFileData.close()

#Read arc file
uniqueArcs = {}
arcCapacity = {}
mutualCapacity = {}
cost = {}
temp_arc = [0]*numCommodity
temp_cost = [0]*numCommodity
arcFileData = open(arcFile, "r")

for eachLine in arcFileData:
    data = eachLine.split("	")
    uniqueArcs[int(data[0])] = [int(data[1]),int(data[2])]
    mutualCapacity[int(data[0])] = int(data[6])
    if temp_arc[int(data[3])-1]==0:
        temp_arc[int(data[3])-1] = [0]*numArcs
        temp_arc[int(data[3])-1][int(data[0])-1]=int(data[5])
    else:
        temp_arc[int(data[3])-1][int(data[0])-1]=int(data[5])
    if temp_cost[int(data[3])-1]==0:
        temp_cost[int(data[3])-1] = [bigM]*numArcs
        temp_cost[int(data[3])-1][int(data[0])-1] = float(data[4])
    else:
        temp_cost[int(data[3])-1][int(data[0])-1] = float(data[4])
    

for i in range(numCommodity):
    arcCapacity[i+1] = temp_arc[i]    
    cost[i+1] = temp_cost[i] 
    
arcFileData.close()


#Read sup file
supplyDemand = {}
temp_supDem = [0]*numCommodity
supFileData = open(supFile, "r")


for eachLine in supFileData:
    data = eachLine.split("	")
    if temp_supDem[int(data[1])-1]==0:
        temp_supDem[int(data[1])-1] = [0]*numNodes
        temp_supDem[int(data[1])-1][int(data[0])-1]=int(data[2])
    else:
        temp_supDem[int(data[1])-1][int(data[0])-1]=int(data[2])

for i in range(numCommodity):
    supplyDemand[i+1] = temp_supDem[i]  
    
supFileData.close()


#---------------------------Solve the math model------------------------------
#
C = [(a,k) for a in uniqueArcs.keys() for k in range(numCommodity)] #decision variable indexer
X_key = {}
my_ind = 0
for (a,k) in C:
    X_key[a,k] = my_ind
    my_ind+=1
X = cp.Variable(shape=len(C), nonneg=True, name="X") 

allConstraints = []
#constraint 1
for i in range(numNodes):
    for k in range(numCommodity):
        sumIn = 0
        sumOut = 0
        for akey,value in uniqueArcs.items():
            if value[0]==(i+1):
                sumIn +=X[X_key[akey,k]]
            elif value[1]==(i+1):
                sumOut +=X[X_key[akey,k]]
        const1=sumIn-sumOut==supplyDemand[k+1][i]
        allConstraints.append(const1)
 

#constraint 2
for (a,k) in C:
    maxVal = bigM#sys.float_info.max
    if arcCapacity[k+1][a-1]==-1:
        const2=X[X_key[a,k]]<=maxVal
        allConstraints.append(const2)
    else:
        const2=X[X_key[a,k]]<=arcCapacity[k+1][a-1]
        allConstraints.append(const2)
        
#constraint 3
for a in uniqueArcs.keys():
    if mutualCapacity[a]!=0:
        totalVars = [X[X_key[a,k]] for k in range(numCommodity)]
        lhs = cp.sum(totalVars)
        const3=lhs<=mutualCapacityPointer[mutualCapacity[a]]
        allConstraints.append(const3)

actualCost = np.asarray([cost[k+1][a-1] for (a,k) in C])
objExpr = cp.sum(actualCost@X) #objective function
objFunc = cp.Minimize(objExpr)
prob = cp.Problem(objFunc, allConstraints)
prob.solve(verbose=True)

print("MMCF objective function value is ",prob.value)




