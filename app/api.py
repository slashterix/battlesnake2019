import json
import random
import copy
from bottle import HTTPResponse
from battlesnake import *
from pprint import pprint

class MoveRequest(object):
    board = None

    def __init__(self, data):
        self.board = Board(data['board'],data['you'])

    def do_move(self):
        board = self.board
        directions = ['up', 'down', 'left', 'right']
        pprint(board.me)
        print("Head X:{} Y:{}".format(board.me.head().x,board.me.head().y))

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
            if not move_coord.isValid():
                print("X: {} Y:{} is out of bounds".format(move_coord.x,move_coord.y))
                directions.remove(direction)


            # Avoid snake tails
            if isinstance(board.gridCoord(move_coord).obj, Snake):
                print("Unsafe move {} {} ".format(direction,board.gridCoord(move_coord)))
                directions.remove(direction)

        pprint(directions)
        if directions:
            return random.choice(directions)
        else:
            return "Womp Womp"

class MoveResponse(HTTPResponse):
    def __init__(self, move):
        assert move in ['up', 'down', 'left', 'right'], \
            "Move must be one of [up, down, left, right]"

        self.move = move
        print("Moving " + move)
        super(HTTPResponse, self).__init__(
            status=200,
            body=json.dumps({"move": self.move}),
            headers={"Content-Type": "application/json"}
        )


class StartResponse(HTTPResponse):
    def __init__(self, color):
        assert type(color) is str, "Color value must be string"
        self.color = color

        super(HTTPResponse, self).__init__(
            status=200,
            body=json.dumps({"color": self.color}),
            headers={"Content-Type": "application/json"}
        )
