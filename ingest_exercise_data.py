#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


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


def run(file_name, is_parquet, table_name):

    pg_user = 'root'
    pg_password = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'
    chunksize = 100000
    

    print(f'Ingesting data for file {file_name} into table {table_name}')

    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    
    if is_parquet:
        df = pd.read_parquet(
            file_name,
        )

        for i in range(0, len(df), chunksize):
            df_chunk = df.iloc[i:i+chunksize]
            if i == 0:
                df_chunk.head(0).to_sql(
                    name = table_name,
                    con = engine,
                    if_exists = 'replace'
                )
            df_chunk.to_sql(name = table_name, 
                            con = engine, 
                            if_exists = 'append')   

    else:
        df_iter = pd.read_csv(
            file_name,
            dtype=dtype,
            iterator = True,
            chunksize = chunksize,
        )

        first = True

        for df_chunk in tqdm(df_iter):
            if first:
                df_chunk.head(0).to_sql(
                    name = table_name,
                    con = engine,
                    if_exists = 'replace'
                )
                first = False

            df_chunk.to_sql(name = table_name, 
                            con = engine, 
                            if_exists = 'append')
    
    print("success!")


if __name__ == '__main__':
    run(file_name ='green_tripdata_2025-11.parquet', is_parquet=True, table_name = 'green_trip_data')
    run(file_name ='taxi_zone_lookup.csv', is_parquet=False, table_name = 'table_zone_lookup')

