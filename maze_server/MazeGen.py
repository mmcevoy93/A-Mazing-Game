import random
import time


def maze_gen(size):
    maze = []  # To refer to a location in a maze, go maze[y][x]
    unvisited = {}  # dictionary to keep track of which arent checked
    stack = []  # used to backtrack to a non deadend
    counter = 0  # next few counters are just to generate initial maze
    rowcounter = 0

    # new couple loops create the stage for maze[]
    for i in range(size):  # the top left is zero
        maze.append(1)
        maze[i] = []
        for j in range(size):
            if rowcounter % 2 != 0:
                maze[i].append("P")
                counter = counter + 1
                continue

            if (counter % 2) == 0:
                maze[i].append("W")  # initally marked as B, ie a black square

                if (i, j) not in unvisited:
                    unvisited[(i, j)] = 1
            else:
                maze[i].append("P")
            counter = counter + 1
        rowcounter = rowcounter + 1

    # top left as start of maze
    currentcell = (0, 0)
    del unvisited[currentcell]

    while unvisited:

        y = currentcell[0]
        x = currentcell[1]
        unvisited_neighbors = []
        neighbors = []
        # change
        # begging of drastic changes

        # upper left cornner case
        if (y == 0) and (x == 0):
            down = (y + 2, x)
            right = (y, x + 2)
            neighbors = [down, right]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)
            # print(unvisited_neighbors)
            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                # print(random_unvisited_neighbor)
                stack.append(currentcell)  # push currentcell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == down:
                    maze[y + 1][x] = "W"
                elif random_unvisited_neighbor == right:
                    maze[y][x + 1] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()
            else:
                print("stack empty")
        # left edge of maze case
        elif ((y - 2) >= 0) and ((y + 2) <= (size - 1)) and (x == 0):

            up = (y - 2, x)
            down = (y + 2, x)
            right = (y, x + 2)
            neighbors = [up, down, right]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push currentcell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == down:
                    maze[y + 1][x] = "W"
                elif random_unvisited_neighbor == right:
                    maze[y][x + 1] = "W"
                elif random_unvisited_neighbor == up:
                    maze[y - 1][x] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()

        # bottom left corrner of maze
        elif (y == (size - 1)) and (x == 0):
            up = (y - 2, x)
            right = (y, x + 2)
            neighbors = [up, right]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push currentcell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == right:
                    maze[y][x + 1] = "W"
                elif random_unvisited_neighbor == up:
                    maze[y - 1][x] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()

        # bottom edge of map case
        elif (y == (size - 1)) and ((x + 2) <= (size - 1)) and ((x - 2) >= 0):
            up = (y - 2, x)
            left = (y, x - 2)
            right = (y, x + 2)
            neighbors = [up, left, right]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push cell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == right:
                    maze[y][x + 1] = "W"
                elif random_unvisited_neighbor == up:
                    maze[y - 1][x] = "W"
                elif random_unvisited_neighbor == left:
                    maze[y][x - 1] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()

        # bottom right cornner of map
        elif (y == (size - 1)) and (x == (size - 1)):
            up = (y - 2, x)
            left = (y, x - 2)
            neighbors = [up, left]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push cell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == up:
                    maze[y - 1][x] = "W"
                elif random_unvisited_neighbor == left:
                    maze[y][x - 1] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()

        # right edge of map
        elif ((y - 2) >= 0) and ((y + 2) <= (size - 1)) and (x == (size - 1)):
            up = (y - 2, x)
            left = (y, x - 2)
            down = (y + 2, x)
            neighbors = [up, left, down]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push cell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == up:
                    maze[y - 1][x] = "W"
                elif random_unvisited_neighbor == left:
                    maze[y][x - 1] = "W"
                elif random_unvisited_neighbor == down:
                    maze[y + 1][x] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()

        # top right cornner of map
        elif (y == 0) and (x == (size - 1)):
            left = (y, x - 2)
            down = (y + 2, x)
            neighbors = [left, down]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push currentcell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == left:
                    maze[y][x - 1] = "W"
                elif random_unvisited_neighbor == down:
                    maze[y + 1][x] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()

        # top edge of map
        elif (y == 0) and ((x - 2) >= 0) and ((x + 2) <= (size - 1)):
            left = (y, x - 2)
            down = (y + 2, x)
            right = (y, x + 2)
            neighbors = [left, down, right]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push cell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == left:
                    maze[y][x - 1] = "W"
                elif random_unvisited_neighbor == down:
                    maze[y + 1][x] = "W"
                elif random_unvisited_neighbor == right:
                    maze[y][x + 1] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty
                currentcell = stack.pop()

        # middle of map
        elif ((x - 2) >= 0) and ((x + 2) <= (size - 1)) and ((y - 2) >= 0) and ((y + 2) <= (size - 1)):
            up = (y - 2, x)
            left = (y, x - 2)
            down = (y + 2, x)
            right = (y, x + 2)
            neighbors = [up, left, down, right]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push cell to stack

                # now we will remove the wall between the random cell and
                # currcell
                if random_unvisited_neighbor == left:
                    maze[y][x - 1] = "W"
                elif random_unvisited_neighbor == down:
                    maze[y + 1][x] = "W"
                elif random_unvisited_neighbor == right:
                    maze[y][x + 1] = "W"
                elif random_unvisited_neighbor == up:
                    maze[y - 1][x] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty

                currentcell = stack.pop()

        # time.sleep(0.1)
        # print(stack)
        # for i in range(size):
        #     print(maze[i])

        # print(len(unvisited))
        # time.sleep(0.1)
    # printing the maze
    # for i in range(size):

        # print(maze[i])

    new_days = open('sendfile.txt', 'w')
    for i in range(size):
        for j in range(size):
            if (i == 0) and (j == 0):
                new_days.write('S')
            elif(i == size - 1) and (j == size - 1):
            	new_days.write('F')
            elif maze[i][j] == 'W':
                new_days.write('P')
            else:
                new_days.write('W')
        new_days.write('\n')
