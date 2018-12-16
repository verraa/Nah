import time
import http.server
import socketserver

class WebHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print ('got request', self.path)
        if self.path == '/':
            self.show_status()
        else:
            self.send_error(404, 'not found')

    def show_status(self):
        game=self.server.game
        response = 'Uptime is {game.uptime:.2f}'.format(game=game)
        self.respond(response)

    def respond(self, response):
        self.send_response(200)
        self.send_header('Context-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

class GameHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print('connection form', self.request.getpeername())
        while True:
            request = self.rfile.readline().strip().decode('utf-8')
            print(request)
            response = 'you said: ' + request
            self.wfile.write(response.encode('utf-8'))
            self.wfile.write('\n'.encode('utf-8'))
            if request == 'quit':
                print('bye')
                break


class Player:
    def __init__(self, server, username):
        if username in server.players:
            raise ValueError('player "%s" already joined' % (username))
        self.username = username
        self.realname = None
        self.health = 100
        self.gold = 0
        self.score = 0
        self.joined = time.time()
        server.players[username] = self

class GameServer:
    def __init__(self):
        self.players = {}
        self.started = 0
        self.http_server = http.server.HTTPServer(('0.0.0.0', 8080), WebHandler)
        self.http_server.game= self

    @property
    def uptime(self):
        if self.started:
            return time.time() - self.started
        else:
            return 0.0

    def run(self):
        self.started = time.time()
        print('Use control-c to stop')
        self.http_server.serve_forever()

server = GameServer()

# Simulate players joining...
Player(server, 'mike')
Player(server, 'carol')
Player(server, 'jan')
