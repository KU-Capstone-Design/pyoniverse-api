import asyncio

import boto3
import pytest
from boto3_type_annotations.sqs import Client

from chalicelib.persistant.asyncio.sqs.command import AsyncSqsAddModifyEqualCommand
from tests.mock.mock import env


@pytest.fixture
def client(env):
    client: Client = boto3.client("sqs")
    return client


def test_add_message(client):
    # given
    command = AsyncSqsAddModifyEqualCommand(
        client=client,
        db_name="test",
        rel_name="products",
        key="id",
        value=1,
        data={"good_count": 1},
    )
    # when & then
    try:
        asyncio.run(command.execute())
        assert True
    except Exception:
        assert False
