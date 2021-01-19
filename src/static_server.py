from os.path import abspath, dirname, join
from aiohttp import web

CONTENT_TYPES = {
    '.html': 'text/html',
    '.js': 'text/javascript',
}

SRC_DIR = abspath(dirname(__file__))
PROJECT_ROOT = dirname(SRC_DIR)
STATIC_DIR = join(PROJECT_ROOT, 'static')


def content_type_for(path):
    for ext, typ in CONTENT_TYPES.items():
        if path.endswith(ext):
            return typ
    return None


async def handler(request):
    base = request.path[1:] or 'index.html'
    try:
        with open(join(STATIC_DIR, base)) as f:
            return web.Response(text=f.read(), content_type=content_type_for(base))
    except FileNotFoundError:
        return web.Response(status=404, text=f'File not found: {base}')


async def static_server(host, port):
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
