__author__ = 'agerasym'

import asyncio

from aiopg.sa import create_engine
from .models import DB_CREDENTIALS, GameObject


class QueryManager(object):
    credentials = DB_CREDENTIALS

    @asyncio.coroutine
    def do_transaction(self, *args, **kwargs):
        engine = yield from create_engine(**self.credentials)
        with (yield from engine) as conn:
            res = yield from conn.execute(*args, **kwargs)
            return res

    @asyncio.coroutine
    def get_game_object(self, obj_id):
        pass

    def add_item(self, **kwargs):
        query = GameObject.insert().values(**kwargs)
        self.do_transaction(query)

    def get_state(self):
        query = GameObject.select()
        return self.do_transaction(query)

    def check_can_move(self, game_obj):
        pass
