from enum import Enum
import numpy as np
import random

AIR_ID = 0
WALL_ID = 1
POINT_ID = 2
GHOST_ID = 3


def between(value, left, right):
    return left <= value <= right


class Pacman:
    def __init__(self, position, maze):
        self.maze = maze
        self.position = position

    def move(self):
        pass


class Ghost:
    def __init__(self, position, maze):
        # Initialize
        self.position = position
        self.maze = maze
        self.current_direction = None
        self.next_direction_list = []
        direction_list = [(0, 1, 'RIGHT'), (-1, 0, 'UP'), (0, -1, 'LEFT'), (1, 0, 'DOWN')]

        # Limit the range that to ghost can move
        for direction in direction_list:
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
            return {'RIGHT': 'LEFT', 'UP': 'DOWN', 'LEFT': 'RIGHT', 'DOWN': 'UP'}[old_direction]


class Lv3:
    def __init__(self, maze, pacman_position, ghosts):
        self.maze = maze
        self.pacman = Pacman(pacman_position, self.maze)
        self.ghosts = [Ghost(ghost_position, self.maze) for ghost_position in ghosts]

    def pacman_update(self):
        return 'LEFT'
        return self.pacman.move()

    def ghosts_update(self):
        directions = []
        for ghost in self.ghosts:
            directions.append(ghost.move_random())
        return directions



