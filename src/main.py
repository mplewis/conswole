import asyncio
from console_server import console_server, TearItDown
from static_server import static_server

HOST = 'localhost'
WS_PORT = 8765
HTTP_PORT = 8888

asyncio.get_event_loop().run_until_complete(console_server(HOST, WS_PORT))
print(f'Listening for WS connections on ws://{HOST}:{WS_PORT}')

asyncio.get_event_loop().run_until_complete(static_server(HOST, HTTP_PORT))
print(f'Listening for HTTP connections on http://{HOST}:{HTTP_PORT}')

asyncio.get_event_loop().run_forever()
