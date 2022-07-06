import pandas as pd
from pyforestplot.text_utils import (
    form_est_ci,
    star_pval,
    indent_nongroupvar,
    normalize_varlabels,
    _get_max_varlen,
    _right_justify_num,
    _remove_est_ci,
)
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal


def test_star_pval():
    # Test 1
    _df = pd.DataFrame({"pval": [0.0001, 0.040, 0.090, 0.500]})
    correct_df = pd.DataFrame({"formatted_pval": ["0.0***", "0.04**", "0.09*", "0.5"]})
    result_df = star_pval(_df, pval="pval", starpval=True, decimal_precision=2)
    assert_series_equal(result_df.formatted_pval, correct_df.formatted_pval)

    # Test 2
    _df = pd.DataFrame({"pval": [0.0011, 0.042, 0.091, 0.512]})
    correct_df = pd.DataFrame(
        {"formatted_pval": ["0.001***", "0.042**", "0.091*", "0.512"]}
    )
    result_df = star_pval(_df, pval="pval", starpval=True, decimal_precision=3)
    assert_series_equal(result_df.formatted_pval, correct_df.formatted_pval)


def test_get_max_varlen():
    _df = pd.DataFrame({"col": ["aa3", "aaa a6"]})
    assert _get_max_varlen(_df, varlabel="col", extrapad=0) == 6
    assert _get_max_varlen(_df, varlabel="col", extrapad=2) == 6 + 2


def test_right_justify_num():
    _df = pd.DataFrame({"col": [-0.123, 11.234, -12.0]})
    correct_df = pd.DataFrame({"formatted_col": [" -0.12", " 11.23", "-12.00"]})
    result_df = _right_justify_num(dataframe=_df, col="col", decimal_precision=2)
    assert_series_equal(result_df.formatted_col, correct_df.formatted_col)

    # deicmal precision = 3
    correct_df = pd.DataFrame({"formatted_col": [" -0.123", " 11.234", "-12.000"]})
    result_df = _right_justify_num(dataframe=_df, col="col", decimal_precision=3)
    assert_series_equal(result_df.formatted_col, correct_df.formatted_col)


def test_indent_nongroupvar():
    _df = pd.DataFrame({"col": ["row1", "row2"]})

    # No indent
    correct_df = _df
    result_df = indent_nongroupvar(_df, varlabel="col", groupvar=None, varindent=0)
    assert_frame_equal(result_df, correct_df)

    # Indent zero spaces when no groupvar
    result_df = indent_nongroupvar(_df, varlabel="col", groupvar=None, varindent=2)
    assert_frame_equal(result_df, correct_df)

    # Indent one space
    _df = pd.DataFrame({"col": ["row1", "row2"], "groupvar": ["group1", "group1"]})
    correct_df = pd.DataFrame(
        {"col": [" row1", " row2"], "groupvar": ["group1", "group1"]}
    )
    result_df = indent_nongroupvar(
        _df, varlabel="col", groupvar="groupvar", varindent=1
    )
    assert_frame_equal(result_df, correct_df)


def test_normalize_varlabels():
    _df = pd.DataFrame({"col": ["row number 1", "row number 2"]})

    # No capitalize
    correct_df = _df
    result_df = normalize_varlabels(_df, varlabel="col", capitalize=None)
    assert_frame_equal(result_df, correct_df)

    # Capitalize (default)
    correct_df = pd.DataFrame({"col": ["Row number 1", "Row number 2"]})
    result_df = normalize_varlabels(_df, varlabel="col")
    assert_frame_equal(result_df, correct_df)

    # title
    correct_df = pd.DataFrame({"col": ["Row Number 1", "Row Number 2"]})
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="title")
    assert_frame_equal(result_df, correct_df)

    # lower
    correct_df = pd.DataFrame({"col": ["row number 1", "row number 2"]})
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="lower")
    assert_frame_equal(result_df, correct_df)

    # upper
    correct_df = pd.DataFrame({"col": ["ROW NUMBER 1", "ROW NUMBER 2"]})
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="upper")
    assert_frame_equal(result_df, correct_df)


def test_remove_est_ci():
    _df = pd.DataFrame(
        {
            "var": ["group1", "var1", "var2"],
            "groupvar": ["group1", "group1", "group1"],
            "ci_range": ["nan", "ci_range", "ci_range"],
            "est_ci": ["nan", "est_ci", "est_ci"],
        }
    )
    correct_df = pd.DataFrame(
        {
            "var": ["group1", "var1", "var2"],
            "groupvar": ["group1", "group1", "group1"],
            "ci_range": ["", "ci_range", "ci_range"],
            "est_ci": ["", "est_ci", "est_ci"],
        }
    )
    result_df = _remove_est_ci(_df, varlabel="var", groupvar="groupvar")
    assert_frame_equal(result_df, correct_df)


def test_form_est_ci():
    _df = pd.DataFrame({"estimate": [1, 2], "ll": [1, 2], "hl": [1, 2]})
    correct_df = pd.DataFrame(
        {
            "estimate": [1, 2],
            "ll": [1, 2],
            "hl": [1, 2],
            "formatted_estimate": ["1.00", "2.00"],
            "formatted_ll": ["1.00", "2.00"],
            "formatted_hl": ["1.00", "2.00"],
            "ci_range": ["(1.00 to 1.00)", "(2.00 to 2.00)"],
            "est_ci": ["1.00(1.00 to 1.00)", "2.00(2.00 to 2.00)"],
        }
    )
    result_df = form_est_ci(
        _df, estimate="estimate", moerror=None, ll="ll", hl="hl", decimal_precision=2
    )
    assert_frame_equal(result_df, correct_df)
