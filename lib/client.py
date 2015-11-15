__author__ = 'agerasym'

import aiohttp
import asyncio
import uuid
import json
import random


async def get_state(client, url):
    async with client.get(url) as resp:
        return await resp.json()


async def add_item(client, url, state):
    # assume grid 10X10
    if len(state) >= 20:
        return
    params = json.dumps({"actions": [{ "type": "add_item",
             "params": {
                 "id": str(uuid.uuid4()),
                 "x": random.randint(1,10),
                 "y": random.randint(1,10)}}]})
    async with client.post(url, data=params.encode('utf-8')) as request:
        print(request.status)


async def move_item(client, url, state):
    id_index = random.randint(0, len(state))
    game_object_id = state[id_index].get('game_object_id')
    params = json.dumps({"actions": [{ "type": "move_item",
             "params": {
                 "id": game_object_id,
                 "x": random.randint(1,10),
                 "y": random.randint(1,10)}}]})
    async with client.post(url, data=params.encode('utf-8')) as request:
        print(request.status)


async def remove_item(client, url, state):
    if len(state) <= 10:
        return
    id_index = random.randint(0, len(state))
    game_object_id = state[id_index].get('game_object_id')
    print(game_object_id)
    params = json.dumps({"actions": [{ "type": "remove_item",
             "params": {
                 "id": game_object_id}}]})
    async with client.post(url, data=params.encode('utf-8')) as request:
        print(request.status)


def main():
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    state = loop.run_until_complete(
        get_state(client, 'http://localhost:8080/get_state'))
    # resp = loop.run_until_complete(
    #     add_item(client, 'http://localhost:8080/update_state', state))
    # resp = loop.run_until_complete(
    #     move_item(client, 'http://localhost:8080/update_state', state))
    resp = loop.run_until_complete(
        remove_item(client, 'http://localhost:8080/update_state', state))
    client.close()

if __name__ == '__main__':
    main()
