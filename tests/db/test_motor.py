import logging
import os
import time
from asyncio import AbstractEventLoop, gather

import pytest
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ReadPreference

from tests.mock.mock import env


async def do_find_one(db: AsyncIOMotorDatabase, cnt: int):
    coroutines = []
    for i in range(1, cnt + 1):
        coroutines.append(
            db["products"].find_one(
                filter={"id": i},
                projection={"_id": False, "id": True, "name": 1},
                hint=[("id", 1)],
            )
        )
    st = time.time()
    documents = await gather(*coroutines)
    et = time.time()
    elapsed = et - st
    logging.info(f"find_one: {elapsed}")
    return elapsed


async def do_find_many(db: AsyncIOMotorDatabase, cnt: int):
    cursor = (
        db["products"]
        .find({"id": {"$gt": cnt}}, {"_id": False, "id": True, "name": 1})
        .hint([("id", 1)])
        .sort("id", 1)
        .limit(cnt)
    )

    st = time.time()
    docs = await cursor.to_list(None)
    et = time.time()
    elapsed = et - st
    logging.info(f"find_many({len(docs)}): {elapsed}")
    return elapsed


@pytest.fixture
def client(env):
    client = motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
    return client


def test_motor(client: AsyncIOMotorClient, env):
    # given
    db = client.get_database(
        "service_dev", read_preference=ReadPreference.SECONDARY_PREFERRED
    )
    # when
    loop: AbstractEventLoop = client.get_io_loop()
    t1 = loop.run_until_complete(do_find_one(db, 1))
    t2 = loop.run_until_complete(do_find_one(db, 100))
    t3 = loop.run_until_complete(do_find_many(db, 100))
    # then
    assert t1 * 10 > t2
    assert t2 > t3
