#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


MONTH = 1
YEAR = 2021

pg_user = 'root'
pg_password = 'root'
pg_host = 'localhost'
pg_port = 5432
pg_db = 'my_taxi'

# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_{YEAR}-{MONTH:02d}.csv.gz'

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

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

def run():

    df_iter = pd.read_csv(
        prefix + 'yellow_tripdata_2021-01.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator = True,
        chunksize = 100000,
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

