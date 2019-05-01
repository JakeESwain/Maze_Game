import random
import pprint
import time

# This function creates the maze given a size and difficulty
def maze_make(size, diff):

    # Generates random 2D array with random numbers from 0 to 10
    maze = [[random.randint(0,10) for row in range(size)] for col in range(size)]

    # Creates the maze with open and closed spaces. The lower the difficult the more open spaces
    for row in range(len(maze)):
        for col in range(len(maze)):

            if maze[row][col] > diff:
                maze[row][col] = '.'
            else:
                maze[row][col] = '!'

    # Since the start and end need to be open for the mae to be solvible, the sets them as open
    maze[0][0], maze[1][0], maze[0][1], maze[-1][-1], maze[-2][-1], maze[-1][-2] = '.', '.', '.', '.', '.','.'
    return maze

def maze_nav(maze):
    # Prints instructions for the game
    print('Solve the maze as quick as you can. If you get stuck press r to restart')
    print('w = up')
    print('a = left')
    print('s = down')
    print('d = right')

    # This sets the X from the path of the later BFS search to open spaces
    for row in range(len(maze)):
        for col in range(len(maze)):
            if maze[row][col] == 'X':
                maze[row][col] = '.'

    # sets user to initail postion and starts timer
    row, col = 0, 0
    maze[0][0] = '0'
    t0 = time.time()

    # follows these commands until the maze is complete
    while maze[-1][-1] != 'X' :

        pprint.pprint(maze)
        maze_dir = input('Right, Left, Up, Down? \n')

        # if they reach the end
        if row and col == -1:
            print('you did it')

        # these use index value inorder to restart or move in all four directions
        elif maze_dir == 'r':
            maze_nav(maze)

        elif maze_dir == 'd':
            if maze[row][col+1] == '.':
                maze[row][col+1] = 'X'
                col = col + 1

            elif maze[row][col+1] == '!':
                print('you lose')

        elif maze_dir == 'a':
            if maze[row][col-1] == '.':
                maze[row][col-1] = 'X'
                col = col - 1
            elif maze[row][col-1] == '!':
                print('you lose')

        elif maze_dir == 'w':
            if maze[row-1][col] == '.':
                maze[row-1][col] = 'X'
                row = row - 1
            elif maze[row-1][col] == '!':
                print('you lose')

        elif maze_dir == 's':
            if maze[row+1][col] == '.':
                maze[row+1][col] = 'X'
                row = row + 1
            elif maze[row+1][col] == '!':
                print('you lose')

    maze[row][col] = 'X'
    maze[-1][-1] = 'X'
    pprint.pprint(maze)
    t1 = time.time()

    print("you did it in", t1-t0, "seconds" )
    return t1

# Sets up for the BFS search
def find_edges(maze, node):
    x,y = node
    edges = []
    length = len(maze)
    for x,y in (x, y+1), (x, y-1), (x+1, y), (x-1, y):
        if 0 <= x < length and 0 <= y < length:
            if maze[x][y] == '.':
                edges.append([x,y])
    return edges

# Preforms a BFS search to make sure the maze is solvible before the user sees it
def bfs(maze, node, size, diff):
    stack = [[node]]
    explored = []
    goal = [len(maze)-1, len(maze)-1]
    while stack:
        path = stack.pop(-1)
        node = path[-1]

        if node not in explored:
            explored.append(node)
            edges = find_edges(maze, node)
            for edge in edges:
                new_path = list(path)
                new_path.append(edge)
                stack.append(new_path)
                if edge == goal:
                    # if it is possible to reach the the end. Give the user the maze
                    for x,y in new_path:
                        maze[x][y] = 'X'
                        if maze[x][y] == maze[-1][-1]:
                          maze_nav(maze)
                          break

    # if the maze is not solvible use recursion to create a new one of the same size and diffulcy
    maze =  bfs(maze_make(size, diff), (0,0), diff, size)
    maze_nav(maze)

# calls all of the comands and collects the size and diffuculty parameters
def run():
    diff = int(input('Choose difficulty from 1 to 5: '))
    size = int(input('Input Size from 5 to 10: '))
    bfs(maze_make(size, diff), (0,0), size, diff)


run()
