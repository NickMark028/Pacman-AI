########################################################
#                      PACMAN AI                       #
########################################################
import os

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


# Main function
def main():
	(n, m, maze, pacman_i, pacman_j) = import_maze('Maps\\Level_1\\Map_1_1.txt')

	


main()



