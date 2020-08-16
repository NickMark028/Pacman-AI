import numpy as np
import random
from collections import deque


AIR_ID = 0
WALL_ID = 1
POINT_ID = 2
GHOST_ID = 3
UNEXPLORED = 10
SAFE = 11
NOT_SAFE = 12

DIRECTION_LIST = [(0, 1, 'RIGHT'), (-1, 0, 'UP'), (0, -1, 'LEFT'), (1, 0, 'DOWN')]
OPPOSITE_DIRECTION = {'RIGHT': 'LEFT', 'UP': 'DOWN', 'LEFT': 'RIGHT', 'DOWN': 'UP'}
DIRECTION_MOVEMENT_LIST = {'RIGHT': (0, 1), 'LEFT': (0, -1), 'UP': (-1, 0), 'DOWN': (1, 0)}


def between(value, left, right):
    return left <= value <= right


class Pacman:
    def __init__(self, position, maze):
        self.maze = maze
        self.position = [position[0], position[1]]
        self.mask = UNEXPLORED*np.ones((len(maze), len(maze[0])))
        self.unexplored_node = set()    # Eg: [(1, 2), (5, 2), ...]
        self.food_set = set()           # Similar to explored_node
        self.path = deque()             # Eg. ['LEFT', 'RIGHT', 'UP', 'DOWN', ...]
        self.vision_range = 4

    def get_position(self):
        return (self.position[0], self.position[1])
    def get_at(self, matrix, position):
        return matrix[position[0]][position[1]]
    def set_at(self, matrix, position, value):
        matrix[position[0]][position[1]] = value

    # Check if a position is inside the maze
    def is_inside_map(self, position):
        return \
            0 <= position[0] < len(self.maze) and\
            0 <= position[1] < len(self.maze[0])

    # Pacman choose a direction to move
    def move(self):
        position_tuple = self.get_position()

        # Scan for near by ghosts and mark unexplored area outside of range
        self.scan(position_tuple, self.vision_range)

        # Continue to move where the pacman left off
        if len(self.path) != 0:
            return self.continue_last_path()

        # Attempt to find food
        self.path = self.find_food(position_tuple, self.vision_range)
        if (len(self.path) == 0):

            # Attempt to explore unexplored area
            self.path = self.explore(position_tuple, self.unexplored_node)
            if (len(self.path) == 0):

                # The map is explored completely, now search for food outside of range
                self.path = self.explore(position_tuple, self.food_set)

                # No food left
                if len(self.path) == 0:
                    return 'END_GAME'

        # Move the pacman
        return self.continue_last_path()

    # Continue to move the last path
    def continue_last_path(self):
        next_move = self.path.popleft()

        direction = DIRECTION_MOVEMENT_LIST[next_move]
        self.position[0] += direction[0]
        self.position[1] += direction[1]

        return next_move

    # Scan for near by ghosts and mark unexplored area outside of range
    def scan(self, current_position, depth_limit):
        # The outer range of the pacman is the unexplored area
        if depth_limit == -1:
            if self.get_at(self.mask, current_position) == UNEXPLORED:
                self.unexplored_node.add(current_position)
            return

        # The area inside of pacman vision is explored
        self.check_food(current_position)
        self.check_ghost(current_position)
        self.check_position(current_position)

        # For each neighboor cell
        for direction in DIRECTION_LIST:
            neighboor = (current_position[0] + direction[0], current_position[1] + direction[1])
            if self.is_inside_map(neighboor):
                self.scan(neighboor, depth_limit - 1)

    # Check food & ghost and current position
    def check_food(self, food_position):
        if (self.get_at(self.maze, food_position) == POINT_ID and\
            self.get_at(self.mask, food_position) == UNEXPLORED):
            self.food_set.add(food_position)
    def check_ghost(self, ghost_position):
        # No ghost
        if self.get_at(self.maze, ghost_position) != GHOST_ID:
            return False

        self.set_at(self.mask, ghost_position, NOT_SAFE)
        for direction in DIRECTION_LIST:
            neighboor = (ghost_position[0] + direction[0], ghost_position[1] + direction[1])
            if self.is_inside_map(neighboor):
                self.set_at(self.mask, neighboor, NOT_SAFE)
        return True
    def check_position(self, current_position):
        self.unexplored_node.discard(current_position)
        if self.get_at(self.mask, current_position) == UNEXPLORED:
            self.set_at(self.mask, current_position, SAFE)

    # Find a food within a depth limit
    def find_food(self, current_position, depth_limit):
        path = deque()
        visited_set = set()
        self.find_food_recursively(current_position, depth_limit, path, visited_set)
        return path
    def find_food_recursively(self, current_position, depth_limit, path, visited_set):
        if self.get_at(self.maze, current_position) == POINT_ID:
            return True

        if depth_limit == 0: return False

        visited_set.add(current_position)

        # For each neighboor cell
        for direction in DIRECTION_LIST:
            neighboor = (current_position[0] + direction[0], current_position[1] + direction[1])

            if neighboor not in visited_set and\
                self.is_inside_map(neighboor) and\
                self.get_at(self.maze, neighboor) != WALL_ID and\
                self.get_at(self.mask, neighboor) != NOT_SAFE:

                path.append(direction[2])

                if (self.find_food_recursively(neighboor, depth_limit - 1, path, visited_set)):
                    return True

                path.pop()

        visited_set.discard(neighboor)
        return False

    # Find a path to unexplored area
    def get_path(self, parent, start, goal):
        path = deque()
        current = parent[goal[0]][goal[1]]  # ((row, column), direction)

        while (current[0] != start):
            path.append(current[1])
            current = parent[current[0][0]][current[0][1]]

        path.reverse()

        return path

    # Explore unexplored area
    def explore(self, start, goal_set):
        # No food left in the maze
        if len(self.food_set) == 0: return []

        # Initialize variables
        marked = [[False for _ in range(len(self.maze[0]))] for _ in range(len(self.maze))]
        parent = [[None for _ in range(len(self.maze[0]))] for _ in range(len(self.maze))]  # [((row, column), direction), ...]
        self.set_at(marked, start, True)
        frontier = deque()
        frontier.append(start)

        # Algorithm start
        while (len(frontier) != 0):
            current = frontier.popleft()    # (row, column)

            # If at goal
            if current in goal_set:
                return self.get_path(parent, start, current)

            # Searching for its neighboor
            for direction in DIRECTION_LIST:
                neighboor = (current[0] + direction[0], current[1] + direction[1])

                if (self.is_inside_map(neighboor) and\
                    not self.get_at(marked, neighboor) and\
                    self.get_at(self.maze, neighboor) != WALL_ID and\
                    self.get_at(self.mask, neighboor) != NOT_SAFE):

                    self.set_at(parent, neighboor, (current, direction[2]))
                    self.set_at(marked, neighboor, True)
                    frontier.append(neighboor)

        # Goal is not reachable
        return []


class Ghost:
    def __init__(self, position, maze):
        # Initialize
        self.position = position
        self.maze = maze
        self.current_direction = None
        self.next_direction_list = []

        # Limit the range that to ghost can move
        for direction in DIRECTION_LIST:
            next_row = self.position[0] + direction[0]
            next_column = self.position[1] + direction[1]
            if (between(next_row, 0, len(self.maze)) and\
                between(next_column, 0, len(self.maze[0])) and\
                self.maze[next_row][next_column] != WALL_ID):
                self.next_direction_list.append(direction)

    def move_random(self):
        if self.current_direction is None:
            direction = random.choice(  self.next_direction_list)
            self.current_direction = direction[2]
            return self.current_direction
        else:
            old_direction = self.current_direction
            self.current_direction = None
            return OPPOSITE_DIRECTION[old_direction]


class Lv3:
    def __init__(self, maze, pacman_position, ghosts):
        self.maze = maze
        self.pacman = Pacman(pacman_position, self.maze)
        self.ghosts = [Ghost(ghost_position, self.maze) for ghost_position in ghosts]

    def pacman_update(self):
        return self.pacman.move()

    def ghosts_update(self):
        directions = []
        for ghost in self.ghosts:
            directions.append(ghost.move_random())
        return directions


