import asyncio
import json
import logging
import os
import traceback
from dataclasses import asdict
from typing import Any, Literal

from boto3_type_annotations.sqs import Client
from chalice import UnprocessableEntityError

from chalicelib.entity.base import EntityType
from chalicelib.entity.util import ENTITY_MAP
from chalicelib.persistant.asyncio.sqs.model.message import Data, Filter, Message
from chalicelib.service.interface.command import AddModifyEqualCommandIfs


class AsyncSqsAddModifyEqualCommand(AddModifyEqualCommandIfs):
    def __init__(
        self,
        client: Client,
        rel_name: str,
        key: str,
        value: Any,
        data: dict,
        db_name: Literal["service"] = "service",
    ):
        super().__init__(
            rel_name=rel_name, key=key, value=value, db_name=db_name, data=data
        )
        self._client = client
        self.logger = logging.getLogger(__name__)

        assert isinstance(self._rel_name, str)
        assert isinstance(self._key, str)
        assert isinstance(self._data, dict)
        assert self._db_name in ["service"]

    async def execute(self) -> EntityType:
        """
        :return: 빈 Entity 반환(data에 해당하는 값만 담김)
        """
        result = await asyncio.to_thread(
            self.__send_message
        )  # sync to async(Blocking IO만 가능)
        if not result:
            raise UnprocessableEntityError("Cannot modify data")
        entity = ENTITY_MAP[self._db_name][self._rel_name].from_dict(self._data)
        return entity

    def __send_message(self) -> bool:
        try:
            sqs_queue_url: str = self._client.get_queue_url(
                QueueName=os.getenv("DB_QUEUE_NAME")
            )["QueueUrl"]
            if self._db_name == "service":
                db_name = os.getenv("MONGO_DB")
            message = Message(
                db_name=db_name,
                rel_name=self._rel_name,
                origin="api",
                action="ADD",
                filters=[Filter(column=self._key, value=self._value, op="eq")],
                data=[Data(column=k, value=v) for k, v in self._data.items()],
            )
            self._client.send_message(
                QueueUrl=sqs_queue_url,
                MessageBody=json.dumps(asdict(message)),
            )
        except Exception as e:
            self.logger.error(traceback.format_exc())
            return False
        else:
            return True
