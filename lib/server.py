__author__ = 'agerasym'

import logging
import logging.handlers
import asyncio
import json
from aiohttp import web
from lib.query_manager import QueryManager

logger = logging.getLogger('ServerLogger')
logger.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler(
    'log/server.log', maxBytes=4096, backupCount=5)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
formatter = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s:  %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class BaseApp(web.Application):
    SUCCESS = 200
    FAIL = 100

    def send_response(self, response):
        body = {
            "body": bytes(json.dumps(response), encoding='utf8'),
            "content_type": "json"
        }
        return web.Response(**body)


class App(BaseApp):
    manager = QueryManager()

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.router.add_route('GET', '/get_state', self.get_state)
        self.router.add_route('POST', '/update_state', self.update_state)

    @asyncio.coroutine
    def get_state(self, request):
        res = yield from self.manager.get_state()
        result = [dict(row) for row in res]
        return self.send_response(result)

    @asyncio.coroutine
    def update_state(self, request):
        result = {}
        data = yield from request.json()
        for action in data.pop("actions"):
            method = getattr(self, action.get("type"), None)
            if method:
                r = yield from method(action.get("type"), action.get("params"))
                result.update(r)
        return self.send_response(result)

    def add_item(self, action_type, params: dict):
        logger.info('got params: {}'.format(params))
        exists, is_occupied_place = \
            yield from self.manager.check_exists_is_occupied(params)
        logger.info('exists: {}, is_occupied {}'.format(
            bool(exists), bool(is_occupied_place)))
        if not exists and not is_occupied_place:
            logger.info('adding object: {}'.format(params))
            yield from self.manager.add_item(**params)
            return {action_type: self.SUCCESS}
        return {action_type: self.FAIL}

    def move_item(self, action_type, params):
        exists, is_occupied_place = \
            yield from self.manager.check_exists_is_occupied(params)
        if exists and not is_occupied_place:
            logger.info('moving object: {}'.format(params))
            yield from self.manager.update_item(**params)
            return {action_type: self.SUCCESS}
        return {action_type: self.FAIL}

    def remove_item(self, action_type, params):
        exists, _ = yield from self.manager.check_exists_is_occupied(params)
        if exists:
            logger.info('removing object: {}'.format(params))
            yield from self.manager.delete_item(**params)
            return {action_type: self.SUCCESS}
        return {action_type: self.FAIL}


def main():
    app = App()
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
