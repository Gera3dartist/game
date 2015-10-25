__author__ = 'agerasym'

import asyncio
import json

from aiohttp import web
from lib.async_pg_access import query_table


# async def get_state(request):
@asyncio.coroutine
def get_state(request):
    res = yield from query_table()
    response = json.dumps([dict(row) for row in res])
    return web.Response(body=bytes(response, encoding='utf8'),
                        content_type='json')


@asyncio.coroutine
def get_name_from_url(request):
    # need to figure out how to get POST data from requst
    # and write handler for it
    return web.Response(text="some post response goes in here")


def configure_routers(app):
    app.router.add_route('GET', '/', get_state)
    app.router.add_route('POST', '/state', get_name_from_url)


def main():
    app = web.Application()
    configure_routers(app)
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', 8080)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()


if __name__ == '__main__':
    main()

