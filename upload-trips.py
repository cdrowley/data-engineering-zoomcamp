import requests
import pandas as pd
import numpy as np
import argparse
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine # for type hinting
from io import BytesIO, StringIO


def downcast(df: pd.DataFrame, unique_thresh: float = 0.05) -> pd.DataFrame:
    '''Compression of the common dtypes "float64", "int64", "object" or "string"'''
    mem_before = df.memory_usage(deep=True).sum()
    mem_before_mb = round(mem_before / (1024**2), 2)
    df = df.convert_dtypes()

    for column in df.select_dtypes(["string", "object"]):
        if (len(df[column].unique()) / len(df[column])) < unique_thresh:
            df[column] = df[column].astype("category")

    for column in df.select_dtypes(["float"]):
        df[column] = pd.to_numeric(df[column], downcast="float")

    for column in df.select_dtypes(["integer"]):
        if df[column].min() >= 0:
            df[column] = pd.to_numeric(df[column], downcast="unsigned")
        else:
            df[column] = pd.to_numeric(df[column], downcast="signed")

    mem_after = df.memory_usage(deep=True).sum()
    mem_after_mb = round(mem_after / (1024**2), 2)
    compression = round(((mem_before - mem_after) / mem_before) * 100)

    print(
        f"DataFrame compressed by {compression}% from {mem_before_mb} MB down to {mem_after_mb} MB."
    )
    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df


def fast_insert(df: pd.DataFrame, table_name: str, engine: Engine, chunksize: int=100_000, if_exists: str="replace"):
    df.head(0).to_sql(table_name, engine, if_exists=if_exists, index=False)

    try:
        conn = engine.raw_connection() # direct/low-level connection to the database
        with conn.cursor() as cur:
            output = StringIO()

            for (idx, chunk) in df.groupby(np.arange(len(df)) // chunksize):
                if idx % 10 == 0:
                    print(f'Writing chunk {idx} of {len(df) // chunksize} to {table_name} table')
                chunk.to_csv(output, sep='\t', header=False, index=False)
                output.seek(0)

                cur.copy_from(output, table_name, null='')
                conn.commit()

                # reset StringIO for next chunk
                output.seek(0)
                output.truncate(0)
    finally:
        conn.close()


def main(params: dict):
    drivername = params.drivername
    username, password = params.username, params.password
    host, port = params.host, params.port
    database, table_name = params.database, params.table_name
    url = params.url

    engine = create_engine(f"{drivername}://{username}:{password}@{host}:{port}/{database}")

    # Downland Yellow Taxi Trips data
    r = requests.get(url, stream=True)

    if not r.ok:
        raise Exception(f'Failed to download data from {url}, response code: {r.status_code}')

    with BytesIO(r.content) as f: 
        trips = pq.read_table(f).to_pandas().pipe(clean_columns).pipe(downcast)

    # Write Yellow Taxi Trips to database
    print(f'Writing {len(trips)} rows to {table_name} table')
    fast_insert(trips, table_name, engine)
    print(f'Finished writing {len(trips)} rows to {table_name} table')


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
    print(args)
    main(args)
