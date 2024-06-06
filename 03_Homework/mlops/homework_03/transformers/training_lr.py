if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from mlops.utils.data_preparation.feature_selector import select_features
from mlops.utils.data_preparation.encoders import vectorize_features
from sklearn.linear_model import LinearRegression


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df = select_features(data)
    target = kwargs.get("target","duration")
    y = data[target].values
    X, _ , dv = vectorize_features(df)
    lr = LinearRegression()
    lr.fit(X, y)
    print(f"The intercept for the fitted model is {lr.intercept_}")
    return lr, dv


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
