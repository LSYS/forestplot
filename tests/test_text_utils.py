import pytest
import pandas as pd
import numpy as np
from pyforestplot.text_utils import (
    form_est_ci,
    star_pval,
    indent_nongroupvar,
    normalize_varlabels,
    format_varlabels,
    prep_annote,
    prep_rightannnote,
    make_tableheaders,
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
    correct_df = pd.DataFrame({"formatted_pval": ["0.001***", "0.042**", "0.091*", "0.512"]})
    result_df = star_pval(_df, pval="pval", starpval=True, decimal_precision=3)
    assert_series_equal(result_df.formatted_pval, correct_df.formatted_pval)

    # Assert assertion that  P-value thresholds and symbols list must be of same length works
    with pytest.raises(Exception) as excinfo:
        star_pval(
            _df,
            pval="pval",
            starpval=True,
            decimal_precision=3,
            thresholds=(0.01, 0.05, 0.1),
            symbols=("a", "b"),
        )
    assert str(excinfo.value) == "Iterables not of the same length."

    # Assert things work when pval is empty
    _df = pd.DataFrame({"pval": [0.0001, np.nan, 0.090, 0.500]})
    correct_df = pd.DataFrame({"formatted_pval": ["0.0***", "", "0.09*", "0.5"]})
    result_df = star_pval(_df, pval="pval", starpval=True, decimal_precision=2)
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
    result_df = indent_nongroupvar(_df, varlabel="col", groupvar="col", varindent=0)
    assert_frame_equal(result_df, correct_df)

    # Indent zero spaces when no groupvar
    result_df = indent_nongroupvar(_df, varlabel="col", groupvar="col", varindent=2)
    assert_frame_equal(result_df, correct_df)

    # Indent one space
    _df = pd.DataFrame({"col": ["row1", "row2"], "groupvar": ["group1", "group1"]})
    correct_df = pd.DataFrame({"col": [" row1", " row2"], "groupvar": ["group1", "group1"]})
    result_df = indent_nongroupvar(_df, varlabel="col", groupvar="groupvar", varindent=1)
    assert_frame_equal(result_df, correct_df)


def test_normalize_varlabels():
    lowercase_lst = ["row number 1", "row number 2"]
    _df = pd.DataFrame({"col": lowercase_lst})
    uppercase_lst = ["ROW NUMBER 1", "ROW NUMBER 2"]

    # No capitalize
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="lower")
    assert_frame_equal(result_df, _df)

    # Capitalize (default)
    correct_df = pd.DataFrame({"col": ["Row number 1", "Row number 2"]})
    result_df = normalize_varlabels(_df, varlabel="col")
    assert_frame_equal(result_df, correct_df)

    # title
    correct_df = pd.DataFrame({"col": ["Row Number 1", "Row Number 2"]})
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="title")
    assert_frame_equal(result_df, correct_df)

    # lower
    correct_df = pd.DataFrame({"col": lowercase_lst})
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="lower")
    assert_frame_equal(result_df, correct_df)

    # upper
    correct_df = pd.DataFrame({"col": uppercase_lst})
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="upper")
    assert_frame_equal(result_df, correct_df)

    # swapcase
    correct_df = pd.DataFrame({"col": uppercase_lst})
    _df = pd.DataFrame({"col": lowercase_lst})
    result_df = normalize_varlabels(_df, varlabel="col", capitalize="swapcase")
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
    numeric = [1, 2]
    _df = pd.DataFrame({"estimate": numeric, "ll": numeric, "hl": numeric})
    ci_lst = ["1.00", "2.00"]
    correct_df = pd.DataFrame(
        {
            "estimate": numeric,
            "ll": numeric,
            "hl": numeric,
            "formatted_estimate": ci_lst,
            "formatted_ll": ci_lst,
            "formatted_hl": ci_lst,
            "ci_range": ["(1.00 to 1.00)", "(2.00 to 2.00)"],
            "est_ci": ["1.00(1.00 to 1.00)", "2.00(2.00 to 2.00)"],
        }
    )
    result_df = form_est_ci(
        _df, estimate="estimate", moerror=None, ll="ll", hl="hl", decimal_precision=2
    )
    assert_frame_equal(result_df, correct_df)


