__author__ = 'agerasym'

import asyncio
import json
from aiohttp import web
from lib.async_pg_access import QueryManager


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
        self.router.add_route('GET', '/', self.get_state)
        self.router.add_route('POST', '/state', self.update_state)

    @asyncio.coroutine
    def get_state(self, request):
        res = yield from self.manager.get_state()
        result = [dict(row) for row in res]
        return self.send_response(result)

    @asyncio.coroutine
    def update_state(self, request):
        result = {}
        data = yield from request.json()
        for action in data:
            method = getattr(self, action.get("type"), None)
            if not method:
                pass
            result.update(method(action.get("type"), action.get("params")))
        return self.send_response(result)

    def add_item(self, action_type, params: dict):
        game_obj = self.manager.get_game_object(params.get(id))
        if game_obj:
            return {action_type: self.FAIL}
        self.manager.add_item(**params)
        return {action_type: self.SUCCESS}

    def move_item(self, action_type, params):
        game_obj = self.manager.get_game_object(params.get(id))
        can_move = self.manager.check_can_move(game_obj)
        if all([game_obj, can_move]):
            # make db record
            return {action_type: self.SUCCESS}
        return {action_type: self.FAIL}

    def remove_item(self, action_type, params):
        game_obj = self.manager.get_game_object(params.get(id))
        if not game_obj:
            return {action_type: self.FAIL}
        # make db record
        return {action_type: self.SUCCESS}


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

