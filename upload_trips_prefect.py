import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from useful_pandas import clean_columns, fast_insert
import requests
import logging
from io import BytesIO
from prefect import task, flow
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector
from datetime import timedelta
import argparse
from dataclasses import dataclass


@dataclass # needed to provide type hints for prefect flow
class upload_trips_params:
    drivername: str
    username: str
    password: str
    host: str
    port: str
    database: str
    table_name: str
    url: str


@task(log_prints=True, retries=3)
def check_db_connection(engine: Engine) -> bool:
    try:
        conn = engine.connect()
        conn.close()
        return True
    except:
        return False


@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract(url: str) -> pd.DataFrame:
    response = requests.get(url, stream=True)

    if not response.ok:
        raise Exception(f'Failed to download data from {url}, response code: {response.status_code}.')

    with BytesIO(response.content) as f:
        return pq.read_table(f).to_pandas()


@task(log_prints=True, retries=3)
def transform(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data
        .pipe(clean_columns)
        .query('passenger_count > 0')
    )


@task(log_prints=True, retries=3)
def load(data: pd.DataFrame, table_name: str, engine: Engine) -> bool:
    return fast_insert(data, table_name, engine)


@flow(name='Ingest Yellow Taxi Trips data from source site to a postgres database.')
def main(params: upload_trips_params) -> None:
    # Setup #
    drivername, username, password = params.drivername, params.username, params.password
    database, host, port = params.database, params.host, params.port
    table_name, url = params.table_name, params.url
    
    engine = create_engine(f"{drivername}://{username}:{password}@{host}:{port}/{database}")
    if check_db_connection(engine) == False:
        raise Exception("Failed to connect to database. Check connection parameters.")

    # ETL #
    data = extract(url)
    num_rows = len(data)
    logging.info(f'Read {num_rows} rows from {url}.')

    data = data.pipe(transform)
    num_rows = len(data)
    logging.info(f'{num_rows} rows after transformation.')

    status = load(data, table_name, engine)
    if status == False:
        raise Exception(f'Failed to write {num_rows} rows to {table_name} table.')
    logging.info(f'Finished writing {num_rows} rows to {table_name} table.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Yellow Taxi Trips data from source site to a postgres database')
    parser.add_argument('--drivername', type=str, default='postgresql+psycopg2', help='Database driver name')
    parser.add_argument('--username', type=str, default='postgres', help='Database username')
    parser.add_argument('--password', type=str, default='postgres', help='Database password')
    parser.add_argument('--host', type=str, default='localhost', help='Database host')
    parser.add_argument('--port', type=str, default='5432', help='Database port')
    parser.add_argument('--database', type=str, default='postgres', help='Database name')
    parser.add_argument('--table_name', type=str, default='yellow_taxi_trips', help='Table name')
    parser.add_argument('--url', type=str, default='https://github.com/cdrowley/data-engineering-zoomcamp/raw/main/data/trips_sample.parquet.gzip', help='URL to download data from')

    args = parser.parse_args()
    
    main(upload_trips_params(**vars(args)))
