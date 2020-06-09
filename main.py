import turtle, random, time, math, itertools
mywindow = turtle.Screen()
turtle.setup(800, 800)
mywindow.title('Travelling Salesman Problem')

#TURTLES
w = turtle.Turtle() #site stamper
w.hideturtle()
w.penup()
w.shape('circle')
w.turtlesize(0.2)
w.speed(0)

w1 = turtle.Turtle() #path drawer
w1.hideturtle()
w1.penup()
w1.shape('circle')
w1.turtlesize(0.2)
w1.speed(0)

w2 = turtle.Turtle()    #temp
w2.penup()
w2.speed(0)
w2.hideturtle()
w2.goto(-170, 330)

w3 = turtle.Turtle()    #gain
w3.penup()
w3.speed(0)
w3.hideturtle()
w3.goto(65, 330)

w4 = turtle.Turtle()    #current dist
w4.penup()
w4.speed(0)
w4.hideturtle()
w4.goto(230, 330)

w5 = turtle.Turtle()    #title
w5.penup()
w5.speed(0)
w5.hideturtle()
w5.goto(0, 350)

w6 = turtle.Turtle()    #swaps
w6.penup()
w6.speed(0)
w6.hideturtle()
w6.goto(-330, 330)

w7 = turtle.Turtle()    #time
w7.penup()
w7.speed(0)
w7.hideturtle()
w7.goto(-100, -350)

w8 = turtle.Turtle()    #best dist
w8.penup()
w8.speed(0)
w8.hideturtle()
w8.goto(65, -350)

w9 = turtle.Turtle()    #middle upper
w9.penup()
w9.speed(0)
w9.hideturtle()
w9.goto(0, 330)

#FUNCTIONS
def generateSites(n):
   sites = []
   home = [random.randint(-300, 300), random.randint(-300, 300)]
   sites.append(home)
   for i in range(0, n - 1, 1):
       while True:
           x = random.randint(-300, 300)
           y = random.randint(-300, 300)
           if [x, y] not in sites:
               sites.append([x, y])
               break
   return sites

def drawSites(sites):
   w.clear()
   w.penup()
   for i in range(0, len(sites), 1):
       if i == 0 or i == len(sites) - 1:
           w.goto(sites[i][0], sites[i][1])
           w.turtlesize(0.5)
           w.stamp()
           w.turtlesize(0.2)
       else:
           w.goto(sites[i][0], sites[i][1])
           w.stamp()

def drawPath(path):
   w1.clear()
   w1.pendown()
   for i in range(0, len(path), 1):
       if i == 0:
           w1.penup()
           w1.goto(path[i][0], path[i][1])
           w1.pendown()
       else:
           w1.goto(path[i][0], path[i][1])
       #time.sleep(1)

def randomize(path):
   random.shuffle(path)
   return path

def calcDist(site1, site2):
   dist = ((site1[0] - site2[0]) ** 2 + (site1[1] - site2[1]) ** 2) ** 0.5
   return dist

def pathDist(tour):
   total = 0
   for i in range(0, len(tour) - 1, 1):
       total += calcDist(tour[i], tour[i + 1])
   return total

def twoOpt(tour, i, j):
   newPath = []
   for k in range(0, i, 1):
       newPath.append(tour[k])
   newPath.append(tour[j])
   for l in range(j - 1, i, -1):
       newPath.append(tour[l])
   newPath.append(tour[i])
   for m in range(j + 1, len(tour), 1):
       newPath.append(tour[m])
   return newPath

def probability(temp, newDist, oldDist):
   if newDist > oldDist:
       return math.exp((oldDist - newDist) / temp)
   else:
       return 1

#MAIN
mywindow.tracer(0, 0)

sites = [[100,75],[20,-150],[-175,10],[-20,220],[-40,120],[40,20],[0,-140], [100, 75]]
#sites = [[100,75],[70,-150],[40,20],[0,-140],[-200,115],[-245,-135],[45,225],[10,-45],[-245,-135], [100, 75]]
home = sites[0]
drawSites(sites)


