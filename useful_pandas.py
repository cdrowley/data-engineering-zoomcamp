import pandas as pd
import numpy as np
from io import StringIO
from sqlalchemy.engine.base import Engine


def downcast(df: pd.DataFrame, unique_thresh: float = 0.05) -> pd.DataFrame:
    """Compress common dtypes to save memory (RAM)."""
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


def fast_insert(df: pd.DataFrame, table_name: str, engine: Engine, chunksize: int=100_000, if_exists: str="replace") -> bool:
    # create or replace table with schema of the DataFrame
    df.head(0).to_sql(table_name, engine, if_exists=if_exists, index=False)

    try:
        conn = engine.raw_connection() # direct, low-level connection to the database
        with conn.cursor() as cur:
            # use StringIO to write DataFrame as in-memory CSV
            output = StringIO()

            # chunk through DataFrame and write to PostgreSQL
            for (idx, chunk) in df.groupby(np.arange(len(df)) // chunksize):
                # write chunk to StringIO object
                chunk.to_csv(output, sep='\t', header=False, index=False)
                output.seek(0)

                # use COPY command to load into PostgreSQL
                cur.copy_from(output, table_name, null='')
                conn.commit()

                # reset StringIO object for the next chunk
                output.seek(0)
                output.truncate(0)
    except Exception as e:
        return False # failure
    finally:
        conn.close()
        return True # success



if __name__ ==  '__main__' :
    pass