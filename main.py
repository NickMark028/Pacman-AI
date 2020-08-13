import pygame
import sys
import os
import numpy as np
import random
import time
from Level4 import Lv4 
pygame.init()


# Import a maze from file name
# Return (n, m, 2D_array_maze, pacman_i, pacman_j)
def import_maze(filename):
    if (not os.path.exists(filename)):
        return (0, 0, None)

    file = open(filename, 'r')

    data = file.readline().strip().split(' ')
    n = int(data[0])
    m = int(data[1])
    maze = []

    for i in range(n):
        data = file.readline().strip().split(' ')
        maze.append([int(x) for x in data])

    data = file.readline().strip().split(' ')
    pacman_i = int(data[0])
    pacman_j = int(data[1])

    file.close()

    return (n, m, maze, pacman_i, pacman_j)


(n, m, maze, pacman_i, pacman_j) = import_maze('Maps\\Level_4\\Map_4_3.txt')

# create screen

screen = pygame.display.set_mode((len(maze[0]) * 20, len(maze) * 20))

# change tilte and logo

pygame.display.set_caption("Pacman")
logo = pygame.image.load('pacmanicon.png')
pygame.display.set_icon(logo)


# create object

def generate_object(obj_img, x, y):
    screen.blit(obj_img, (x, y))


# pacman player

player_img = pygame.image.load('pacman.png')
player_img0 = pygame.image.load('pacman.png')
player_img90 = pygame.transform.rotate(player_img, 90)
player_img180 = pygame.transform.rotate(player_img, 180)
player_img270 = pygame.transform.rotate(player_img, 270)

x = (pacman_j) * 20
y = (pacman_i) * 20

# test index
# print(maze[y // 20][(x - 20) // 20])
# print(y // 20 , (x - 20) // 20)
# print(maze[y // 20][(x + 20) // 20])
# print(y // 20 , (x + 20) // 20)
# print(maze[(y-20) // 20][x // 20])
# print((y-20) // 20 , x // 20)
# print(maze[(y+20) // 20][x // 20])
# print((y+20) // 20 , x // 20)

# generate food
food_img = pygame.image.load('food.png')

food_list = set()

# generate ghost

ghost_img_list = []
ghost_list = []
ghost_img1 = pygame.image.load('ghost_1.png')
ghost_img_list.append(ghost_img1)
ghost_img2 = pygame.image.load('ghost_2.png')
ghost_img_list.append(ghost_img2)
ghost_img3 = pygame.image.load('ghost_3.png')
ghost_img_list.append(ghost_img3)
ghost_img4 = pygame.image.load('ghost_4.png')
ghost_img_list.append(ghost_img4)
ghost_img5 = pygame.image.load('ghost_5.png')
ghost_img_list.append(ghost_img5)

for i in range(0, len(maze)):
    for j in range(0, len(maze[0])):
        if maze[i][j] == 3:
            ghost_list.append((i, j))
        if maze[i][j] == 2:
            goal = (i, j)
            food_list.add((i, j))

# wall block

block_img = pygame.image.load('wall.png')
block_img1 = pygame.image.load('wall2.png')
block_corner_img = pygame.image.load('wall1.png')


# movement with keyboard ( not use)
# def left_move():
#     global x, y, player_img
#     if keys[pygame.K_LEFT] and maze[y // 20][(x - 20) // 20] != 1 and maze[y // 20][(x - 20) // 20] != 2:
#         x -= 20
#         maze[y // 20][x // 20] = 0
#         player_img = player_img180
#         return True
#     return False
#
#
# def right_move():
#     global x, y, player_img
#     if keys[pygame.K_RIGHT] and maze[y // 20][(x + 20) // 20] != 1 and maze[y // 20][(x + 20) // 20] != 2:
#         x += 20
#         maze[y // 20][x // 20] = 0
#         player_img = player_img0
#         return True
#     return False
#
#
# def up_move():
#     global x, y, player_img
#     if keys[pygame.K_UP] and maze[(y - 20) // 20][x // 20] != 1 and maze[(y - 20) // 20][x // 20] != 2:
#         y -= 20
#         maze[y // 20][x // 20] = 0
#         player_img = player_img90
#         return True
#     return False
#
#
# def down_move():
#     global x, y, player_img
#     if keys[pygame.K_DOWN] and maze[(y + 20) // 20][x // 20] != 1 and maze[(y + 20) // 20][x // 20] != 2:
#         y += 20
#         maze[y // 20][x // 20] = 0
#         player_img = player_img270
#         return True
#     return False



