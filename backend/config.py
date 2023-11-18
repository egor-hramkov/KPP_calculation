import os

import cherrypy

conf = {
    'global': {'server.socket_host': '0.0.0.0', 'server.socket_port': 8080},
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        'tools.encode.on': True,
        'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True
    },
}

BASE_DIR = os.path.abspath(os.path.curdir)
GRAPHICS_DIR = BASE_DIR + '\\static\\graphics'
