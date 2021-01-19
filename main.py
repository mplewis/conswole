import asyncio
import websockets
from werkzeug.debug.console import Console

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

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
