__author__ = 'agerasym'

import asyncio

from aiopg.sa import create_engine
from lib import DB_CREDENTIALS, GameObject


@asyncio.coroutine
def query_table():
    engine = yield from create_engine(**DB_CREDENTIALS)
    with (yield from engine) as conn:
        res = yield from conn.execute(GameObject.select())
        return res



# @asyncio.coroutine
# def fill_table():
#     engine = yield from create_engine(**DB_CREDENTIALS)
#     with (yield from engine) as conn:
#         res = yield from conn.execute(GameObject.select())
#         filled_fields = []
#         for i, row in enumerate(res):
#             yield from conn.execute(GameMap.insert(
#             ).values(
#                 x=i,
#                 y=i,
#                 game_object_id=row.id,
#             ))

##
# loop = asyncio.get_event_loop()
# loop.run_until_complete(fill_table())
