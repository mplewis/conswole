import websockets
from werkzeug.debug.console import Console

def wss(stop):
    async def s(websocket, path):
        c = Console()
        try:
            async for cmd in websocket:
                print(f"< {cmd.rstrip()}")
                result = c.eval(cmd).replace('\n', '<br>')
                await websocket.send(result)
                print(f"> {result}")
        finally:
            print('Disconnected')
            stop()
    return s

def console_server(host, port):
    def stop():
        print('OK, stopped')
    return websockets.serve(wss(stop), host, port)
