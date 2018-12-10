import json
from pprint import pprint,pformat

class Coord(object):
    board_width = 0
    board_height = 0

    def __init__(self, coord, obj):
        self.x = coord['x']
        self.y = coord['y']
        self.obj = obj

    @classmethod
    def setBoardHeight(cls, height):
        cls.board_height = height

    @classmethod
    def setBoardWidth(cls, width):
        cls.board_width = width

    def isValid(self):
        if self.x < 0 or self.x >= self.board_width:
            return False
        if self.y < 0 or self.y >= self.board_height:
            return False
        return True

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
        print("Snake Body Creation")
        print(json.dumps(snake['body']))
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
        Coord.setBoardHeight(self.height)
        Coord.setBoardWidth(self.width)
        self.grid = [[Coord({'x':col,'y':row},None) for col in xrange(self.height)] for row in xrange(self.width)]

        for food_coord in board['food']:
            food = Coord(food_coord,Food())
            self.food.append(food)
            self.grid[food.x][food.y] = food

        for snake_data in board['snakes']:
            snake = Snake(snake_data, self)
            if snake.id == you['id']:
                snake.me = True
                self.me = snake
            self.snakes.append(snake)

        print("Number of snakes {}".format(len(self.snakes)))
        #pprint(self.grid[5][10])
        #pprint (zip(*self.grid), width=120)

    def gridCoord(self, coord):
        return self.grid[coord.x][coord.y]