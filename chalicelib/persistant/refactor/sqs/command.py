import asyncio
import json
import logging
import os
from dataclasses import asdict
from typing import List

import boto3

from chalicelib.persistant.asyncio.sqs.model.message import Data, Filter, Message


class AsyncSqsAddModifyEqualCommand:
    def __init__(
        self,
        rel_name: str,
        db_name: str,
        filters: List[Filter],
        updated: List[Data],
    ):
        self.__client = boto3.client("sqs")
        self.__db_name = db_name
        self.__rel_name = rel_name
        self.__filters = filters
        self.__updated = updated
        self.logger = logging.getLogger(__name__)

    async def execute(self):
        sqs_queue_url: str = self.__client.get_queue_url(
            QueueName=os.getenv("DB_QUEUE_NAME")
        )["QueueUrl"]
        if self.__db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self.__db_name

        message = Message(
            db_name=db_name,
            rel_name=self.__rel_name,
            origin="api",
            action="ADD",
            filters=self.__filters,
            data=self.__updated,
        )
        # sync to async(Blocking IO만 가능)
        await asyncio.to_thread(
            self.__client.send_message,
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps(asdict(message)),
        )
