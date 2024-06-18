#!/usr/bin/env python
# coding: utf-8

import sys
import numpy as np
import pickle
import pandas as pd
from pathlib import Path



def load_model(filename):
    
    with open(filename, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model



def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    return df


def prepare_data(df: pd.DataFrame, dv, year, month):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)

    return X_val

def apply_model(model_file,taxi_type, year, month):

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'

    print(f'reading the data from {input_file}')
    df = read_data(input_file)

    print('loading the model...')
    dv, model = load_model(model_file)  

    print('Preparing the data by applying the dictionary...')
    X_val = prepare_data(df, dv, year, month)
    print(f'applying the model ...')
    y_pred = model.predict(X_val)

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    return df_result, output_file


def save_results(output_file, df_result: pd.DataFrame):
    print(f'saving the result to {output_file} ...')
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
    print(f'the output file have {Path(output_file).stat().st_size * (10**(-6))} Mb ...')

def run():
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    taxi_type = 'yellow'
    model_filename = 'model.bin'

    MONTH = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]


    Path(f'output/{taxi_type}').mkdir(parents=True, exist_ok=True)
    
    df_result, output_file = apply_model(
        model_file=model_filename,
        taxi_type=taxi_type,
        year=year,
        month=month
    )
    print(f"The mean predicted duration for {MONTH[month-1]} is {np.mean(df_result['predicted_duration'])}")
    save_results(
        output_file=output_file, 
        df_result=df_result
    )


if __name__=='__main__':
    run()