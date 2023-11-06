import os

import cherrypy

conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    },
}