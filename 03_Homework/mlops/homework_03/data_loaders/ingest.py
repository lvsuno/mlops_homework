import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    TAXI_TYPE= "yellow"
    URL_PREFIX="https://d37ci6vzurychx.cloudfront.net/trip-data"
    month = kwargs.get("month", 3)
    year = kwargs.get("year", 2023)

    url = f'{URL_PREFIX}/{TAXI_TYPE}_tripdata_{year}-{month:02d}.parquet'
    response = requests.get(url)
    if response.status_code !=200:
        raise Exception(response.text)

    df = pd.read_parquet(io.BytesIO(response.content))
        
    print(f"The number of rows in the loaded data is {df.shape[0]}")
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
