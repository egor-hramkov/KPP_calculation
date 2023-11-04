import cherrypy

from backend.config import conf


@cherrypy.expose
class CherryApp:
    """Основной класс для бэкэнда веб-приложения"""

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return f"Вроде всё работает!"

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """Метод рассчёта всех параметров и возврата json-файла"""
        # ToDo Храмков - планирую что этот метод будет обрабатывать основной POST запрос на рассчёт параметров
        params = cherrypy.request.json
        if not params:
            return {'error': 'EMPTY PARAMS'}
        return {"data": params}


if __name__ == '__main__':
    cherrypy.quickstart(CherryApp(), '/', conf)
