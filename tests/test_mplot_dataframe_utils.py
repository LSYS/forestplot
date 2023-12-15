import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from forestplot.mplot_dataframe_utils import (
    _insert_headers_models,
    insert_group_model,
    make_multimodel_tableheaders,
)


def test_insert_group_model():
    # Setup test data
    data = {
        "model_col": ["Model1", "Model1", "Model2", "Model2"],
        "groupvar": ["GroupA", "GroupB", "GroupA", "GroupB"],
        "value": [10, 20, 30, 40],
    }
    df = pd.DataFrame(data)

    # Expected output
    expected_data = {
        "varlabel": ["GroupA", None, "GroupB", None, "GroupA", None, "GroupB", None],
        "groupvar": [
            "GroupA",
            "GroupA",
            "GroupB",
            "GroupB",
            "GroupA",
            "GroupA",
            "GroupB",
            "GroupB",
        ],
        "model_col": [
            "Model1",
            "Model1",
            "Model1",
            "Model1",
            "Model2",
            "Model2",
            "Model2",
            "Model2",
        ],
        "value": [None, 10, None, 20, None, 30, None, 40],
    }
    expected_df = pd.DataFrame(expected_data)

    # Apply the function
    result_df = insert_group_model(df, "groupvar", "varlabel", "model_col")

    # Assert
    assert_frame_equal(result_df, expected_df)


def test_insert_headers_models():
    # Setup
    df = pd.DataFrame(
        {
            "model_col": ["model1", "model1", "model2", "model2"],
            "data1": [100, 200, 300, 400],
        }
    )

    # Expected output
    expected_output = pd.DataFrame(
        {
            "model_col": [None, "model1", "model1", None, "model2", "model2"],
            "data1": [None, 100, 200, None, 300, 400],
        }
    )

    # Exercise
    result = _insert_headers_models(df, "model_col", None)

    # Verify
    assert_frame_equal(
        result.reset_index(drop=True), expected_output.reset_index(drop=True)
    )


def test_make_multimodel_tableheaders():
    # Setup
    df_input = pd.DataFrame(
        {
            "var": ["var0", "var1", "var2", "var3", "var0", "var1", "var2", "var3"],
            "group": [
                "Group 0",
                "Group 0",
                "Group 1",
                "Group 1",
                "Group 0",
                "Group 0",
                "Group 1",
                "Group 1",
            ],
            "model": [
                "Model 0",
                "Model 0",
                "Model 0",
                "Model 0",
                "Model 1",
                "Model 1",
                "Model 1",
                "Model 1",
            ],
            "coef": [
                "Coef 0",
                "Coef 1",
                "Coef 2",
                "Coef 3",
                "Coef 4",
                "Coef 5",
                "Coef 6",
                "Coef 7",
            ],
        }
    )

    # Expected output
    df_expected = pd.DataFrame(
        {
            "var": [
                np.nan,
                "var0",
                "var1",
                "var2",
                "var3",
                np.nan,
                "var0",
                "var1",
                "var2",
                "var3",
            ],
            "group": [
                np.nan,
                "Group 0",
                "Group 0",
                "Group 1",
                "Group 1",
                np.nan,
                "Group 0",
                "Group 0",
                "Group 1",
                "Group 1",
            ],
            "model": [
                "Model 0",
                "Model 0",
                "Model 0",
                "Model 0",
                "Model 0",
                "Model 1",
                "Model 1",
                "Model 1",
                "Model 1",
                "Model 1",
            ],
            "coef": [
                np.nan,
                "Coef 0",
                "Coef 1",
                "Coef 2",
                "Coef 3",
                np.nan,
                "Coef 4",
                "Coef 5",
                "Coef 6",
                "Coef 7",
            ],
            "yticklabel": [
                "Variable  header",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "Variable  header",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
            ],
            "yticklabel2": [
                "",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
            ],
        }
    )

    # Exercise
    df_result = make_multimodel_tableheaders(
        df_input,
        varlabel="var",
        model_col="model",
        models=None,
        annote=["var"],
        annoteheaders=["header"],
        rightannote=None,
        right_annoteheaders=None,
    )
    # Verify
    # assert_frame_equal(df_result, df_expected)
    pd.testing.assert_frame_equal(df_result.iloc[:, :4], df_expected.iloc[:, :4])
