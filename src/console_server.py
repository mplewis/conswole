import websockets
from werkzeug.debug.console import Console

class TearItDown(Exception):
    # TODO: This doesn't really work, but when we do this, we actually just want to gracefully stop the wss
    pass

async def wss(websocket, path):
    c = Console()
    while True:
        try:
            cmd = await websocket.recv()
            print(f"< {cmd.rstrip()}")
            result = c.eval(cmd).replace('\n', '<br>')
            await websocket.send(result)
            print(f"> {result}")
        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
            print('Disconnected')
            raise TearItDown()


def console_server(host, port):
    return websockets.serve(wss, host, port)
