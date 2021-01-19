import pkgutil
from os.path import abspath, dirname, join
from aiohttp import web

CONTENT_TYPES = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
}
WERKZEUG_STYLE_CSS = pkgutil.get_data('werkzeug.debug', 'shared/style.css').decode()

SRC_DIR = abspath(dirname(__file__))
PROJECT_ROOT = dirname(SRC_DIR)
STATIC_DIR = join(PROJECT_ROOT, 'static')


def content_type_for(path):
    for ext, typ in CONTENT_TYPES.items():
        if path.endswith(ext):
            return typ
    return None


def static_contents(path):
    if path == 'werkzeug_debug.css':
        return WERKZEUG_STYLE_CSS
    try:
        with open(join(STATIC_DIR, path)) as f:
            return f.read()
    except FileNotFoundError:
        return None


async def handler(request):
    path = request.path[1:] or 'index.html'
    text = static_contents(path)
    if not text:
        web.Response(status=404, text=f'File not found: {path}')
    return web.Response(text=text, content_type=content_type_for(path))


async def static_server(host, port):
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
