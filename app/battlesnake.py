import json
import copy
import heapq
import random
from pprint import pprint,pformat

# Debugger
import pdb

class Coord(object):
    def __init__(self, coord, obj):
        self.x = coord['x']
        self.y = coord['y']
        self.obj = obj
        self.cost = 2 # Default value

    def __str__(self):
        if self.obj:
            return str(self.obj)
        else:
            return ' '

    def __repr__(self):
        return json.dumps({
                'x': self.x,
                'y': self.y,
                'obj': str(self.obj)
            })

class Food(object):
    def __str__(self):
        return "F"
    __repr__ = __str__


class Snake(object):
    def __init__(self, snake, board):
        self.id = snake['id']
        self.health = snake['health']
        self.body = []
        self.me = False
        #print("Snake Body Creation")
        #print(json.dumps(snake['body']))
        for snake_coord in snake['body']:
            body = Coord(snake_coord,self)
            self.body.append(body)
            board.grid[body.x][body.y] = body

    def head(self):
        return self.body[0]

    def len(self):
        return len(self.body)

    def __str__(self):
        if self.me:
            return "M"
        else:
            return "X"

    def __repr__(self):
        body = []
        for b in self.body:
            body.append({'x': b.x,'y': b.y})
        return json.dumps({
                'id': self.id,
                'health': self.health,
                'me': self.me,
                'body': body
            })

class Board(object):

    def __init__(self, board, you):
        self.height = board['height']
        self.width = board['width']
        self.food = []
        self.snakes  = []
        self.grid = [[Coord({'x':col,'y':row},None) for row in xrange(self.height)] for col in xrange(self.width)]

        for food_coord in board['food']:
            food = Coord(food_coord,Food())
            food.cost = 1 # Lower than normal to indicate its preffered
            self.food.append(food)
            self.grid[food.x][food.y] = food

        for snake_data in board['snakes']:
            snake = Snake(snake_data, self)
            if snake.id == you['id']:
                snake.me = True
                self.me = snake
            else:
                for next in self.gridNeighbours(snake.head()):
                    next.cost = 3 # Avoid locations other snakes might move into
            self.snakes.append(snake)

        #print("Number of snakes {}".format(len(self.snakes)))
        #pprint(self.grid[5][10])
        #pprint (zip(*self.grid), width=120)

    def gridCoord(self, coord):
        return self.grid[coord.x][coord.y]

    def coordIsValid(self, coord):
        return 0 <= coord.x < self.width and 0 <= coord.y < self.height

    def coordIsSnake(self, coord):
        return isinstance(coord.obj, Snake)

    def coordIsNotSnake(self, coord):
        return not isinstance(coord.obj, Snake)

    def gridNeighbours(self,coord):
        up       = copy.copy(coord)
        up.y    -= 1
        down     = copy.copy(coord)
        down.y  += 1
        left     = copy.copy(coord)
        left.x  -= 1
        right    = copy.copy(coord)
        right.x += 1
        results = [up, down, left, right]
        #if (coord.x + coord.y) % 2 == 0: results.reverse() # aesthetics

        #print("All four")
        #pprint(results)
        results = filter(self.coordIsValid, results)
        #print("Filtered")
        #pprint(results)
        results = map(self.gridCoord, results)
        #print("Mapped")
        #pprint(results)
        results = filter(self.coordIsNotSnake, results)
        #print("Filtered again")
        #pprint(results)
        return results

    def heuristic(self, coord):
        heur = 0
        for food in self.food:
            heur += abs(coord.x - food.x) + abs(coord.y - food.y)
        heur = heur / len(self.food)
        return heur


def do_move(board):

    # Find path to food
    move = a_star_search(board, board.me.head())
    if move:
        direction = dirToCoord(board.me.head(),move)
        print("A* suggests moving " + direction)
        return direction

    # No path to food, attempt a safe alternative
    moves = board.gridNeighbours(board.me.head())
    if moves:
        return dirToCoord(board.me.head(),random.choice(moves))
    else:
        print("No where safe to go. Womp womp :(")
        return 'up' #Womp Womp






    directions = ['up', 'down', 'left', 'right']

    for direction in directions[:]:
        move_coord = copy.copy(board.me.head())

        if direction == 'up':
            move_coord.y -= 1
        if direction == 'down':
            move_coord.y += 1
        if direction == 'left':
            move_coord.x -= 1
        if direction == 'right':
            move_coord.x +=1

        # Avoid walls
        if not board.coordIsValid(move_coord):
            print("X: {} Y:{} is out of bounds".format(move_coord.x,move_coord.y))
            directions.remove(direction)
            continue

        # Avoid snake tails
        if isinstance(board.gridCoord(move_coord).obj, Snake):
            print("Unsafe move {} {} ".format(direction,board.gridCoord(move_coord)))
            directions.remove(direction)
            continue

    pprint(directions)
    if directions:
        return random.choice(directions)
    else:
        return 'up' #Womp Womp

def dirToCoord(from_coord, to_coord):
    dx = to_coord.x - from_coord.x
    dy = to_coord.y - from_coord.y

    if dx == 1:
        return 'right'
    elif dx == -1:
        return 'left'
    elif dy == -1:
        return 'up'
    elif dy == 1:
        return 'down'

# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

def a_star_search(board, start):
    #pdb.set_trace()
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if isinstance(current.obj, Food):
            path = reconstruct_path(came_from, start,current)
            return path.pop()

        for next in board.gridNeighbours(current):
            new_cost = cost_so_far[current] + next.cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + board.heuristic(next)
                frontier.put(next, priority)
                came_from[next] = current

    #return came_from, cost_so_far, goals

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    #path.append(start) # optional
    #path.reverse() # optional
    return path

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
