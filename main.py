import pygame
import sys
import os
import numpy as np
import random
import time
from Level4 import Lv4
from Level3 import Lv3

pygame.init()


# Import a maze from file name
# Return (n, m, 2D_array_maze, pacman_i, pacman_j)
def import_maze(filename):
    if (not os.path.exists(filename)):
        return (0, 0, None, 0, 0)

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



# create screen


# change tilte and logo

pygame.display.set_caption("Pacman")
logo = pygame.image.load('pacmanicon.png')
pygame.display.set_icon(logo)


# create object




# pacman player


# generate food


# generate ghost


# wall block


class MainRun:
    def __init__(self, path, Level):
        # Maze
        self.height, self.width, self.maze, self.pacman_i, self.pacman_j = import_maze(path)

        # Pacman
        self.player_img = pygame.image.load('pacman.png')
        self.player_img0 = pygame.image.load('pacman.png')
        self.player_img90 = pygame.transform.rotate(self.player_img, 90)
        self.player_img180 = pygame.transform.rotate(self.player_img, 180)
        self.player_img270 = pygame.transform.rotate(self.player_img, 270)
        self.x = (self.pacman_j) * 20
        self.y = (self.pacman_i) * 20

        # Food
        self.food_img = pygame.image.load('food.png')
        self.food_list = set()

        # Ghost
        self.ghost_img_list = []
        self.ghost_list = []
        self.ghost_img1 = pygame.image.load('ghost_1.png')
        self.ghost_img_list.append(self.ghost_img1)
        self.ghost_img2 = pygame.image.load('ghost_2.png')
        self.ghost_img_list.append(self.ghost_img2)
        self.ghost_img3 = pygame.image.load('ghost_3.png')
        self.ghost_img_list.append(self.ghost_img3)
        self.ghost_img4 = pygame.image.load('ghost_4.png')
        self.ghost_img_list.append(self.ghost_img4)
        self.ghost_img5 = pygame.image.load('ghost_5.png')
        self.ghost_img_list.append(self.ghost_img5)

        # Wall Block
        self.block_img = pygame.image.load('wall.png')
        self.block_img1 = pygame.image.load('wall2.png')
        self.block_corner_img = pygame.image.load('wall1.png')

        self.score = 0
        self.level = Level
        self.fog = True
        
        # Pygame
        self.screen = pygame.display.set_mode((self.width * 20, self.height * 20+50))

    def generate_object(self,obj_img, x, y):
        self.screen.blit(obj_img, (x, y))
    
    def GenerateGhost(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == 3:
                    self.ghost_list.append((i, j))
                if self.maze[i][j] == 2:
                    self.food_list.add((i, j))

    # movement with oder
    def move_animation(self, command):
        # time.sleep(0.5)
        if command == 'END_GAME':
            print('game over')
            return False
        if command == 'LEFT' and self.maze[self.y // 20][(self.x - 20) // 20] != 1:
            self.x -= 20
            if self.maze[self.y // 20][self.x // 20] == 2:
                self.score += 20
                self.maze[self.y // 20][self.x // 20] = 0
                self.player_img = self.player_img180
                self.food_list.remove((self.y // 20, self.x // 20))
                print((self.y // 20, self.x // 20))
            elif self.maze[self.y // 20][self.x // 20] == 3:
                print('game over')
                return False
            else:
                self.score -= 1
                self.player_img = self.player_img180
        if command == 'RIGHT' and self.maze[self.y // 20][(self.x + 20) // 20] != 1:
            self.x += 20
            if self.maze[self.y // 20][self.x // 20] == 2:
                self.score += 20
                self.maze[self.y // 20][self.x // 20] = 0
                self.player_img = self.player_img0
                self.food_list.remove((self.y // 20, self.x // 20))
                print((self.y // 20, self.x // 20))
            elif self.maze[self.y // 20][self.x // 20] == 3:
                print('game over')
                return False
            else:
                self.score -= 1
                self.player_img = self.player_img0
        if command == 'UP' and self.maze[(self.y - 20) // 20][self.x // 20] != 1:
            self.y -= 20
            if self.maze[self.y // 20][self.x // 20] == 2:
                self.score += 20
                self.maze[self.y // 20][self.x // 20] = 0
                self.player_img = self.player_img90
                self.food_list.remove((self.y // 20, self.x // 20))
                print((self.y // 20, self.x // 20))
            elif self.maze[self.y // 20][self.x // 20] == 3:
                print('game over')
                return False
            else:
                self.score -= 1
                self.player_img = self.player_img90
        if command == 'DOWN' and self.maze[(self.y + 20) // 20][self.x // 20] != 1:
            self.y += 20
            if self.maze[self.y // 20][self.x // 20] == 2:
                self.score += 20
                self.maze[self.y // 20][self.x // 20] = 0
                self.player_img = self.player_img270
                self.food_list.remove((self.y // 20, self.x // 20))
                print((self.y // 20, self.x // 20))
            elif self.maze[self.y // 20][self.x // 20] == 3:
                print('game over')
                return False
            else:
                self.score -= 1
                self.player_img = self.player_img270
        
        return True


    def ghost_move_animation(self, command, y_ghost, x_ghost):
        # time.sleep(0.5)
        if command == 'LEFT' and self.maze[y_ghost // 20][(x_ghost - 20) // 20] != 1:
            self.maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in self.food_list else 0
            x_ghost -= 20
            self.maze[y_ghost // 20][x_ghost // 20] = 3
        if command == 'RIGHT' and self.maze[y_ghost // 20][(x_ghost + 20) // 20] != 1:
            self.maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in self.food_list else 0
            x_ghost += 20
            self.maze[y_ghost // 20][x_ghost // 20] = 3
        if command == 'UP' and self.maze[(y_ghost - 20) // 20][x_ghost // 20] != 1:
            self.maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in self.food_list else 0
            y_ghost -= 20
            self.maze[y_ghost // 20][x_ghost // 20] = 3
        if command == 'DOWN' and self.maze[(y_ghost + 20) // 20][x_ghost // 20] != 1:
            self.maze[y_ghost // 20][x_ghost // 20] = 2 if (y_ghost // 20, x_ghost // 20) in self.food_list else 0
            y_ghost += 20
            self.maze[y_ghost // 20][x_ghost // 20] = 3
    
        return (y_ghost // 20, x_ghost // 20)


    def BFS_for_lv1_2(self, start, goal):
        frontier = [start]
        expanded = []
        parent_list = []
        flag = np.zeros((self.height, self.width))
    
        while (frontier[0] != goal):
            node = frontier.pop(0)
            flag[node[0]][node[1]] = 1
            expanded.append(node)
    
            if (flag[node[0] - 1][node[1]] != 1 and (node[0] - 1, node[1]) not in frontier and self.maze[node[0] - 1][
                node[1]] != 1 and self.maze[node[0] - 1][node[1]] != 3):
                parent_list.append(((node[0] - 1, node[1]), node))
                frontier.append((node[0] - 1, node[1]))
            if (flag[node[0] + 1][node[1]] != 1 and (node[0] + 1, node[1]) not in frontier and self.maze[node[0] + 1][
                node[1]] != 1 and self.maze[node[0] + 1][node[1]] != 3):
                parent_list.append(((node[0] + 1, node[1]), node))
                frontier.append((node[0] + 1, node[1]))
            if (flag[node[0]][node[1] - 1] != 1 and (node[0], node[1] - 1) not in frontier and self.maze[node[0]][
                node[1] - 1] != 1 and self.maze[node[0]][node[1] - 1] != 3):
                parent_list.append(((node[0], node[1] - 1), node))
                frontier.append((node[0], node[1] - 1))
            if (flag[node[0]][node[1] + 1] != 1 and (node[0], node[1] + 1) not in frontier and self.maze[node[0]][
                node[1] + 1] != 1 and self.maze[node[0]][node[1] + 1] != 3):
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
        for i in range(0, len(path) - 1):
            if (path[i][0] - 1, path[i][1]) == (path[i + 1][0], path[i + 1][1]):
                movement.append('UP')
            if (path[i][0] + 1, path[i][1]) == (path[i + 1][0], path[i + 1][1]):
                movement.append('DOWN')
            if (path[i][0], path[i][1] - 1) == (path[i + 1][0], path[i + 1][1]):
                movement.append('LEFT')
            if (path[i][0], path[i][1] + 1) == (path[i + 1][0], path[i + 1][1]):
                movement.append('RIGHT')
    
        return movement


    def Level_1_2(self):
        self.GenerateGhost()
        running = True
        t = 0
        goal = (1, 2)
        for q in self.food_list:
            goal = q
        cmd = self.BFS_for_lv1_2((self.pacman_i, self.pacman_j), goal)
        while running:
            self.screen.fill((0, 0, 0))
    
            for i in range(0, len(self.maze)):
                for j in range(0, len(self.maze[0])):
                    if self.maze[i][j] == 2:
                        self.generate_object(self.food_img, j * 20, i * 20)
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #     keys = pygame.key.get_pressed()
            # if t == len(cmd):
            #     print('?')
            #     sys.exit()
    
            for i in range(0, len(self.ghost_list)):
                self.generate_object(self.ghost_img_list[i % 5], self.ghost_list[i][1] * 20, self.ghost_list[i][0] * 20)
            for i in range(0, len(self.maze)):
                for j in range(0, len(self.maze[0])):
                    if self.maze[i][j] == 1:
                        self.generate_object(self.block_img, j * 20, i * 20)
            self.generate_object(self.player_img, self.x, self.y)
            time.sleep(0.1)
            if t == len(cmd):
                pygame.display.update()
                time.sleep(0.1)
                break
            self.move_animation(cmd[t])
            t += 1
            pygame.display.update()
    
        return
    def Generate_Object_While_Running(self):
        if self.fog:
            for i in range(max(0, self.y // 20 - 4), min(self.height, self.y // 20 + 5)):
                for j in range(max(0, self.x // 20 - 4), min(self.width, self.x // 20 + 5)):
                    if abs(abs(i - self.y // 20) - abs(j - self.x // 20)) == 5:
                        continue
                    if self.maze[i][j] == 2:
                        self.generate_object(self.food_img, j * 20, i * 20)
                    if self.maze[i][j] == 1:
                        self.generate_object(self.block_img, j * 20, i * 20)

            for i in range(0, len(self.ghost_list)):
                if abs(self.ghost_list[i][0] - self.y // 20) + abs(self.ghost_list[i][1] - self.x // 20) < 6 and abs(abs(self.ghost_list[i][0] - self.y // 20) - abs(self.ghost_list[i][1] - self.x // 20)) < 5:
                    self.generate_object(self.ghost_img_list[i % 5], self.ghost_list[i][1] * 20, self.ghost_list[i][0] * 20)

        else:
            for i in range(0, self.height):
                for j in range(0, self.width):
                    if self.maze[i][j] == 2:
                        self.generate_object(self.food_img, j * 20, i * 20)
                    if self.maze[i][j] == 1:
                        self.generate_object(self.block_img, j * 20, i * 20)

            for i in range(0, len(self.ghost_list)):
                self.generate_object(self.ghost_img_list[i % 5], self.ghost_list[i][1] * 20, self.ghost_list[i][0] * 20)

        self.generate_object(self.player_img, self.x, self.y)
        time.sleep(0.5)

    # game loop
    # def Level_3():


    def Level_4(self):
        self.GenerateGhost()
        running = True
        cmd = Lv4(self.maze, 1, 3, 2, (self.pacman_i, self.pacman_j))
        cmd_ghost = []
        game_running = True
    
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))

            self.Generate_Object_While_Running()
    
            if not game_running:
                time.sleep(0.1)
                print('game_over')
                pygame.display.update()
                break
    
            game_running = self.move_animation(cmd.FindPathForPaceman(self.maze))
            if game_running:
                cmd_ghost = cmd.FindPathForGhosts(self.maze, self.ghost_list)
                for i in range(len(self.ghost_list)):
                    self.ghost_list[i] = self.ghost_move_animation(cmd_ghost[i], self.ghost_list[i][0] * 20, self.ghost_list[i][1] * 20)
                    if (self.y // 20, self.x // 20) == self.ghost_list[i]:
                        game_running = False
            pygame.display.update()
    
        return

    def RunGame(self):
        if self.level < 3:
            self.Level_1_2()
        elif self.level == 4:
            self.Level_4()


'''running = True
t = 0
# cmd = BFS(maze, (pacman_i, pacman_j), goal)
# cmd = Lv4(maze, 1, 3, 2, (pacman_i, pacman_j))
cmd = Lv3(maze, (pacman_i, pacman_j), ghost_list)
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
    if t == len(cmd):
        time.sleep(0.5)
        pygame.display.update()
        break
    move_animation(cmd[t])
    t += 1

    if not game_running:
        time.sleep(1)
        print('game_over')
        pygame.display.update()
        break

    # game_running = move_animation(cmd.FindPathForPaceman(maze))
    game_running = move_animation(cmd.pacman_update())
    if game_running:
        # cmd_ghost = cmd.FindPathForGhosts(maze, ghost_list)
        cmd_ghost = cmd.ghosts_update()
        for i in range(len(ghost_list)):
            ghost_list[i] = ghost_move_animation(cmd_ghost[i], ghost_list[i][0] * 20, ghost_list[i][1] * 20)
            # ghost_list[i] = ghost_move_animation(cmd_ghost[i], ghost_list[i][0] * 20, ghost_list[i][1] * 20)
            if (y // 20, x // 20) == ghost_list[i]:
                game_running = False
    pygame.display.update()'''

main_loop = MainRun('Maps\\Level_1\\Map_1_3.txt', 1)
main_loop.RunGame()