def test_format_varlabels():
    ci_range = ["(1.00 to 1.00)", "(2.00 to 2.00)", "(3.00 to 3.00)"]
    var = ["var1", "var2", "var3"]
    numeric = [1, 2, 3]
    sringfloat = ["1.00", "2.00", "3.00"]
    est_ci = [
        "1.00(1.00 to 1.00)",
        "2.00(2.00 to 2.00)",
        "3.00(3.00 to 3.00)",
    ]
    ci_range_grp = ["", "(2.00 to 2.00)", "(3.00 to 3.00)"]
    info = ["a", "b", "c"]
    input_df = pd.DataFrame(
        {
            "var": var,
            "estimate": numeric,
            "ll": numeric,
            "hl": numeric,
            "info": info,
            "formatted_estimate": sringfloat,
            "formatted_ll": sringfloat,
            "formatted_hl": sringfloat,
            "ci_range": ci_range,
            "est_ci": est_ci,
        }
    )

    # Test that no groups and no string annotation (column2) works
    correct_df = pd.DataFrame(
        {
            "var": var,
            "estimate": numeric,
            "ll": numeric,
            "hl": numeric,
            "info": info,
            "formatted_estimate": sringfloat,
            "formatted_ll": sringfloat,
            "formatted_hl": sringfloat,
            "ci_range": ci_range,
            "est_ci": est_ci,
            "yticklabel": [
                "var1  1.00(1.00 to 1.00)",
                "var2  2.00(2.00 to 2.00)",
                "var3  3.00(3.00 to 3.00)",
            ],
        }
    )
    result_df = format_varlabels(
        input_df, varlabel="var", form_ci_report=True, ci_report=True, groupvar=None
    )
    assert_frame_equal(result_df, correct_df)

    # Test that groups with no string annotation works
    var = ["group", "var1", "var2"]
    groupvar = ["group", "group", "group"]
    est_ci = ["", "2.00(2.00 to 2.00)", "3.00(3.00 to 3.00)"]
    input_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "ll": numeric,
            "hl": numeric,
            "formatted_estimate": sringfloat,
            "formatted_ll": sringfloat,
            "formatted_hl": sringfloat,
            "info": info,
            "ci_range": ci_range,
            "est_ci": est_ci,
        }
    )
    correct_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "ll": numeric,
            "hl": numeric,
            "formatted_estimate": sringfloat,
            "formatted_ll": sringfloat,
            "formatted_hl": sringfloat,
            "info": info,
            "ci_range": ci_range_grp,
            "est_ci": est_ci,
            "yticklabel": ["group", "var1   2.00(2.00 to 2.00)", "var2   3.00(3.00 to 3.00)",],
        }
    )
    result_df = format_varlabels(
        input_df, varlabel="var", form_ci_report=True, ci_report=True, groupvar="groupvar",
    )
    assert_frame_equal(result_df, correct_df)

    # Test that ci_report=False option works (yticklabel should just be varlabel)
    correct_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "ll": numeric,
            "hl": numeric,
            "formatted_estimate": sringfloat,
            "formatted_ll": sringfloat,
            "formatted_hl": sringfloat,
            "info": info,
            "ci_range": ci_range_grp,
            "est_ci": est_ci,
            "yticklabel": var,
        }
    )
    result_df = format_varlabels(
        input_df, varlabel="var", form_ci_report=False, ci_report=False, groupvar="groupvar",
    )
    assert_frame_equal(result_df, correct_df)

    # Test that ci_report=False option works (yticklabel should just be varlabel) even when form_ci_report=True
    correct_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "ll": numeric,
            "hl": numeric,
            "formatted_estimate": sringfloat,
            "formatted_ll": sringfloat,
            "formatted_hl": sringfloat,
            "info": info,
            "ci_range": ci_range_grp,
            "est_ci": est_ci,
            "yticklabel": var,
        }
    )
    result_df = format_varlabels(
        input_df, varlabel="var", form_ci_report=True, ci_report=False, groupvar="groupvar",
    )
    assert_frame_equal(result_df, correct_df)


def test_prep_annote():
    # Assert things work when there is group exists
    numeric = [1, 2, 3]
    info = ["a", "b", "c"]
    var = ["group", "var1", "var2"]
    groupvar = ["group", "group", "group"]
    formatted_info = ["a   ", "b   ", "c   "]
    input_df = pd.DataFrame(
        {"var": var, "groupvar": groupvar, "estimate": numeric, "info": info,}
    )
    correct_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "info": info,
            "formatted_info": formatted_info,
            "yticklabel": ["group", "var1   b   ", "var2   c   "],
        }
    )
    result_df = prep_annote(
        input_df, annote=["info"], annoteheaders=["info"], varlabel="var", groupvar="groupvar",
    )
    assert_frame_equal(result_df, correct_df)

    # Assert things work when there is no group
    correct_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "info": info,
            "formatted_info": formatted_info,
            "yticklabel": ["group  a   ", "var1   b   ", "var2   c   "],
        }
    )
    result_df = prep_annote(
        input_df, annote=["info"], annoteheaders=["info"], varlabel="var", groupvar=None
    )
    assert_frame_equal(result_df, correct_df)


