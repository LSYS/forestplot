import pytest
from pyforestplot.dataframe_utils import load_data
import pandas as pd


def test_load_data():
    df = load_data("mortality")
    assert isinstance(df, pd.DataFrame)

    # Assert casing does not matter
    df = load_data("Mortality")
    assert isinstance(df, pd.DataFrame)

    # Assert assertion will fail for names that don't exist
    dummy_name = "dummy_name"
    with pytest.raises(AssertionError) as excinfo:
        df = load_data(dummy_name)
    assert f"{dummy_name} not found." in str(excinfo.value)
