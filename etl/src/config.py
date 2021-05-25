from pydantic import BaseSettings


class Settings(BaseSettings):
    message_wait_seconds: int
    message_batch_size: int
    kafka_consumer_group: str
    kafka_topics: list[str] = []
    kafka_hosts: list[str] = []
    clickhouse_main_host: str
    clickhouse_alt_hosts: list[str] = []

    @property
    def kafka_hosts_as_string(self):
        return ",".join(self.kafka_hosts)

    @property
    def clickhouse_alt_hosts_as_string(self):
        return ",".join(self.clickhouse_alt_hosts)


settings = Settings()