#BRUTE FORCE

w5.clear()
w5.write('Brute Force', align='center', font=('Arial', 20, 'bold'))
mywindow.update()

possibleSites = sites.copy()
del possibleSites[0]
del possibleSites[-1]
possiblePerm = list(itertools.permutations(sites, len(sites)))

bestDist = 9999999999999
bestPath = 0
for i in range(0, len(possiblePerm), 1):
   path = list(possiblePerm[i])
   path.insert(0, home)
   path.append(home)
   total = pathDist(path)
   if total < bestDist:
       bestDist = total
       bestPath = list(possiblePerm[i])

drawPath(bestPath)
w9.clear()
w9.write('Best Dist: {0:.2f}'.format(bestDist), align='center')
mywindow.update()
time.sleep(5)
w9.clear()

#CREATE RANDOM START PATH FOR GREEDY, 2-OPT, SA
nSites = 100
sites = generateSites(nSites)
home = sites[0]
del sites[0]
randomStart = randomize(sites)
randomStart.insert(0, home)
randomStart.append(home)

#randomStart = [[205, -89], [159, 89], [-143, 204], [-117, -221], [-170, 249], [-57, 124], [255, 4], [-195, -103], [-284, 90], [-187, 219], [-150, 98], [189, 230], [-158, 276], [288, -101], [-248, -297], [3, -70], [-290, -221], [105, -271], [-79, 242], [100, 299], [-227, 71], [95, -186], [-105, 28], [-287, 232], [110, 42], [-185, 71], [-150, -61], [-27, -12], [17, -113], [-31, 220], [62, -37], [229, 96], [-158, -258], [216, -268], [251, -248], [189, 243], [100, -192], [74, -179], [-282, 136], [175, -20], [-40, -62], [-254, 115], [-270, 190], [71, 280], [-244, 281], [-104, 19], [205, 112], [-261, 120], [293, -77], [-209, 250], [195, 63], [22, 54], [235, -185], [133, -221], [236, 227], [-277, 241], [-173, -15], [215, 277], [251, -299], [157, -285], [31, -110], [83, -278], [-171, 31], [-250, -158], [-156, 74], [56, 97], [128, 156], [228, 30], [223, -111], [-99, 108], [-63, 26], [-184, 238], [56, -103], [-63, 194], [-1, -232], [108, 265], [-160, -135], [173, -189], [-133, -23], [-24, -217], [288, 169], [-208, -295], [-176, -211], [1, -50], [-55, -165], [105, 26], [142, -109], [-6, 5], [-267, -219], [186, 298], [-183, 260], [37, 170], [-27, 282], [13, 194], [-93, -26], [181, 95], [116, -158], [-61, -190], [-40, 286], [145, -243], [-185, 152], [-21, -235], [-22, -83], [-215, -63], [156, -136], [-34, -120], [193, 175], [234, 176], [97, -281], [-250, -141], [-210, 197], [-258, 270], [97, -262], [100, 61], [130, -236], [-230, -161], [286, -126], [222, 278], [-238, 259], [-137, 25], [34, -253], [300, 30], [260, -251], [-277, 13], [-246, 198], [-148, -12], [-85, -167], [-114, -168], [-85, -275], [-248, -275], [-210, 36], [130, -263], [-7, -121], [294, 280], [-151, 184], [-151, 131], [161, 27], [157, 211], [121, -196], [197, -61], [-292, -141], [-210, -56], [13, -136], [220, -162], [134, -297], [229, -241], [-27, -260], [113, 116], [-149, 299], [29, -129], [226, -275], [-25, 127], [1, 27], [-258, 21], [43, 171], [-101, -6], [-219, 14], [-47, -235], [-259, -239], [137, 27], [17, -180], [-277, -105], [-291, -274], [-139, 296], [129, -280], [138, 87], [-179, 76], [60, -2], [-21, -141], [29, 122], [-161, -216], [139, -220], [-140, 148], [124, -112], [144, -78], [224, 196], [-164, 3], [-137, 150], [286, 140], [-14, -274], [87, 28], [79, 107], [71, 277], [-149, 217], [-267, -189], [-248, 296], [276, 39], [-229, 21], [-59, 66], [253, 228], [-147, 277], [-201, 100], [52, -224], [-170, 109], [149, -248], [-212, -29], [-279, 193], [-280, 196], [279, 39], [203, 62], [205, -89]]
#randomStart = [[205, -89], [159, 89], [-143, 204], [-117, -221], [-170, 249], [-57, 124], [255, 4], [-195, -103], [-284, 90], [-187, 219], [-150, 98], [189, 230], [-158, 276], [288, -101], [-248, -297], [3, -70], [-290, -221], [105, -271], [-79, 242], [100, 299], [-227, 71], [95, -186], [-105, 28], [-287, 232], [110, 42], [-185, 71], [-150, -61], [-27, -12], [17, -113], [-31, 220], [62, -37], [229, 96], [-158, -258], [216, -268], [251, -248], [189, 243], [100, -192], [74, -179], [-282, 136], [175, -20], [-40, -62], [-254, 115], [-270, 190], [71, 280], [-244, 281], [-104, 19], [205, 112], [-261, 120], [293, -77], [-209, 250], [195, 63], [22, 54], [235, -185], [133, -221], [236, 227], [-277, 241], [-173, -15], [215, 277], [251, -299], [157, -285], [31, -110], [83, -278], [-171, 31], [-250, -158], [-156, 74], [56, 97], [128, 156], [228, 30], [223, -111], [-99, 108], [-63, 26], [-184, 238], [56, -103], [-63, 194], [-1, -232], [108, 265], [-160, -135], [173, -189], [-133, -23], [-24, -217], [288, 169], [-208, -295], [-176, -211], [1, -50], [-55, -165], [105, 26], [142, -109], [-6, 5], [-267, -219], [186, 298], [-183, 260], [37, 170],  [145, -243], [-185, 152], [-21, -235], [-22, -83], [-215, -63], [156, -136], [-34, -120], [193, 175], [234, 176], [97, -281], [-250, -141], [-210, 197], [-258, 270], [97, -262], [100, 61], [130, -236], [-230, -161], [286, -126], [222, 278], [-238, 259], [-137, 25], [34, -253], [300, 30], [260, -251], [-277, 13], [-246, 198], [-148, -12], [-85, -167], [-114, -168], [-85, -275], [-248, -275], [-210, 36], [130, -263], [-7, -121], [294, 280], [-151, 184], [-151, 131], [161, 27], [157, 211], [121, -196], [197, -61], [-27, -260], [113, 116], [-149, 299], [29, -129], [226, -275], [-25, 127], [1, 27], [-258, 21], [43, 171], [-101, -6], [-219, 14], [-47, -235], [-259, -239], [137, 27], [17, -180], [-277, -105], [-291, -274], [-139, 296], [129, -280], [138, 87], [-179, 76], [60, -2], [-21, -141], [29, 122], [-137, 150], [286, 140], [-14, -274], [87, 28], [79, 107], [71, 277], [-149, 217], [-267, -189], [-248, 296], [276, 39], [-229, 21], [-59, 66], [253, 228], [-147, 277], [-201, 100], [52, -224], [-170, 109], [149, -248], [-212, -29], [-279, 193], [-280, 196], [279, 39], [203, 62], [205, -89]]


