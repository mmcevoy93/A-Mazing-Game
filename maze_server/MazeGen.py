# Nicholas Serrano 1508361
# Maxwell McEvoy
import random
import time


def maze_gen(size):
    maze = []  # To refer to a location in a maze, go maze[y][x]
    unvisited = {}  # dictionary to keep track of which nodes arent checked
    stack = []  # used to backtrack to a non deadend and keep track of position
    counter = 0  # next few counters are just to generate initial maze
    rowcounter = 0

    # couple loops create the stage for maze[], which is a 2D size by size list.
    # To picture what this initally looks like, think of a piece of grid paper.
    # The white squares are the "nodes" and the lines in between all the nodes
    # are the edges connecting them. In our maze, the nodes (P) are the
    # white squares, and the walls(W) are the black squares
    for i in range(size):  # the top left of array is (0,0)
        maze.append(1)
        maze[i] = []
        for j in range(size):
            if rowcounter % 2 != 0:
                maze[i].append("P")
                counter = counter + 1
                continue

            if (counter % 2) == 0:
                maze[i].append("W")  # initally marked as W, ie a black square

                if (i, j) not in unvisited:
                    unvisited[(i, j)] = 1 # key values don't really mean anything
            else:
                maze[i].append("P")
            counter = counter + 1
        rowcounter = rowcounter + 1

    # top left as start of maze
    currentcell = (0, 0)  # current cell is the cell we are currently visiting
    del unvisited[currentcell]  # mark as visited

    while unvisited:  #keep looping until there are no more unvisited nodes
    	
    	# We will use a randomized depth first search based algorithm.
        y = currentcell[0]
        x = currentcell[1]
        unvisited_neighbors = []
        neighbors = []

        # The next bunch of if statements are the different boundaries cases 
        # that currentcell could be at. The maze is a big 
        # square, with cornners, sides, etc. In each case we will check for the 
        # unvisited neighbors at that currentcell, randomly select one of 
        # them using randint, and breaking the wall between the current cell 
        # and randomly selected negihboring cell. Now current cell has been 
        # visited, and added to the stack. In the case we have no unvisited 
        # neighbors at that current cell (such as a "dead end"), we will pop 
        # cells from the stack to travel back to a cell with unvisited neighbors. 

        # upper left cornner case
        if (y == 0) and (x == 0):
            down = (y + 2, x)
            right = (y, x + 2)
            neighbors = [down, right]
            for i in neighbors:
                if i in unvisited:
                    unvisited_neighbors.append(i)

            if unvisited_neighbors:  # if we have any unvisited neighbors
                randnumber = random.randint(0, len(unvisited_neighbors) - 1)
                random_unvisited_neighbor = unvisited_neighbors[randnumber]
                stack.append(currentcell)  # push currentcell to stack

                # now we will remove the wall between the random cell and
                # currcell, and make the random cell the next node to check
                if random_unvisited_neighbor == down:
                    maze[y + 1][x] = "W"
                elif random_unvisited_neighbor == right:
                    maze[y][x + 1] = "W"

                currentcell = random_unvisited_neighbor
                del unvisited[random_unvisited_neighbor]

            elif stack:  # else if the stack is not empty, we will pop an item
                currentcell = stack.pop()

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

    #write the generated maze to text file
    new_days = open('sendfile.txt', 'w')
    new_days.write(str(size)[0])
    new_days.write('\n')
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
