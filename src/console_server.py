import websockets
from werkzeug.debug.console import Console

async def wss(websocket, path):
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


def console_server(host, port):
    return websockets.serve(wss, host, port)