#GREEDY
w.clear()
w1.clear()
w5.clear()
w5.write('Greedy Search', align='center', font=('Arial', 20, 'bold'))
sites = randomStart.copy()
drawSites(sites)
path = []
home = sites[0]
path.append(home)

del sites[0]
del sites[-1]

for i in range(0, len(sites), 1):
   currentSite = path[len(path) - 1]
   closestDist = 9999999999999999999
   closestIndex = 0
   for j in range(0, len(sites), 1):
       if j != i:
           if calcDist(currentSite, sites[j]) < closestDist:
               closestDist = calcDist(currentSite, sites[j])
               closestIndex = j
   path.append(sites[closestIndex])
   del sites[closestIndex]
path.insert(0, home)
path.append(home)
drawPath(path)
w9.clear()
w9.write('Best Dist: {0:.2f}'.format(pathDist(path)), align='center')
mywindow.update()
time.sleep(5)
w9.clear()


#2-OPT
w5.clear()
w5.write('2-Opt', align='center', font=('Arial', 20, 'bold'))

path = randomStart.copy()
drawSites(path)
drawPath(path)
mywindow.update()

startTime = time.process_time()
mywindow.update()
reduction = True
while reduction == True:
   reduction = False
   for i in range(1, len(path) - 1, 1):    #side 1 that != home
       for j in range(i + 1, len(path) - 1, 1):
           newPath = twoOpt(path, i, j)
           if pathDist(newPath) < pathDist(path):
               path = newPath.copy()
               drawPath(path)
               w9.clear()
               w9.write('Current Dist: {0:.2f}'.format(pathDist(path)), align='center')
               mywindow.update()
               reduction = True
