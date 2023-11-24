import logging
import os
import sys

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Resource
from motor.motor_asyncio import AsyncIOMotorClient


def get_client():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    client.get_io_loop().run_until_complete(client.admin.command("ping"))
    yield client
    client.close()


class ResourceInjector(DeclarativeContainer):
    logging = Resource(
        logging.basicConfig,
        force=True,
        level=logging.INFO,
        stream=sys.stdout,
        datefmt="%Y-%m-%dT%H:%M:%S",
        format="%(asctime)s %(name)s[%(levelname)s]:%(message)s",
    )

    client = Resource(get_client)
