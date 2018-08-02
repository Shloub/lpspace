import cherrypy

import filler


class Main(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def filler(self, **kwargs):
        return filler.filler(**kwargs)


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': 'shloub.liquipedia.space'})
    cherrypy.quickstart(Main())
