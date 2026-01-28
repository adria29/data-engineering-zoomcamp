#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click


# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

table_name = 'yellow_taxi_data'
chunksize = 100000


@click.command()
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
@click.option('--table-name', default='yellow_taxi_data', help='Database table name')
def run(month, year, pg_user, pg_password, pg_host, pg_port, pg_db, chunksize, table_name):

    print(f'Ingesting data for {year}-{month:02d} into table {table_name}')

    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator = True,
        chunksize = chunksize,
    )

    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name = 'yellow_taxi_data',
                con = engine,
                if_exists = 'replace'
            )
            first = False

        df_chunk.to_sql(name = table_name, 
                        con = engine, 
                        if_exists = 'append')
    
    print("success!")


if __name__ == '__main__':
    run()

