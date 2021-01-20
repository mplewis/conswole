import websockets
from datetime import datetime
from werkzeug.debug.console import Console

def wss(done):
    server_init = datetime.now()
    async def s(ws, path):
        c = Console()
        try:
            uptime = datetime.now() - server_init
            print('Client connected.')
            await ws.send(f'CONSWOLE_SERVER_UPTIME:{uptime.total_seconds()}')
            async for cmd in ws:
                print(f"< {cmd.rstrip()}")
                raw = c.eval(cmd)
                result = (raw + '\n').replace('\n', '<br>')
                await ws.send(result)
                print(f"> {result}")
        finally:
            done()
    return s

def console_server(host, port, done):
    return websockets.serve(wss(done), host, port)
