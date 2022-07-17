import pytest
from pyforestplot.dataframe_utils import (
    load_data,
    insert_groups,
    sort_groups,
    sort_data,
    reverse_dataframe,
    insert_empty_row,
)
import pandas as pd
import numpy as np
from pandas.testing import assert_series_equal
from pandas.testing import assert_frame_equal


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


def test_insert_groups():
    input_df = pd.DataFrame({"varlabel": ["var1", "var2"], "groupvar": ["group1", "group1"]})
    correct_df = pd.DataFrame(
        {"groupvar": ["group1", "group1", "group1"], "varlabel": ["group1", "var1", "var2"],}
    )
    result_df = insert_groups(input_df, groupvar="groupvar", varlabel="varlabel")
    # assert_frame_equal(result_df, correct_df)
    assert_series_equal(result_df["groupvar"], correct_df["groupvar"])
    assert_series_equal(result_df["varlabel"], correct_df["varlabel"])


def test_sort_data():
    input_string = ["c", "a", "b"]
    input_numeric = [3, -1, 2]

    output_string = ["c", "b", "a"]
    output_numeric = [3, 2, -1]

    # Vanilla sort
    input_df = pd.DataFrame({"estimate": input_numeric, "groupvar": input_string})
    correct_df = pd.DataFrame({"estimate": output_numeric, "groupvar": output_string})
    result_df = sort_data(input_df, estimate="estimate", groupvar="groupvar", sort=True)
    assert_frame_equal(result_df, correct_df)

    # Sort by another column (not 'estimate') without having to set 'sort' to True
    input_df = pd.DataFrame(
        {"estimate": input_numeric, "sortval": input_numeric, "groupvar": input_string}
    )
    correct_df = pd.DataFrame(
        {"estimate": output_numeric, "sortval": output_numeric, "groupvar": output_string,}
    )
    result_df = sort_data(input_df, estimate="estimate", groupvar="groupvar", sortby="sortval")
    assert_frame_equal(result_df, correct_df)

    # No sorting
    result_df = sort_data(input_df, estimate="estimate", groupvar="groupvar")
    assert_frame_equal(result_df, input_df)


def test_reverse_dataframe():
    input_string = ["a", "b", "c"]
    input_numeric = [-1, 2, 3]

    output_string = input_string[::-1]
    output_numeric = input_numeric[::-1]

    input_df = pd.DataFrame({"estimate": input_numeric, "varlabel": input_string})
    correct_df = pd.DataFrame({"estimate": output_numeric, "varlabel": output_string})
    result_df = reverse_dataframe(input_df)
    assert_frame_equal(result_df, correct_df)


def test_insert_empty_row():
    input_string = ["a", "b", "c"]
    input_numeric = [-1, 2, 3]
    input_df = pd.DataFrame({"estimate": input_numeric, "varlabel": input_string})
    result_df = insert_empty_row(input_df)
    assert len(result_df) == 1 + len(input_df)
    assert np.isnan(result_df.loc[0, "estimate"])
    assert np.isnan(result_df.loc[0, "varlabel"])


def test_sort_groups():
    input_string = ["a", "b", "c"]
    input_numeric = [-1, 2, 3]
    group = ["g1", "g2", "g1"]
    input_df = pd.DataFrame(
        {"estimate": input_numeric, "varlabel": input_string, "group": group}
    )
    correct_df = pd.DataFrame(
        {"estimate": input_numeric, "varlabel": input_string, "group": ["g1", "g1", "g2"]}
    )

    result_df = sort_groups(input_df, groupvar="group", group_order=["g1", "g2"])
    assert_frame_equal(result_df, input_df)

    # another test
    correct_df = pd.DataFrame(
        {"estimate": input_numeric, "varlabel": input_string, "group": ["g2", "g1", "g1"]}
    )
    result_df = sort_groups(input_df, groupvar="group", group_order=["g2", "g1"])
    assert_frame_equal(result_df, input_df)
