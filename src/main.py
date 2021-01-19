import asyncio
import websockets
from os.path import abspath, dirname, join
from aiohttp import web
from werkzeug.debug.console import Console

HOST = 'localhost'
WS_PORT = 8765
HTTP_PORT = 8888

SRC_DIR = abspath(dirname(__file__))
PROJECT_ROOT = dirname(SRC_DIR)
STATIC_DIR = join(PROJECT_ROOT, 'static')


async def hello(websocket, path):
    c = Console()
    while True:
        try:
            cmd = await websocket.recv()
            print(f"< {cmd.rstrip()}")
            result = c.eval(cmd).replace('\n', '<br>')
            await websocket.send(result)
            print(f"> {result}")
        except websockets.exceptions.ConnectionClosedError:
            break


async def handler(request):
    without_leading_slash = request.path[1:]
    if not without_leading_slash:
        without_leading_slash = 'index.html'
    target_static_path = join(STATIC_DIR, without_leading_slash)
    try:
        with open(target_static_path) as f:
            return web.Response(text=f.read())
    except FileNotFoundError:
        return web.Response(status=404, text=f'File not found: {without_leading_slash}')
    return web.Response(text="OK", headers=MultiDict([{'Content-Type': 'text/html'}]))

async def main(host, port):
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()


asyncio.get_event_loop().run_until_complete(websockets.serve(hello, HOST, WS_PORT))
print(f'Listening for WS connections on ws://{HOST}:{WS_PORT}')
asyncio.get_event_loop().run_until_complete(main(HOST, HTTP_PORT))
print(f'Listening for HTTP connections on http://{HOST}:{HTTP_PORT}')
asyncio.get_event_loop().run_forever()
