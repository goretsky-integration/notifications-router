import logging
from collections.abc import Generator

from redis import Redis
from redis.exceptions import ResponseError, ConnectionError

__all__ = ('MessageQueueConsumer',)

logger = logging.getLogger(__name__)


class MessageQueueConsumer:

    def __init__(
            self,
            *,
            redis_client: Redis,
            stream_name: str,
            consumer_group: str,
    ):
        self.__redis_client = redis_client
        self.__stream_name = stream_name
        self.__consumer_group = consumer_group
        self.__is_stream_initiated = False

    def __init_stream_group(self) -> None:
        """Create a consumer group for a stream if it doesn't exist yet."""
        try:
            self.__redis_client.xgroup_create(
                name=self.__stream_name,
                groupname=self.__consumer_group,
                id='0',
                mkstream=True,
            )
        except ResponseError:
            logger.warning(
                'Could not create consumer group "%s" for stream "%s":'
                ' already exists',
                self.__consumer_group,
                self.__stream_name,
            )
        except ConnectionError:
            logger.critical(
                'Could not connect to Redis. Check if Redis is running.'
            )
            exit(1)

        self.__is_stream_initiated = True

    def __enter__(self):
        if not self.__is_stream_initiated:
            self.__init_stream_group()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__redis_client.xgroup_destroy(
            name=self.__stream_name,
            groupname=self.__consumer_group,
        )

    def start_consuming(
            self,
            consumer_name: str,
    ) -> Generator[dict, None, None]:
        """Start consuming messages from a stream."""
        if not self.__is_stream_initiated:
            self.__init_stream_group()

        while True:
            response = self.__redis_client.xreadgroup(
                groupname=self.__consumer_group,
                consumername=consumer_name,
                streams={self.__stream_name: '>'},
                count=2,
                block=0
            )

            for message in response:
                stream_name, messages = message
                for msg in messages:
                    message_id, data = msg
                    logger.info(
                        'Message from %s - %s: %s',
                        stream_name,
                        message_id,
                        data,
                    )
                    yield data['data']
