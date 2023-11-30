import boto3
import pytest
from boto3_type_annotations.sqs import Client

from chalicelib.persistant.asyncio.sqs.command import AsyncSqsAddModifyEqualCommand


@pytest.fixture
def client(env):
    client: Client = boto3.client("sqs")
    return client


@pytest.mark.asyncio
async def test_add_message(client):
    # given
    command = AsyncSqsAddModifyEqualCommand(
        client=client,
        db_name="service",
        rel_name="products",
        key="id",
        value=1,
        data={"good_count": 1},
    )
    # when & then
    try:
        await command.execute()
        assert True
    except Exception:
        assert False