def test_prep_rightannote():
    # Assert things work when there is group exists
    numeric = [1, 2, 3]
    info = ["a", "b", "c"]
    var = ["group", "var1", "var2"]
    groupvar = ["group", "group", "group"]
    formatted_info = ["a   ", "b   ", "c   "]
    input_df = pd.DataFrame(
        {"var": var, "groupvar": groupvar, "estimate": numeric, "info": info,}
    )
    correct_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "info": info,
            "formatted_info": formatted_info,
            "yticklabel2": formatted_info,
        }
    )
    result_df = prep_rightannnote(
        input_df,
        rightannote=["info"],
        right_annoteheaders=["info"],
        varlabel="var",
        groupvar=None,
    )
    assert_frame_equal(result_df, correct_df)

    correct_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": groupvar,
            "estimate": numeric,
            "info": info,
            "formatted_info": formatted_info,
            "yticklabel2": ["", "b   ", "c   "],
        }
    )
    result_df = prep_rightannnote(
        input_df,
        rightannote=["info"],
        right_annoteheaders=["info"],
        varlabel="var",
        groupvar="groupvar",
    )
    assert_frame_equal(result_df, correct_df)


def test_make_tableheaders():
    var = ["group", "var1", "var2"]
    input_df = pd.DataFrame(
        {
            "var": var,
            "groupvar": ["group", "group", "group"],
            "estimate": [1, 2, 3],
            "info": ["a", "b", "c"],
            "fomatted_info": ["a   ", "b   ", "c   "],
            "yticklabel": ["group", "var1  b", "var2  c"],
            "yticklabel2": ["", "b   ", "c   "],
        }
    )
    correct_df = pd.DataFrame(
        {
            "var": [np.nan, "group", "var1", "var2"],
            "groupvar": [np.nan, "group", "group", "group"],
            "estimate": [np.nan, 1, 2, 3],
            "info": [np.nan, "a", "b", "c"],
            "fomatted_info": [np.nan, "a   ", "b   ", "c   "],
            "yticklabel": ["Variable  left head", "group", "var1  b", "var2  c"],
            "yticklabel2": ["right head", "", "b   ", "c   "],
        }
    )
    result_df = make_tableheaders(
        input_df,
        varlabel="var",
        annote=["info"],
        annoteheaders=["left head"],
        rightannote=["info"],
        right_annoteheaders=["right head"],
        groupvar="groupvar",
    )
    assert len(result_df) == 1 + len(input_df)
    assert_frame_equal(result_df, correct_df)

    # Assert things work if no headers specified
    result_df = make_tableheaders(
        input_df,
        varlabel="var",
        annote=["info"],
        annoteheaders=None,
        rightannote=["info"],
        right_annoteheaders=None,
        groupvar="groupvar",
    )
    assert len(result_df) == len(input_df)
    assert_frame_equal(result_df, input_df)

    # Assert things work if no rightheaders specified
    correct_df = pd.DataFrame(
        {
            "var": [np.nan, "group", "var1", "var2"],
            "groupvar": [np.nan, "group", "group", "group"],
            "estimate": [np.nan, 1, 2, 3],
            "info": [np.nan, "a", "b", "c"],
            "fomatted_info": [np.nan, "a   ", "b   ", "c   "],
            "yticklabel": ["Variable  left head", "group", "var1  b", "var2  c"],
            "yticklabel2": ["", "", "b   ", "c   "],
        }
    )
    result_df = make_tableheaders(
        input_df,
        varlabel="var",
        annote=["info"],
        annoteheaders=["left head"],
        rightannote=["info"],
        right_annoteheaders=None,
        groupvar="groupvar",
    )
    assert len(result_df) == 1 + len(input_df)
    assert_frame_equal(result_df, correct_df)

    # Assert things work if no leftheaders specified
    correct_df = pd.DataFrame(
        {
            "var": [np.nan, "group", "var1", "var2"],
            "groupvar": [np.nan, "group", "group", "group"],
            "estimate": [np.nan, 1, 2, 3],
            "info": [np.nan, "a", "b", "c"],
            "fomatted_info": [np.nan, "a   ", "b   ", "c   "],
            "yticklabel": ["Variable", "group", "var1  b", "var2  c"],
            "yticklabel2": ["right head", "", "b   ", "c   "],
        }
    )
    result_df = make_tableheaders(
        input_df,
        varlabel="var",
        annote=["info"],
        annoteheaders=None,
        rightannote=["info"],
        right_annoteheaders=["right head"],
        groupvar="groupvar",
    )
    assert len(result_df) == 1 + len(input_df)
    assert_frame_equal(result_df, correct_df)
