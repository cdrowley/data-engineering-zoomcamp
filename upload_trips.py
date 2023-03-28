import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from useful_pandas import clean_columns, fast_insert
import argparse
import requests
import logging
from io import BytesIO


def check_db_connection(engine: Engine) -> bool:
    try:
        conn = engine.connect()
        conn.close()
        return True
    except:
        return False


def download_data(response: requests.Response):
    with BytesIO(response.content) as f:
        return pq.read_table(f).to_pandas().pipe(clean_columns)


def main(params: argparse.Namespace):
    drivername, username, password = params.drivername, params.username, params.password
    database, host, port = params.database, params.host, params.port
    table_name, url = params.table_name, params.url
    
    engine = create_engine(f"{drivername}://{username}:{password}@{host}:{port}/{database}")
    if not check_db_connection(engine):
        raise Exception("Failed to connect to database. Check connection parameters.")

    response = requests.get(url, stream=True)
    if not response.ok:
        raise Exception(f'Failed to download data from {url}, response code: {response.status_code}.')

    data = download_data(response)
    num_rows = len(data)
    logging.info(f'Read {num_rows} rows from {url}.')

    status = fast_insert(data, table_name, engine)
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
    parser.add_argument('--url', type=str, default='https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet', help='URL to download data from')

    args = parser.parse_args()
    main(args)
