import asyncio
from console_server import console_server
from static_server import static_server

HOST = 'localhost'
WS_PORT = 8765
HTTP_PORT = 8888

loop = asyncio.get_event_loop()

def done():
    print('Client disconnected. Shutting down.')
    loop.stop()

loop.run_until_complete(static_server(HOST, HTTP_PORT))
print(f'Listening for HTTP connections on http://{HOST}:{HTTP_PORT}')

loop.run_until_complete(console_server(HOST, WS_PORT, done))
print(f'Listening for WS connections on ws://{HOST}:{WS_PORT}')

loop.run_forever()
