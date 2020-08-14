from enum import Enum
import numpy as np
import random
from collections import deque


UNKNOW = -1
AIR_ID = 0
WALL_ID = 1
POINT_ID = 2
GHOST_ID = 3
GHOST_POSSIBLE_MOVE_ID = 4

DIRECTION_LIST = [(0, 1, 'RIGHT'), (-1, 0, 'UP'), (0, -1, 'LEFT'), (1, 0, 'DOWN')]
OPPOSITE_DIRECTION = {'RIGHT': 'LEFT', 'UP': 'DOWN', 'LEFT': 'RIGHT', 'DOWN': 'UP'}


def between(value, left, right):
    return left <= value <= right


class Pacman:
    def __init__(self, position, maze):
        self.maze = maze
        self.mask = UNKNOW*np.ones((len(maze), len(maze[0])))
        self.position = position
        self.unexplored_node = set()    # Eg: [(1, 2), (5, 2), ...]
        self.food_set = set()           # Similar to explored_node
        self.next_move = None           # Eg: 'LEFT', 'RIGHT', 'UP', 'DOWN'
        self.vision_range = 4

        self.unexplored_node.add(self.position)

    # Check if a position is inside the maze
    def is_inside_map(self, position):
        return \
            0 <= position[0] < len(self.map) and\
            0 <= position[1] < len(self.maze[0])

    # Pacman choose a direction to move
    def move(self):
        if len(self.unexplored_node) != 0:
            self.next_move = self.explore_map(self.food_set)
        else:
            # The map has yet to be explored
            self.scan(self.position, self.vision_range + 1)
            self.next_move = self.find_food(self.position, self.vision_range)

            if (self.next_move is None):
                self.next_move = self.explore_map(self.unexplored_node)

                # The map is fully explored
                if self.next_move is None:
                    self.next_move = self.explore_map(self.food_set)

            return self.next_move

    # Scan the area around the pacman
    def scan(self, current_position, depth_limit):
        if depth_limit == 0:
            self.unexplored_node.add(current_position)
        else:
            self.unexplored_node.discard(current_position)

            # For each neighboor cell
            for direction in DIRECTION_LIST:
                neighboor = (self.position[0] + direction[0], self.position[1] + direction[1])

                if self.is_inside_map(neighboor):
                    if not self.check_ghost(neighboor):
                        self.mask[neighboor[0]][neighboor[1]] = AIR_ID
                    self.scan(neighboor, depth_limit - 1)

    # Check is at position
    def check_ghost(self, ghost_position):
        # No ghost
        if self.map[ghost_position[0]][ghost_position[1]] != GHOST_ID:
            return False

        # Mark a plus cross for the ghost
        self.mask[ghost_position[0], ghost_position[1]] = GHOST_POSSIBLE_MOVE_ID
        for direction in DIRECTION_LIST:
            neighboor = (self.position[0] + direction[0], self.position[1] + direction[1])
            if self.is_inside_map(neighboor):
                self.mask[next_row, next_column] = GHOST_POSSIBLE_MOVE_ID
        return True

    # Find a food within a depth limit
    def find_food(self, current_position, depth_limit):
        path = []
        self.find_food_recursively(current_position, depth_limit)
        return path[0] if len(path) != 0 else None
    def find_food_recursively(self, current_position, depth_limit, path):
        if self.maze[current_position[0]][current_position[1]] == POINT_ID:
            return True

        if depth_limit == 0: return None

        # For each neighboor cell
        for direction in DIRECTION_LIST:
            neighboor = (self.position[0] + direction[0], self.position[1] + direction[1])

            if self.is_inside_map(neighboor):
                if not self.check_ghost(neighboor) and\
                    self.maze[neighboor[0]][neighboor[1]] != WALL_ID and\
                    self.mask[neighboor[0]][neighboor[1]] != GHOST_POSSIBLE_MOVE_ID:

                    path.append(direction[2])

                    if (self.find_food_recursively(neighboor, depth_limit - 1, path)):
                        return True

                    path.pop()

        return False

    ########################################################
    # Find a path to unexplored area
    def get_next_move(self, parent, start, goal):
        current = parent[goal[0]][goal[1]]
        while (current[0] != start):
            current = parent[current[0][0]][current[0][1]]
        return current[1]

    # Explore unexplored area
    def explore_map(self, goal_set):
        # Initialize variables
        node_count = len(self.maze[0])*len(self.maze)
        marked = [[False for _ in range(len(self.maze[0]))] for _ in range(len(self.maze))]
        parent = [[None for _ in range(len(self.maze[0]))] for _ in range(len(self.maze))]  # [((row, column), direction), ...]
        start = self.position
        marked[self.position[0]][self.position[1]] = True
        frontier = deque()
        frontier.append(self.position)

        # Algorithm start
        while (len(frontier) != 0):
            current = frontier.popleft()

            # If at goal
            if current in goal_set:
                return self.get_next_move(parent, start, current)

            # Searching for its neighboor
            for direction in DIRECTION_LIST:
                neighboor = (self.position[0] + direction[0], self.position[1] + direction[1])

                if (not marked[neighboor[0]][neighboor[1]] and\
                    self.maze[neighboor[0]][neighboor[1]] != WALL_ID and\
                    self.mask[neighboor[0]][neighboor[1]] != GHOST_POSSIBLE_MOVE_ID):

                    parent[neighboor[0]][neighboor[1]] = (current, direction[2])
                    marked[neighboor[0]][neighboor[1]] = True
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
            direction = random.choice(self.next_direction_list)
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


