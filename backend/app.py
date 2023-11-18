import cherrypy

from config import conf
from main import Main

@cherrypy.expose
class CherryApp:
    """Основной класс для бэкэнда веб-приложения"""

    @cherrypy.tools.json_out()
    def GET(self):
        return {"data": Main().response}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """Метод рассчёта всех параметров и возврата json-файла"""
        params = cherrypy.request.json
        if not params:
            return {'error': 'EMPTY PARAMS'}
        return {"data": Main(params).response}


if __name__ == '__main__':
    cherrypy.quickstart(CherryApp(), '/', conf)
