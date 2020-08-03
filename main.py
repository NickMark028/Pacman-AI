import pygame
import os
import random
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

(n, m, maze, pacman_i, pacman_j) = import_maze('Maps\\Level_3\\Map_3_1.txt')


# create screen

screen = pygame.display.set_mode((len(maze[0])*20, len(maze)*20))

# change tilte and logo
pygame.display.set_caption("Pacman")
logo = pygame.image.load('pacmanicon.png')
pygame.display.set_icon(logo)
#create object
def generate_object(obj_img, X, Y):
    screen.blit(obj_img, (X , Y))
#pacman player
player_img  = pygame.image.load('pacman.png')
player_img0  = pygame.image.load('pacman.png')
player_img90 = pygame.transform.rotate(player_img, 90)
player_img180 = pygame.transform.rotate(player_img, 180)
player_img270 = pygame.transform.rotate(player_img, 270)

print(pacman_i,pacman_j)
X=(pacman_j)*20
Y=(pacman_i)*20
print(maze[pacman_i][pacman_j])
print(pacman_i, pacman_j)
print(X, Y)
#test index
# print(maze[Y // 20][(X - 20) // 20])
# print(Y // 20 , (X - 20) // 20)
# print(maze[Y // 20][(X + 20) // 20])
# print(Y // 20 , (X + 20) // 20)
# print(maze[(Y-20) // 20][X // 20])
# print((Y-20) // 20 , X // 20)
# print(maze[(Y+20) // 20][X // 20])
# print((Y+20) // 20 , X // 20)
#food
food_img = pygame.image.load('food.png')
#ghost
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
        if maze[i][j] == 2:
            ghost_list.append((i, j))

#wall block
block_img = pygame.image.load('wall.png')
block_img1 = pygame.image.load('wall2.png')
block_corner_img = pygame.image.load('wall1.png')

#map (just test, not real map)
# map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
#        [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
#        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
#        [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
#        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#        [1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
#        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
#        [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
#        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
# game loop

running = True
while running:
    screen.fill((0, 0, 0))

    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 3:
                generate_object(food_img, j*20, i*20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and maze[Y // 20][(X - 20) // 20] != 1 and maze[Y // 20][(X - 20) // 20] != 2:
                X -= 20
                maze[Y // 20][X // 20] = 0
                player_img = player_img180
        if keys[pygame.K_RIGHT] and maze[Y // 20][(X + 20) // 20] != 1 and maze[Y // 20][(X + 20) // 20] != 2:
                X += 20
                maze[Y // 20][X // 20] = 0
                player_img = player_img0
        if keys[pygame.K_UP] and maze[(Y - 20) // 20][X // 20] != 1 and maze[(Y - 20) // 20][X // 20] != 2:
                Y -= 20
                maze[Y // 20][X // 20] = 0
                player_img = player_img90
        if keys[pygame.K_DOWN] and maze[(Y + 20)  // 20][X // 20] != 1 and maze[(Y + 20)  // 20][X // 20] != 2:
                Y += 20
                maze[Y // 20][X // 20] = 0
                player_img = player_img270
    generate_object(player_img, X, Y)
    for i in range(0, len(ghost_list)):
        generate_object(ghost_img_list[i % 5], ghost_list[i][1]*20, ghost_list[i][0]*20)
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 1:
                generate_object(block_img, j*20, i*20)
    pygame.display.update()