import bottle
import os
import sys

# Debugger
import pdb

from .api import *
from pprint import pprint
from .battlesnake import *

@bottle.route('/')
def static():
    return '<center><h1>Judgmental Shoelace</h1><img src="' + application.get_url('/static/<path:path>', path='snek.jpg') + '"/></center>'


@bottle.route('/static/<path:path>', name='static')
def static(path):
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
        #host=os.getenv('IP', '0.0.0.0'),
        #port=os.getenv('PORT', '8080'),
        #server='gunicorn',
        #worker_class='gevent',
        #workers=2,
        #reload=True,
        #accesslog='-',
        debug=True)
