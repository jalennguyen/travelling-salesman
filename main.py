import turtle
import random
import time
import math
import itertools


def generate_sites(n):
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


def draw_sites(sites):
    w.clear()
    w.penup()
    for j in range(0, len(sites), 1):
        if j == 0 or j == len(sites) - 1:
            w.goto(sites[j][0], sites[j][1])
            w.turtlesize(0.5)
            w.stamp()
            w.turtlesize(0.2)
        else:
            w.goto(sites[j][0], sites[j][1])
            w.stamp()


def draw_path(path):
    w1.clear()
    w1.pendown()
    for k in range(0, len(path), 1):
        if k == 0:
            w1.penup()
            w1.goto(path[k][0], path[k][1])
            w1.pendown()
        else:
            w1.goto(path[k][0], path[k][1])


def shuffle_sites(path):
    random.shuffle(path)
    return path


def calc_dist(site1, site2):
    dist = ((site1[0] - site2[0]) ** 2 + (site1[1] - site2[1]) ** 2) ** 0.5
    return dist


def path_dist(tour):
    total = 0
    for i in range(0, len(tour) - 1, 1):
        total += calc_dist(tour[i], tour[i + 1])
    return total


def swap(tour, i, j):
    new_path = []
    for k in range(0, i, 1):
        new_path.append(tour[k])
    new_path.append(tour[j])

    for l in range(j - 1, i, -1):
        new_path.append(tour[l])
    new_path.append(tour[i])

    for m in range(j + 1, len(tour), 1):
        new_path.append(tour[m])

    return new_path


def probability(temp, new_dist, old_dist):
    if new_dist > old_dist:
        return math.exp((old_dist - new_dist) / temp)
    else:
        return 1


def brute_force(sites, home):
    w5.clear()
    w5.write('Brute Force', align='center', font=('Arial', 20, 'bold'))
    window.update()

    possible_sites = sites.copy()
    del possible_sites[0]
    del possible_sites[-1]
    possible_perm = list(itertools.permutations(sites, len(sites)))

    best_dist = float('inf')
    best_path = 0
    for i in range(0, len(possible_perm), 1):
        path = list(possible_perm[i])
        path.insert(0, home)
        path.append(home)
        total = path_dist(path)
        if total < best_dist:
            best_dist = total
            best_path = list(possible_perm[i])

    draw_path(best_path)
    w9.clear()
    w9.write('Best Dist: {0:.2f}'.format(best_dist), align='center')
    window.update()
    time.sleep(5)
    w9.clear()


def greedy(tour):
    w.clear()
    w1.clear()
    w5.clear()
    w5.write('Greedy Search', align='center', font=('Arial', 20, 'bold'))

    sites = tour.copy()
    draw_sites(sites)
    path = []
    home = sites[0]
    path.append(home)

    del sites[0]
    del sites[-1]

    start_time = time.process_time()
    for i in range(0, len(sites), 1):
        current_site = path[len(path) - 1]
        closest_dist = float('inf')
        closest_index = 0
        for j in range(0, len(sites), 1):
            if j != i:
                if calc_dist(current_site, sites[j]) < closest_dist:
                    closest_dist = calc_dist(current_site, sites[j])
                    closest_index = j

        path.append(sites[closest_index])
        del sites[closest_index]

    path.insert(0, home)
    path.append(home)
    draw_path(path)
    end_time = time.process_time()
    diff_time = end_time - start_time

    w9.clear()
    w9.write('Best Dist: {0:.2f}'.format(path_dist(path)), align='center')
    print(f'Greedy Search\n   Best Distance: {path_dist(path)}\n   Time: {diff_time}')
    window.update()
    time.sleep(5)
    w9.clear()