#movement with oder
score = 0
def move_animation(command):
    global x, y, player_img, maze, score
    #time.sleep(0.5)
    if command == 'END_GAME':
        print('game over')
        return False
    if command == 'LEFT' and maze[y // 20][(x - 20) // 20] != 1:
        x -= 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img180
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img180
    if command == 'RIGHT' and maze[y // 20][(x + 20) // 20] != 1:
        x += 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img90
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img0
    if command == 'UP' and maze[(y - 20) // 20][x // 20] != 1:
        y -= 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img90
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img90
    if command == 'DOWN' and maze[(y + 20) // 20][x // 20] != 1:
        y += 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img270
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img270
    
    return True

def ghost_move_animation(command, y_ghost, x_ghost):
    global maze
    #time.sleep(0.5)
    if command == 'LEFT' and maze[y_ghost // 20][(x_ghost - 20) // 20] != 1:
        maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in food_list else 0
        x_ghost -= 20
        maze[y_ghost // 20][x_ghost // 20] = 3
    if command == 'RIGHT' and maze[y_ghost // 20][(x_ghost + 20) // 20] != 1:
        maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in food_list else 0
        x_ghost += 20
        maze[y_ghost // 20][x_ghost // 20] = 3
    if command == 'UP' and maze[(y_ghost - 20) // 20][x_ghost // 20] != 1:
        maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in food_list else 0
        y_ghost -= 20
        maze[y_ghost // 20][x_ghost // 20] = 3
    if command == 'DOWN' and maze[(y_ghost + 20) // 20][x_ghost // 20] != 1:
        maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in food_list else 0
        y_ghost += 20
        maze[y_ghost // 20][x_ghost // 20] = 3
    
    return (y_ghost // 20, x_ghost // 20)
# BFS for lv 1-2
def BFS(mtx, start, goal):
    frontier = [start]
    expanded = []
    parent_list = []
    flag = np.zeros((len(maze), len(maze[0])))

    while (frontier[0] != goal):
        node = frontier.pop(0)
        flag[node[0]][node[1]] = 1
        expanded.append(node)

        if (flag[node[0] - 1][node[1]] != 1 and (node[0] - 1, node[1]) not in frontier and mtx[node[0] - 1][node[1]] != 1 and mtx[node[0] - 1][node[1]] != 3):
            parent_list.append(((node[0] - 1, node[1]), node))
            frontier.append((node[0] - 1, node[1]))
        if (flag[node[0] + 1][node[1]] != 1 and (node[0] + 1, node[1]) not in frontier and mtx[node[0] + 1][node[1]] != 1 and mtx[node[0] + 1][node[1]] != 3):
            parent_list.append(((node[0] + 1, node[1]), node))
            frontier.append((node[0] + 1, node[1]))
        if (flag[node[0]][node[1] - 1] != 1 and (node[0], node[1] - 1) not in frontier and mtx[node[0]][node[1] - 1] != 1 and mtx[node[0]][node[1] - 1] != 3):
            parent_list.append(((node[0], node[1] - 1), node))
            frontier.append((node[0], node[1] - 1))
        if (flag[node[0]][node[1] + 1] != 1 and (node[0], node[1] + 1) not in frontier and mtx[node[0]][node[1] + 1] != 1 and mtx[node[0]][node[1] + 1] != 3):
            parent_list.append(((node[0], node[1] + 1), node))
            frontier.append((node[0], node[1] + 1))
    expanded.append(goal)
    temp_parent = goal
    temp_path = []
    for n in reversed(parent_list):
        if n[0] == temp_parent:
            temp_parent = n[1]
            temp_path.append(temp_parent)
    path = list(reversed(temp_path))
    path.append(goal)
    print(path)
    movement = []
    for i in range(0, len(path)-1):
        if (path[i][0] - 1, path[i][1]) == (path[i + 1][0], path[i + 1][1]):
            movement.append('UP')
        if (path[i][0] + 1, path[i][1]) == (path[i + 1][0], path[i + 1][1]):
            movement.append('DOWN')
        if (path[i][0], path[i][1] - 1) == (path[i + 1][0], path[i + 1][1]):
            movement.append('LEFT')
        if (path[i][0], path[i][1] + 1) == (path[i + 1][0], path[i + 1][1]):
            movement.append('RIGHT')
    print(movement)
    return movement



# game loop

running = True
t = 0
#cmd = BFS(maze, (pacman_i, pacman_j), goal)
cmd = Lv4(maze, 1, 3, 2, (pacman_i, pacman_j))
cmd_ghost = []
game_running = True

while running:
    screen.fill((0, 0, 0))


    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 2:
                generate_object(food_img, j * 20, i * 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #     keys = pygame.key.get_pressed()
    # if t == len(cmd):
    #     print('?')
    #     sys.exit()


    for i in range(0, len(ghost_list)):
        generate_object(ghost_img_list[i % 5], ghost_list[i][1] * 20, ghost_list[i][0] * 20)
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 1:
                generate_object(block_img, j * 20, i * 20)
    generate_object(player_img, x, y)
    time.sleep(0.1)
    '''if t == len(cmd):
        time.sleep(0.5)
        pygame.display.update()
        break
    move_animation(cmd[t])
    t += 1'''

    if not game_running:
        time.sleep(1)
        print('game_over')
        pygame.display.update()
        break

    game_running = move_animation(cmd.FindPathForPaceman(maze))
    if game_running:
        cmd_ghost = cmd.FindPathForGhosts(maze, ghost_list)
        for i in range(len(ghost_list)):
            ghost_list[i] = ghost_move_animation(cmd_ghost[i], ghost_list[i][0] * 20, ghost_list[i][1] * 20)
            if (y // 20, x // 20) == ghost_list[i]:
                game_running = False
    pygame.display.update()

