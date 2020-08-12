from enum import Enum
import numpy as np
import random


def between(value, left, right):
    return left <= value <= right


class Lv3:
    class ObjectID(Enum):
        air = 0
        wall = 1
        point = 2
        ghost = 3

    class Pacman:
        def __init__(self, row, column, maze):
            self.maze = maze
            self.row_start = row
            self.column_start = column

        def move(self):
            pass

    class Ghost:
        def __init__(self, row, column, maze):
            # Initialize
            self.column_start = column
            self.row_start = row
            self.maze = maze
            self.direction_index = -1   # -1: origin position
            self.next_direction_list = []
            direction_list = [(0, 1, 'RIGHT'), (-1, 0, 'UP'), (0, -1, 'LEFT'), (1, 0, 'DOWN')]

            # Limit the range that to ghost can move
            for direction in direction_list:
                next_row = self.row_start + direction[0]
                next_column = self.column_start + direction[1]
                if not(
                    between(next_row, 0, len(self.maze)) and\
                    between(next_column, 0, len(self.maze[0])) and\
                    self.maze[next_row, next_column] != ObjectID.wall\
                    ):
                    self.next_direction_list.append(direction)

        def move_random(self):
            if self.direction_index == -1:
                self.direction_index = random(len(self.next_direction_list))
                direction = self.next_direction_list[self.direction_index]
                self.maze[self.row_start, self.column_start] = ObjectID.air
                self.maze[self.row_start + direction[0], self.column_start + direction[1]] = ObjectID.ghost
                return direction[2]
            else:
                direction = self.next_direction_list[self.direction_index]
                self.maze[self.row_start, self.column_start] = ObjectID.ghost
                self.maze[self.row_start - direction[0], self.column_start - direction[1]] = ObjectID.air
                self.direction_index = -1
                return {'RIGHT': 'LEFT', 'UP': 'DOWN', 'LEFT': 'RIGHT', 'DOWN': 'UP'}[direction[2]]

    def __init__(self, maze, pacman_position, ghosts):
        self.maze = maze
        self.pacman = Pacman(pacman_position[0], pacman_position[1], self.maze)
        self.ghosts = [Ghost(ghost[0], ghost[1], self.maze) for ghost in ghosts]

    def update(self):
        self.pacman.move()
        for ghost in self.ghosts:
            ghost.move_random()


