import pygame
import sys
import os
import numpy as np
import random
import time
from Level4 import Lv4
from Level3 import Lv3
from pygame.locals import *

pygame.init()

menu_font = pygame.font.Font('crackman.ttf', 55)
GO_font = pygame.font.Font('crackman.ttf', 120)
scr_width = 800
scr_height = 600
mainClock = pygame.time.Clock()

#Color
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
red_ferrari = (255,40,0)

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


# Create screen and logo, title
global screen
screen = pygame.display.set_mode((scr_width, scr_height), 0 )
pygame.display.set_caption("Pacman")
logo = pygame.image.load('pacmanicon.png')
pygame.display.set_icon(logo)

# Additional functions
def menu_config():
    # change tilte and logo
    pygame.display.set_caption("Pacman")
    logo = pygame.image.load('pacmanicon.png')
    pygame.display.set_icon(logo)

    menu_img = pygame.image.load('pacman_background.png')
    screen.blit(menu_img, (0, 0))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

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

        # Pygame
        self.screen = pygame.display.set_mode((self.width * 20, self.height * 20))

    def generate_object(self, obj_img, x, y):
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
            self.screen.fill(black)

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

    # game loop
    def Level_3(self):
        self.GenerateGhost()
        running = True
        cmd = Lv3(self.maze, (self.pacman_i, self.pacman_j), self.ghost_list)
        game_running = True

        while running:
            self.screen.fill(black)

            for i in range(0, len(self.maze)):
                for j in range(0, len(self.maze[0])):
                    if self.maze[i][j] == 2:
                        self.generate_object(self.food_img, j * 20, i * 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            for i in range(0, len(self.ghost_list)):
                self.generate_object(self.ghost_img_list[i % 5], self.ghost_list[i][1] * 20, self.ghost_list[i][0] * 20)
            for i in range(0, len(self.maze)):
                for j in range(0, len(self.maze[0])):
                    if self.maze[i][j] == 1:
                        self.generate_object(self.block_img, j * 20, i * 20)
            self.generate_object(self.player_img, self.x, self.y)
            time.sleep(1/20)

            if not game_running:
                time.sleep(1/20)
                print('game_over')
                pygame.display.update()
                break

            game_running = self.move_animation(cmd.pacman_update())
            if game_running:
                cmd_ghost = cmd.ghosts_update()
                for i in range(len(self.ghost_list)):
                    self.ghost_list[i] = self.ghost_move_animation(cmd_ghost[i], self.ghost_list[i][0] * 20, self.ghost_list[i][1] * 20)
                    if (self.y // 20, self.x // 20) == self.ghost_list[i]:
                        game_running = False
            pygame.display.update()


    def Level_4(self):
        self.GenerateGhost()
        running = True
        cmd = Lv4(self.maze, 1, 3, 2, (self.pacman_i, self.pacman_j))
        cmd_ghost = []
        game_running = True

        while running:
            self.screen.fill(black)

            for i in range(0, len(self.maze)):
                for j in range(0, len(self.maze[0])):
                    if self.maze[i][j] == 2:
                        self.generate_object(self.food_img, j * 20, i * 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for i in range(0, len(self.ghost_list)):
                self.generate_object(self.ghost_img_list[i % 5], self.ghost_list[i][1] * 20, self.ghost_list[i][0] * 20)
            for i in range(0, len(self.maze)):
                for j in range(0, len(self.maze[0])):
                    if self.maze[i][j] == 1:
                        self.generate_object(self.block_img, j * 20, i * 20)
            self.generate_object(self.player_img, self.x, self.y)
            time.sleep(0.1)

            if not game_running:
                time.sleep(1)
                print('game_over')
                pygame.display.update()
                break

            game_running = self.move_animation(cmd.FindPathForPaceman(self.maze))
            if game_running:
                cmd_ghost = cmd.FindPathForGhosts(self.maze, self.ghost_list)
                for i in range(len(self.ghost_list)):
                    self.ghost_list[i] = self.ghost_move_animation(cmd_ghost[i], self.ghost_list[i][0] * 20,
                                                                   self.ghost_list[i][1] * 20)
                    if (self.y // 20, self.x // 20) == self.ghost_list[i]:
                        game_running = False
            pygame.display.update()

        return

    def RunGame(self):
        if self.level < 3:
            self.Level_1_2()
        elif self.level == 3:
            self.Level_3()
        elif self.level == 4:
            self.Level_4()

click = False

def main_menu():
    while True:
        screen.fill(black)
        menu_config()

        play_button = pygame.Rect(315, 405, 170, 55)
        exit_button = pygame.Rect(235, 515, 350, 55)

        pygame.draw.rect(screen, black, play_button)
        pygame.draw.rect(screen, black, exit_button)

        draw_text("Play", menu_font, red_ferrari, screen, 340, 400)
        draw_text("Quit", menu_font, red_ferrari, screen, 335, 510)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == KEYDOWN:
            #     if event.key == K_ESCAPE:
            #         pygame.quit()
            #         sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if play_button.collidepoint((mx, my)):
            if click:
                lvl_selection_menu()
        if exit_button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        mainClock.tick(60)


def lvl_selection_menu():
    lvl_run = True
    game_over = True
    while lvl_run:
        screen.fill(black)
        menu_config()

        level_1 = pygame.Rect(90, 360, 230, 50)
        level_2 = pygame.Rect(490, 360, 230, 50)
        level_3 = pygame.Rect(90, 445, 230, 50)
        level_4 = pygame.Rect(490, 445, 230, 50)
        exit_button = pygame.Rect(315, 520, 170, 50)

        pygame.draw.rect(screen, black, level_1)
        pygame.draw.rect(screen, black, level_2)
        pygame.draw.rect(screen, black, level_3)
        pygame.draw.rect(screen, black, level_4)
        pygame.draw.rect(screen, black, exit_button)

        draw_text("Level 1", menu_font, red_ferrari, screen, 100, 350)
        draw_text("Level 2", menu_font, red_ferrari, screen, 500, 350)
        draw_text("Level 3", menu_font, red_ferrari, screen, 100, 435)
        draw_text("Level 4", menu_font, red_ferrari, screen, 500, 435)
        draw_text("Back", menu_font, red_ferrari, screen, 340, 510)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if level_1.collidepoint((mx, my)):
            if click:
                path = 'Maps\\Level_1\\Map_1_'
                map_selection_menu(path, 1)
        if level_2.collidepoint((mx, my)):
            if click:
                path = 'Maps\\Level_2\\Map_2_'
                map_selection_menu(path, 2)
        if level_3.collidepoint((mx, my)):
            if click:
                path = 'Maps\\Level_3\\Map_3_'
                map_selection_menu(path, 3)
        if level_4.collidepoint((mx, my)):
            if click:
                path = 'Maps\\Level_4\\Map_4_'
                map_selection_menu(path, 4)
        if exit_button.collidepoint((mx, my)):
            if click:
                lvl_run = False

        pygame.display.update()
        mainClock.tick(60)

def map_selection_menu(path, level):
    map_run = True
    screen = pygame.display.set_mode((scr_width, scr_height), 0)
    while map_run:
        screen.fill(black)
        menu_config()

        map_1 = pygame.Rect(75, 350, 180, 55)
        map_2 = pygame.Rect(550, 350, 180, 55)
        map_3 = pygame.Rect(75, 435, 180, 55)
        map_4 = pygame.Rect(550, 435, 180, 55)
        map_5 = pygame.Rect(315, 400, 180, 55)
        exit_button = pygame.Rect(315, 510, 170, 55)

        pygame.draw.rect(screen, black, map_1)
        pygame.draw.rect(screen, black, map_2)
        pygame.draw.rect(screen, black, map_3)
        pygame.draw.rect(screen, black, map_4)
        pygame.draw.rect(screen, black, map_5)
        pygame.draw.rect(screen, black, exit_button)

        draw_text("Map 1", menu_font, red_ferrari, screen, 85, 350)
        draw_text("Map 2", menu_font, red_ferrari, screen, 565, 350)
        draw_text("Map 3", menu_font, red_ferrari, screen, 85, 435)
        draw_text("Map 4", menu_font, red_ferrari, screen, 565, 435)
        draw_text("Map 5", menu_font, red_ferrari, screen, 335, 400)
        draw_text("Back", menu_font, red_ferrari, screen, 340, 510)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == KEYDOWN:
            #     if event.key == K_ESCAPE:
            #         map_run = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if map_1.collidepoint((mx, my)):
            if click:
                main_loop = MainRun(path + '1.txt', level)
                main_loop.RunGame()
                screen = pygame.display.set_mode((scr_width, scr_height), 0)
        if map_2.collidepoint((mx, my)):
            if click:
                main_loop = MainRun(path + '2.txt', level)
                main_loop.RunGame()
                screen = pygame.display.set_mode((scr_width, scr_height), 0)
        if map_3.collidepoint((mx, my)):
            if click:
                main_loop = MainRun(path + '3.txt', level)
                main_loop.RunGame()
                screen = pygame.display.set_mode((scr_width, scr_height), 0)
        if map_4.collidepoint((mx, my)):
            if click:
                main_loop = MainRun(path + '4.txt', level)
                main_loop.RunGame()
                screen = pygame.display.set_mode((scr_width, scr_height), 0)
        if map_5.collidepoint((mx, my)):
            if click:
                main_loop = MainRun(path + '5.txt', level)
                main_loop.RunGame()
                screen = pygame.display.set_mode((scr_width, scr_height), 0)
        if exit_button.collidepoint((mx, my)):
            if click:
                map_run = False

        pygame.display.update()
        mainClock.tick(60)

def game_over():
    waiting = True

    while waiting:
        draw_text("Game over", GO_font, red_ferrari, 90, 130)


        play_again = pygame.Rect(90, 390, 200, 55)
        quit = pygame.Rect(390, 390, 200, 55)
        pygame.draw.rect(screen, blue, play_again)
        pygame.draw.rect(screen, blue, quit)

        draw_text("Play again", menu_font, red_ferrari, 100, 400)
        draw_text("Quit", menu_font, red_ferrari, 400, 400)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if play_again.collidepoint((mx, my)) or quit.collidepoint((mx, my)):
            if click:
                waiting = False
        # if quit.collidepoint((mx, my)):
        #     if click:
        #         waiting = False

main_menu()
