import bottle
import os
import sys

# Debugger
import pdb

from api import *
from pprint import pprint
from battlesnake import *

@bottle.route('/')
def static():
    return "<center><h1>Judgmental Shoelace</h1><img src=\"/static/snek.jpg\"/></center>"


@bottle.route('/static/<path:path>')
def static(path):
    pprint (path)
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data
    #pprint(data)

    return StartResponse('#%06X' % random.randint(0,256**3-1))


@bottle.post('/move')
def move():
    data = bottle.request.json
    board = Board(data['board'],data['you'])

    return MoveResponse(do_move(board))


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Any cleanup that needs to be done for this game based on the data
    #print json.dumps(data)


@bottle.post('/ping')
def ping():
    return "Alive"


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
