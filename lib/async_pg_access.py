__author__ = 'agerasym'

import asyncio

from aiopg.sa import create_engine
from .models import DB_CREDENTIALS, GameObject, GameMap


class QueryManager(object):
    credentials = DB_CREDENTIALS

    def _convert(self, gen):
        """
        Converts fetched db object(generator) to list of dicts
        :param gen:
        :return:
        """
        return [dict(item) for item in gen]

    def _get_gameobject_args(self, **kwargs):
        return {'game_object_id': kwargs.get('id'),
                  'x': kwargs.get('x'),
                  'y': kwargs.get('y')}

    @asyncio.coroutine
    def do_transaction(self, *args, **kwargs):
        engine = yield from create_engine(**self.credentials)
        with (yield from engine) as conn:
            res = yield from conn.execute(*args, **kwargs)
            return res

    @asyncio.coroutine
    def check_exists_is_occupied(self, params):
        obj_is_new_query = \
            GameMap.select(GameMap.c.game_object_id == params.get('id'))
        place_is_free_query = \
            GameMap.select(
                (GameMap.c.x == params.get('x')) &
                (GameMap.c.y == params.get('y')))
        obj_is_new = yield from self.do_transaction(obj_is_new_query)
        place_is_free = yield from self.do_transaction(place_is_free_query)
        return self._convert(obj_is_new), self._convert(place_is_free)

    @asyncio.coroutine
    def add_item(self, **kwargs):
        params = self._get_gameobject_args(**kwargs)
        add_object = GameObject.insert().values(**{'id': kwargs.get('id')})
        put_on_map = GameMap.insert().values(**params)
        yield from self.do_transaction(add_object)
        yield from self.do_transaction(put_on_map)

    @asyncio.coroutine
    def update_item(self, **kwargs):
        params = self._get_gameobject_args(**kwargs)
        update_query = GameMap.update().\
            where(GameMap.c.game_object_id == params.pop('game_object_id')
                  ).values(**params)
        yield from self.do_transaction(update_query)

    @asyncio.coroutine
    def delete_item(self, **kwargs):
        params = self._get_gameobject_args(**kwargs)
        delete_from_map = GameMap.delete().\
            where(GameMap.c.game_object_id == params.pop('game_object_id')
                  )
        delete_game_object = GameObject.delete().where(
            GameObject.c.id == kwargs.get('id'))
        yield from self.do_transaction(delete_from_map)
        yield from self.do_transaction(delete_game_object)

    def get_state(self):
        query = GameMap.select()
        return self.do_transaction(query)
