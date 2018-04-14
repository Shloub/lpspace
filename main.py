import cherrypy


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': 'shloub.liquipedia.space'})
    cherrypy.quickstart(HelloWorld())
