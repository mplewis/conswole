import websockets
from werkzeug.debug.console import Console

async def wss(websocket, path):
    c = Console()
    async for cmd in websocket:
        print(f"< {cmd.rstrip()}")
        result = c.eval(cmd).replace('\n', '<br>')
        await websocket.send(result)
        print(f"> {result}")

def console_server(host, port):
    return websockets.serve(wss, host, port)