endTime = time.process_time()
diffTime = endTime - startTime
w8.clear()
w8.write('Best Dist: {0:.2f}'.format(pathDist(path)))
w7.clear()
w7.write('Time: {0:.2f}'.format(diffTime))
mywindow.update()
time.sleep(5)
w8.clear()
w7.clear()
w9.clear()



#SIMULATED ANNEALING USING RANDOM 2-OPT
path = randomStart.copy()

drawSites(path)
drawPath(path)
w5.clear()
w5.write('Simulated Annealing', align='center', font=('Arial', 20, 'bold'))
mywindow.update()
temp = 100
startTime = time.process_time()
swaps = 0
while temp > 0.000001:
   reps = 0
   while reps <= 25:
       while True:
           i = random.randint(1, (len(path) - 2))
           j = random.randint(1, (len(path) - 2))
           if i + 2 <= j: #non adj sides
               break
       #i + 2 <= j and
       newPath = twoOpt(path, i, j)

       prob = probability(temp, pathDist(newPath), pathDist(path)) #generates num 0 - 1

       if prob > random.random():
           gain = pathDist(path) - pathDist(newPath)
           path = newPath.copy()
           drawPath(path)
           w6.clear()
           w6.write('Swaps:' + str(swaps))
           w2.clear()
           w2.write('Temperature: {0:.6f}'.format(temp))
           w3.clear()
           w3.write('Gain: {0:.2f}'.format(gain))
           w4.clear()
           w4.write('Current Dist: {0:.2f}'.format(pathDist(path)))
           swaps += 1
           mywindow.update()
       reps += 1

   temp = temp * 0.995

#cleanup
reduction = True
while reduction == True:
   reduction = False
   for i in range(1, len(path) - 1, 1):    #side 1 that != home
       for j in range(i + 1, len(path) - 1, 1):
           newPath = twoOpt(path, i, j)
           if pathDist(newPath) < pathDist(path):
               gain = pathDist(path) - pathDist(newPath)
               path = newPath.copy()
               drawPath(path)
               w6.clear()
               w6.write('Swaps: ' + str(swaps))
               w2.clear()
               w2.write('Temperature: {0:.6f}'.format(temp))
               w3.clear()
               w3.write('Gain: {0:.2f}'.format(gain))
               w4.clear()
               w4.write('Current Dist: {0:.2f}'.format(pathDist(path)))
               swaps += 1
               mywindow.update()
               reduction = True

endTime = time.process_time()
diffTime = endTime - startTime
print(diffTime)
w8.clear()
w8.write('Best Dist: {0:.2f}'.format(pathDist(path)))
w7.clear()
w7.write('Time: {0:.2f}'.format(diffTime))
mywindow.update()
mywindow.exitonclick()