def two_opt(tour):
    w5.clear()
    w5.write('2-Opt', align='center', font=('Arial', 20, 'bold'))

    path = tour.copy()
    draw_sites(path)
    draw_path(path)
    window.update()

    start_time = time.process_time()
    reduction = True
    while reduction:
        reduction = False
        for i in range(1, len(path) - 1, 1):    #side 1 that != home
            for j in range(i + 1, len(path) - 1, 1):
                new_path = swap(path, i, j)
                if path_dist(new_path) < path_dist(path):
                    path = new_path.copy()
                    draw_path(path)
                    w9.clear()
                    w9.write('Current Dist: {0:.2f}'.format(path_dist(path)), align='center')
                    window.update()
                    reduction = True

    end_time = time.process_time()
    diff_time = end_time - start_time
    w8.clear()
    w8.write('Best Dist: {0:.2f}'.format(path_dist(path)))
    w7.clear()
    w7.write('Time: {0:.2f}'.format(diff_time))
    print(f'Two-Opt\n   Best Distance: {path_dist(path)}\n   Time: {diff_time}')
    window.update()
    time.sleep(5)
    w8.clear()
    w7.clear()
    w9.clear()


def sa(tour):
    path = tour.copy()
    draw_sites(path)
    draw_path(path)

    w5.clear()
    w5.write('Simulated Annealing', align='center', font=('Arial', 20, 'bold'))
    window.update()

    temp = 100
    swaps = 0
    start_time = time.process_time()
    while temp > 0.000001:
        reps = 0
        while reps <= 25:
            while True:
                i = random.randint(1, (len(path) - 2))
                j = random.randint(1, (len(path) - 2))
                if i + 2 <= j: # non adj sides
                    break
            new_path = swap(path, i, j)

            prob = probability(temp, path_dist(new_path), path_dist(path)) # generates num 0 - 1
            if prob > random.random():
                gain = path_dist(path) - path_dist(new_path)
                path = new_path.copy()
                draw_path(path)

                w6.clear()
                w6.write('Swaps:' + str(swaps))
                w2.clear()
                w2.write('Temperature: {0:.6f}'.format(temp))
                w3.clear()
                w3.write('Gain: {0:.2f}'.format(gain))
                w4.clear()
                w4.write('Current Dist: {0:.2f}'.format(path_dist(path)))
                swaps += 1
                window.update()
            reps += 1

        temp = temp * 0.995

    # cleanup
    reduction = True
    while reduction:
        reduction = False

        for i in range(1, len(path) - 1, 1):    # side 1 that != home
            for j in range(i + 1, len(path) - 1, 1):
                new_path = swap(path, i, j)
                if path_dist(new_path) < path_dist(path):
                    gain = path_dist(path) - path_dist(new_path)
                    path = new_path.copy()
                    draw_path(path)

                    w6.clear()
                    w6.write('Swaps: ' + str(swaps))
                    w2.clear()
                    w2.write('Temperature: {0:.6f}'.format(temp))
                    w3.clear()
                    w3.write('Gain: {0:.2f}'.format(gain))
                    w4.clear()
                    w4.write('Current Dist: {0:.2f}'.format(path_dist(path)))

                    window.update()
                    swaps += 1
                    reduction = True

    end_time = time.process_time()
    diff_time = end_time - start_time
    print(f'Simulated Annealing\n   Best Distance: {path_dist(path)}\n   Time: {diff_time}')

    w8.clear()
    w8.write('Best Dist: {0:.2f}'.format(path_dist(path)))
    w7.clear()
    w7.write('Time: {0:.2f}'.format(diff_time))
    window.update()


class Marker(turtle.Turtle):
    def __init__(self, xpos, ypos):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.shape('circle')
        self.turtlesize(0.2)
        self.penup()
        self.goto(xpos, ypos)


window = turtle.Screen()
turtle.setup(800, 800)
window.title('Travelling Salesman Problem')

# Defining turtles for drawing
w = Marker(0, 0)    # site stamper
w1 = Marker(0, 0)   # path drawer
w2 = Marker(-170, 330)  # temp
w3 = Marker(65, 330)    # gain
w4 = Marker(230, 330)   # current dist
w5 = Marker(0, 350) # title
w6 = Marker(-330, 330)  # swaps
w7 = Marker(-100, -350) # time
w8 = Marker(60, -350)   # best dist
w9 = Marker(0, 330) # middle upper

window.tracer(0, 0)

# run brute force
sites = generate_sites(8)
home = sites[0]
sites.append(home)
draw_sites(sites)
brute_force(sites, home)

# set up tour for greedy, 2opt, sa
sites = generate_sites(100)
home = sites[0]
del sites[0]
tour = shuffle_sites(sites)
tour.insert(0, home)
tour.append(home)

# run algorithms
greedy(tour)
two_opt(tour)
sa(tour)

window.exitonclick()
