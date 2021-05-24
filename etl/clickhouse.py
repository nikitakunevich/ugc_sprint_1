from typing import List
from clickhouse_driver import Client
from config import settings
from models import Event

# clickhouse client init
clickhouse_client = Client(host=settings.clickhouse_main_host, alt_hosts=settings.clickhouse_alt_hosts_as_string)


def init_clickhouse_database():
    clickhouse_client.execute('CREATE DATABASE IF NOT EXISTS analytics ON CLUSTER company_cluster')
    clickhouse_client.execute(
        '''CREATE TABLE IF NOT EXISTS analytics.regular_table ON CLUSTER company_cluster 
        (
            user_id String, 
            movie_id String, 
            movie_timestamp Int32, 
            language String, 
            timezone String, 
            ip String,
            type String,
            version String
        ) 
        Engine=MergeTree() ORDER BY movie_timestamp'''
    )


def save_to_clickhouse(events: List[Event]):
    clickhouse_client.execute('''INSERT INTO analytics.regular_table (user_id, 
                                                                      movie_id, 
                                                                      movie_timestamp,
                                                                      language,
                                                                      timezone,
                                                                      ip,
                                                                      type,
                                                                      version) VALUES''',
                              ((x.payload.user_id,
                                x.payload.movie_id,
                                x.payload.movie_timestamp,
                                x.language,
                                x.timezone,
                                x.ip,
                                x.type,
                                x.version
                                ) for x in events))
