from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_topics: list[str] = []
    kafka_hosts: list[str] = []

    @property
    def kafka_hosts_as_string(self):
        return ",".join(self.kafka_hosts)


settings = Settings()
