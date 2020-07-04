from http.server import BaseHTTPRequestHandler, HTTPServer
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
from parlai.scripts.script import ParlaiScript
import parlai.utils.logging as logging

import json
import sys

HOST_NAME = 'localhost'
PORT = 8080

SHARED: Dict[Any, Any] = {}

with open("parlai_chat_web.html", "r", encoding="UTF-8") as web_html: WEB_HTML = web_html.read(1000000)
with open("parlai_chat_web.js", "r", encoding="UTF-8") as js_file: JS_FILE = js_file.read(1000000)
with open("parlai_chat_web_fav_icon.png", "rb") as fav_icon: FAV_ICON = fav_icon.read(1000000)
with open("parlai_chat_web_background.jpg", "rb") as bachground: BACKGROUND = bachground.read(1000000)
with open("parlai_chat_web.css", "r", encoding="UTF-8") as css_file: CSS_FILE = css_file.read(1000000)
with open("parlai_chat_web_hal_character.png", "rb") as hal_character_file: HAL_CHARACTER_FILE = hal_character_file.read(1000000)
with open("parlai_chat_web_user_character.jpg", "rb") as user_character_file: USER_CHARACTER_FILE = user_character_file.read(1000000)


class MyHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests.
    """

    def _interactive_running(self, opt, reply_text):
        reply = {'episode_done': False, 'text': reply_text}
        SHARED['agent'].observe(reply)
        model_res = SHARED['agent'].act()
        return model_res

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Handle POST request, especially replying to a chat message.
        """
        if self.path == '/interact':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            model_response = self._interactive_running(
                SHARED.get('opt'), body.decode('utf-8')
            )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            json_str = json.dumps(model_response)
            self.wfile.write(bytes(json_str, 'utf-8'))
        elif self.path == '/reset':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            SHARED['agent'].reset()
            self.wfile.write(bytes("{}", 'utf-8'))
        else:
            return self._respond({'status': 500})

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/parlai_chat_web.js': {'status': 200},
            '/parlai_chat_web_fav_icon.png': {'status': 202},  # Need for chrome
            '/parlai_chat_web_background.jpg' : {'status': 200},
            '/parlai_chat_web.css' : {'status': 200},
            '/parlai_chat_web_hal_character.png' : {'status': 200},
            '/parlai_chat_web_user_character.jpg' : {'status': 200},
        }
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})

    def _handle_http(self, status_code, path, text=None):
        if path == '/':
            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            content = WEB_HTML
            return bytes(content, 'UTF-8')
        elif path == '/parlai_chat_web_fav_icon.png':
            self.send_response(status_code)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            content = FAV_ICON
            return bytes(content)
        elif path == '/parlai_chat_web_background.jpg':
            self.send_response(status_code)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            content = BACKGROUND
            return bytes(content)
        elif path == '/parlai_chat_web.js':
            self.send_response(status_code)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            content = JS_FILE
            return bytes(content, 'UTF-8')
        elif path == '/parlai_chat_web.css':
            self.send_response(status_code)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            content = CSS_FILE
            return bytes(content, 'UTF-8')
        elif path == '/parlai_chat_web_hal_character.png':
            self.send_response(status_code)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            content = HAL_CHARACTER_FILE
            return bytes(content)
        elif path == '/parlai_chat_web_user_character.jpg':
            self.send_response(status_code)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            content = USER_CHARACTER_FILE
            return bytes(content)

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)


def setup_interweb_args(shared):
    """
    Build and parse CLI opts.
    """
    parser = setup_args()
    parser.add_argument('--port', type=int, default=PORT, help='Port to listen on.')
    parser.add_argument(
        '--host',
        default=HOST_NAME,
        type=str,
        help='Host from which allow requests, use 0.0.0.0 to allow all IPs',
    )
    return parser


def interactive_web(opt, parser):
    SHARED['opt'] = parser.opt

    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])

    # show args after loading model
    parser.opt = agent.opt
    parser.print_args()
    MyHandler.protocol_version = 'HTTP/1.0'
    httpd = HTTPServer((opt['host'], opt['port']), MyHandler)
    logging.info('http://{}:{}/'.format(opt['host'], opt['port']))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


class InteractiveWeb(ParlaiScript):
    @classmethod
    def setup_args(cls):
        return setup_interweb_args(SHARED)

    def run(self):
        return interactive_web(self.opt, self.parser)


if __name__ == '__main__':

    sys.argv.append("-t")
    sys.argv.append("blended_skill_talk")

    sys.argv.append("-mf")
    sys.argv.append("zoo:blender/blender_90M/model")

    InteractiveWeb.main()
