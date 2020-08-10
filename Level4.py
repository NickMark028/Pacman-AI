import queue
class Lv4:
    def __init__(self, maze, Wall, Ghost, Food):
        self.maze_pacman = [[-1 for _ in len(maze[0])] for _ in len(maze)]
        self.maze_time = [[0 for _ in len(maze[0])] for _ in len(maze)]
        self.time_count = 0
        self.wall = Wall
        self.ghost = Ghost
        self.food = Food
        self.direction = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        self.point_for_eating_food = -10**5
        self.point_for_food = 1
        self.poit_for_impact_ghost = 10 ** 10
        self.point_for_exploring = 2

    def FindPathForEachGhost(self, ghost, target, maze):
        height, width = len(maze), len(maze[0])
        frontier = queue.Queue()
        frontier.put(ghost)
        parent = [[-1 for _ in range(len(maze[0]))] for _ in range(len(maze))]
        
        parent[ghost[0]][ghost[1]] = 0

        while not frontier.empty():
            current_node = frontier.put()

            for i in range(4):
                next_node = (current_node[0] + self.direction[i][0], current_node[1] + self.direction[i][1])

                if 0 <= next_node[0] < height and 0 <= next_node[1] < width and maze[next_node[0]][next_node[1]] != self.wall and parent[next_node[0]][next_node[1]] == -1:
                    frontier.put(next_node)
                    parent[next_node[0]][next_node[1]] = current_node[0] * width + current_node[1]

                if next_node == target:
                    next_step = target
                    while parent[next_step[0]][next_step[1]] != ghost[0] * width + ghost[1]:
                        next_step = (parent[next_step[0]][next_step[1]] // width, parent[next_step[0]][next_step[1]] % width)
                    
                    return next_step

        return ghost
            
    def FindPathForGhosts(self, maze, pacman, ghost_list):
        #height, width = len(maze), len(maze[0])
        adjacent_Pacman = [pacman for _ in range(5)]
        move = ["RIGHT" for _ in range(len(ghost_list))]
        for i in range(4):
            adjacent_Pacman[i] = (pacman[0] + self.direction[i][0], pacman[1] + self.direction[i][1])
        for i in range(len(ghost_list)):
            target = adjacent_Pacman[i % 4]
            if ghost_list[i][0] == target or maze[target[0]][target[1]] == self.wall:
                target = pacman
            next_move = FindPathForEachGhost(ghost_list[i], target, maze)
            
            if next_move[0] - 1 == ghost_list[i][0]:
                move[i] = "DOWN"
            elif next_move[0] + 1 == ghost_list[i][0]:
                move[i] = "UP"
            elif next_move[1] - 1 == ghost_list[i][1]:
                move[i] = "LEFT"
        
        return move

    def See(self, x, y, pacman, maze):
        if not (0 <= x < len(maze)) or not (0 <= y < len(maze[0])):
            return self.wall
        if abs(pacman[0] - x) + abs(pacman[1] - y) < 6 and not abs(abs(pacman[0] - x) - abs(pacman[1] - y)) == 5:
            if maze[x][y] == self.ghost:
                return self.ghost
            else:
                self.maze_pacman[x][y] = maze[x][y]
        else:
            return self.maze_pacman[x][y]

    def FindGhost(self, maze, pacman):
        visited, ghost_list = [], []
        q = queue.Queue()

        q.put(pacman)
        visited.append(pacman)
        depth, count = 0, [1, 0]

        while not q.empty() and depth < 5:
            current_node = q.get()
            count[0] -= 1

            for i in range(4):
                next_node = (current_node[0] + self.direction[i][0], current_node[1] + self.direction[i][1])
                
                if next_node not in visited:
                    if self.See(next_node[0], next_node[1], pacman, maze) == self.ghost:
                        ghost_list.append(next_node)
                    q.put(next_node)
                    visited.append(next_node)
                    count[1] += 1
            
            if not count[0]:
                depth += 1
                count[0] += count[1]
                count[1] = 0

        return ghost_list
    
    def CalDistance(self, x, y):
        visited = dict()
        frontier = queue.Queue()

        frontier.put((x, y))
        visited[(x, y)] = 0
        distance_food, distance_explored = 10 ** 15, 10 ** 15
        while not frontier.empty():
            current_node = frontier.get()
            point = visited[current_node]
            for i in range(4):
                new_x, new_y = current_node[0] + self.direction[i][0], current_node[1] + self.direction[i][1]
                if 0 <= new_x < len(self.maze_pacman) and 0 <= new_y < len(self.maze_pacman[0]) and ((new_x, new_y) not in visited) and self.maze_pacman[new_x][new_y] != self.wall:
                    visited[(new_x, new_y)] = point + 1
                    if self.maze_pacman[new_x][new_y] != -1:
                        frontier.put((new_x, new_y))
                        distance_explored = min(distance_explored, point + 1)
                    if self.maze_pacman[new_x][new_y] == self.food:
                        distance_food = min(distance_food, point + 1)
        
        return distance_food, distance_explored
    def CalHeuristicFunction(self, x, y):
        distance_food, distance_explored = self.CalDistance(x, y)
        if distance_food == 10 ** 15 and distance_explored == 10 ** 15:
            return 10 ** 15
        if distance_food == 10 ** 15:
            distance_food = 0
        if distance_explored == 10 ** 15:
            distance_explored = 0`
        
        return self.point_for_food * distance_food + self.point_for_exploring * distance_explored + self.time_count[x][y]

    def PredictPathofGhost(self, ghost_list, maze, pacman):
        possible_way = [ghost_list]

        depth = 0
        while depth < 5:
            visited = []
            for (x, y) in possible_way[depth]:
                for i in range(4):
                    x, y = x + self.direction[i][0], y + self.direction[i][1]
                    
                    if (x, y) not in visited and self.See(x, y, pacman, maze) != self.wall:
                        visited.append((x, y))
                    
                    x, y = x - self.direction[i][0], y - self.direction[i][1]

            possible_way.append(visited)
            depth += 1
        
        return possible_way

    

    def CalPointForPredictivePath(self,x, y, predictive_path, maze, pacman, step):
        point = 0
        
        cell = self.See(x, y, pacman, maze)
        if (x, y) in predictive_path[step] or (x, y) in predictive_path[step + 1]:
            point += self.poit_for_impact_ghost * 
        if cell = self.food:
            point += self.point_for_eating_food
            self.maze_pacman[x][y] = 0

        if step == 4:
            point += self.CalHeuristicFunction(x, y)
        else:
            min_point = 10 ** 18
            for i in range(4):
                new_x, new_y = x + self.direction[i][0], y + self.direction[i][1]
                if self.See(new_x, new_y, pacman, maze) != self.wall:
                    min_point = min(min_point, self.CalPointForPredictivePath(new_x, new_y, predictive_path, maze, pacman, step + 1))

        self.maze_pacman[x][y] = self.food

        return point + min_point

        
    def FindPathForPaceman(self, maze, pacman):
        ghost_list = self.FindGhost(maze, pacman)
        predictive_path = self.PredictPathofGhost(ghost_list, maze, pacman)

        min_point, next_step = 10 ** 18, 0
        for i in range(4):
            x, y = pacman[0] + self.direction[i][0], self.direction[i][1]
            if self.See(x, y, pacma, maze) != self.wall:
                temp_point = self.CalPointForPredictivePath(x, y, predictive_path, maze):
                if min_point > temp_point:
                    min_point = temp_point, next_step = i

        x, y = pacman[0] + self.direction[next_step][0], pacman[1] + self.direction[next_step][1]
        if 0 <= x < len(self.maze_pacman) and 0 <= y < len(self.maze_pacman[0]):
           if self.maze_pacman[x][y] == self.food:
               self.maze_pacman[x][y] = 0

        if next_step == 0:
            return "UP"
        elif next_step == 1:
            return "DOWN"
        elif next_step == 2:
            return "LEFT"
        else:
            return "RIGHT"