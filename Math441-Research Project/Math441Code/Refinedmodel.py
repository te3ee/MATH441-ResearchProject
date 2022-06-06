'refined model'
'requires Pandas and Gurobi to use'
from pandas import *
from gurobipy import *

# Budget constraint
salary_cap = 80000000

# Player constraint 
player_count = 12

# Initializing variables for easy testing 
atlantic_div = 2
central_div = 2
northwest_div = 2
southeast_div = 2
pacific_div = 2
southwest_div = 2

# Variables for position constraints
pg = 3
sg = 3  
sf = 2
pf = 2
cen = 2

# The penalty coeifficient for our refined modal(not sure yet)
coeifficient_alpha = 6       

'gathers excel sheet data and throws into one big dictionary'
xls = ExcelFile(r'/Users/Terence/Desktop/Math441Code/Copy of Math 441_ Data.xlsx')
data_frame = xls.parse(xls.sheet_names[0])
dictionary = data_frame.to_dict()

'separates the one big dictionary up'
xIndex = dictionary.get('xIndex')
player = dictionary.get('Player')
position = dictionary.get('Position ')
region = dictionary.get('Region')
points = dictionary.get('Estimated points')
salary = dictionary.get('Cost')

'initializing empty sets for regions'
atlantic = []
central = []
southeast = []
northwest = []
pacific = []
southwest = []

'splits players into sets by region'
for i in range(len(region)):
    if ('Atlantic' == region.get(i)):
        atlantic.append(xIndex.get(i))
    elif ('Central' == region.get(i)):
        central.append(xIndex.get(i))
    elif ('SouthEast' == region.get(i)):
        southeast.append(xIndex.get(i))
    elif ('NorthWest' == region.get(i)):
        northwest.append(xIndex.get(i))
    elif ('Pacific' == region.get(i)):
        pacific.append(xIndex.get(i))
    elif ('SouthWest' == region.get(i)):
        southwest.append(xIndex.get(i))
    else:
        print('A player is not in a region')

'initializing empty sets for positions'
point_guards = []
shooting_guards = []
small_forwards = []
power_forwards  = []
centers = []

'splits players into sets by position'
for i in range(len(region)):
    if ('PG' in position.get(i)):
        point_guards.append(xIndex.get(i))
    if ('SG' in position.get(i)):
        shooting_guards.append(xIndex.get(i))
    if ('SF' in position.get(i)):
        small_forwards.append(xIndex.get(i))
    if ('PF' in position.get(i)):
        power_forwards.append(xIndex.get(i))
    if ('C' in position.get(i)):
        centers.append(xIndex.get(i))

m = Model('FantasyTeamBuilding')

'add variables'
variable_list = {}
for j in range(len(xIndex)):
    variable_list[j] = m.addVar(name=player.get(j), vtype=GRB.BINARY)

atlantic_list = {}
central_list = {}
southeast_list = {}
northwest_list = {}
pacific_list = {}
southwest_list = {}
point_guards_list = {}
shooting_guards_list = {}
small_forwards_list = {}
power_forwards_list  = {}
centers_list = {}

m.update()
'sort variables into appropriate sets for divison'
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in atlantic):
        atlantic_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in central):
        central_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in southeast):
        southeast_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in northwest):
        northwest_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in pacific):
        pacific_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in southwest):
        southwest_list[count] = variable_list[i]
        count=count+1
        
'sort variables into appropriate sets for position'
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in point_guards):
        point_guards_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in shooting_guards):
        shooting_guards_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in small_forwards):
        small_forwards_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in power_forwards):
        power_forwards_list[count] = variable_list[i]
        count=count+1
count=0
for i in range(len(xIndex)):
    if (xIndex.get(i) in centers):
        centers_list[count] = variable_list[i]
        count=count+1        

# Quadratic penalty
if (sum(point_guards_list[i] for i in range(len(point_guards))) > pg):
   penalty_pg = (sum(point_guards_list[i] for i in range(len(point_guards))) - pg)**2
else: penalty_pg = 0

if (sum(shooting_guards_list[i] for i in range(len(shooting_guards))) > sg):
   penalty_sg = (sum(shooting_guards_list[i] for i in range(len(shooting_guards))) - sg)**2
else: penalty_sg = 0

if (sum(small_forwards_list[i] for i in range(len(small_forwards))) > sf):
   penalty_sf = (sum(small_forwards_list[i] for i in range(len(small_forwards))) - sf)**2
else: penalty_sf = 0

if (sum(power_fowards_list[i] for i in range(len(power_forwards))) > pf):
   penalty_pf = (sum(power_forwards_list[i] for i in range(len(power_forwards))) - pf)**2
else: penalty_pf = 0

if (sum(centers_list[i] for i in range(len(centers))) > cen):
   penalty_cen = (sum(centers_list[i] for i in range(len(centers))) - cen)**2
else: penalty_cen = 0

penalty = coeifficient_alpha * (penalty_pg + penalty_sg + penalty_pf + penalty_sf + penalty_cen)



'objective function'
m.setObjective((sum(variable_list[i] * points.get(i) for i in range(len(points)))- penalty),
        GRB.MAXIMIZE)

'salary constraint'

m.addConstr(
        (sum(variable_list[i] * salary.get(i) for i in range(len(salary)))
        <= salary_cap))

'number of players constraint'
m.addConstr(
        sum(variable_list[i] for i in range(len(xIndex)))
        == player_count)

'divison constraints'
m.addConstr(
        (sum(atlantic_list[i] for i in range(len(atlantic)))
        == atlantic_div))
m.addConstr(
        (sum(central_list[i] for i in range(len(central)))
        == central_div))
m.addConstr(
        (sum(southeast_list[i] for i in range(len(southeast)))
        == southeast_div))
m.addConstr(
        (sum(northwest_list[i] for i in range(len(northwest)))
        == northwest_div))
m.addConstr(
        (sum(pacific_list[i] for i in range(len(pacific)))
        == pacific_div))
m.addConstr(
        (sum(southwest_list[i] for i in range(len(southwest)))
        == southwest_div))

'position constraints'
# change other constraints of other positions to less than 
# inorder to keep the player count constraint valid
m.addConstr(
        (sum(point_guards_list[i] for i in range(len(point_guards)))
        == pg))
m.addConstr(
        (sum(shooting_guards_list[i] for i in range(len(shooting_guards)))
        <= sg))
m.addConstr(
        (sum(small_forwards_list[i] for i in range(len(small_forwards)))
        <= sf))
m.addConstr(
        (sum(power_forwards_list[i] for i in range(len(power_forwards)))
        <= pf))
m.addConstr(
        (sum(centers_list[i] for i in range(len(centers)))
        <= cen))


'writes lp file'
m.update()
m.write(r'/Users/Terence/Downloads/file.lp')

'reads lp file and solves IP'
n = read(r'/Users/Terence/Downloads/file.lp')
n.optimize()
print('Total points of team at optimal:')
print(n.objVal)

# prints players that selected in team
print(n.printAttr("X"))

