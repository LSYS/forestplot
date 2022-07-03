import pytest
from pyforestplot.arg_validators import check_data
import pandas as pd


def test_check_data():
    # Assert assertion for wrong data type works
    with pytest.raises(TypeError) as excinfo:
        check_data(dataframe="string", estimate="null", varlabel="null")
    assert str(excinfo.value) == "Expect data as Pandas DataFrame"

    numeric_as_string = ["-1", "2", "3.0"]
    string = ["a", "b", "c"]
    numeric = [-1, 2, 3.0]

    # Assert that assertion for numeric type for estimate works
    _df = pd.DataFrame({"estimate": string})
    with pytest.raises(TypeError) as excinfo:
        check_data(dataframe=_df, estimate="estimate", varlabel="estimate")
    assert str(excinfo.value) == "Estimates should be float or int"

    # Assert that conversion for numeric estimate stored as string works
    _df = pd.DataFrame({"estimate": numeric_as_string, "moerror": numeric})
    check_data(
        dataframe=_df, estimate="estimate", varlabel="estimate", moerror="moerror"
    )

    # Assert that assertion for numeric type for moerror works
    _df = pd.DataFrame({"estimate": numeric, "moerror": string})
    with pytest.raises(TypeError) as excinfo:
        check_data(
            dataframe=_df, estimate="estimate", varlabel="estimate", moerror="moerror"
        )
    assert str(excinfo.value) == "Margin of error values should be float or int"

    # Assert that conversion for numeric moerror stored as string works
    _df = pd.DataFrame({"estimate": numeric_as_string, "moerror": numeric_as_string})
    check_data(
        dataframe=_df, estimate="estimate", varlabel="estimate", moerror="moerror"
    )

    # Assert that assertion for numeric type for ll works
    _df = pd.DataFrame({"estimate": numeric, "ll": string})
    with pytest.raises(TypeError) as excinfo:
        check_data(dataframe=_df, estimate="estimate", varlabel="estimate", ll="ll")
    assert str(excinfo.value) == "CI lowerlimit values should be float or int"

    # Assert that conversion for numeric ll stored as string works
    _df = pd.DataFrame(
        {
            "estimate": numeric_as_string,
            "ll": numeric_as_string,
            "hl": numeric_as_string,
        }
    )
    check_data(
        dataframe=_df, estimate="estimate", varlabel="estimate", ll="ll", hl="hl"
    )

    # Assert that assertion for numeric type for hl works
    _df = pd.DataFrame({"estimate": numeric, "hl": string})
    with pytest.raises(TypeError) as excinfo:
        check_data(dataframe=_df, estimate="estimate", varlabel="estimate", hl="hl")
    assert str(excinfo.value) == "CI higherlimit values should be float or int"

    # Assert that conversion for numeric hl stored as string works
    _df = pd.DataFrame(
        {
            "estimate": numeric_as_string,
            "ll": numeric_as_string,
            "hl": numeric_as_string,
        }
    )
    check_data(
        dataframe=_df, estimate="estimate", varlabel="estimate", ll="ll", hl="hl"
    )

    # Assert assertion that either moerror or (ll and hl) is specified works
    with pytest.raises(AssertionError) as excinfo:
        check_data(dataframe=_df, estimate="estimate", varlabel="estimate")
    assert (
        str(excinfo.value)
        == 'If "moerror" is not provided, then "ll" and "hl" must be provided.'
    )

    ##########################################################################
    ## Check that column creation works
    ##########################################################################
    # Assert moerror is created if ll and hl specified
    _df = pd.DataFrame(
        {
            "estimate": numeric_as_string,
            "ll": numeric_as_string,
            "hl": numeric_as_string,
        }
    )
    processed_df = check_data(
        dataframe=_df, estimate="estimate", varlabel="estimate", ll="ll", hl="hl"
    )
    assert "moerror" in processed_df

    # Assert ll and hl is created if only moerror specified
    _df = pd.DataFrame({"estimate": numeric_as_string, "moerror": numeric_as_string,})
    processed_df = check_data(
        dataframe=_df, estimate="estimate", varlabel="estimate", moerror="moerror"
    )
    assert set(["ll", "hl"]).issubset(processed_df.columns)

    ##########################################################################
    ## Check annote
    ##########################################################################
    # Assert assertion that addannote and annoteheader is same length works
    _df = pd.DataFrame({"estimate": numeric_as_string, "moerror": numeric})
    with pytest.raises(AssertionError) as excinfo:
        check_data(
            dataframe=_df,
            estimate="estimate",
            varlabel="estimate",
            moerror="moerror",
            addannote=["col1", "col2"],
            annoteheaders=["header1"],
        )
    assert str(excinfo.value) == "addannote and annoteheaders should have same length."

    # No errors if addannote can be found in dataframe columns
    processed_df = check_data(
        dataframe=_df,
        estimate="estimate",
        varlabel="estimate",
        moerror="moerror",
        addannote=["moerror"],
    )

    # Raise error if addannote cannot be found in dataframe columns
    with pytest.raises(AssertionError) as excinfo:
        processed_df = check_data(
            dataframe=_df,
            estimate="estimate",
            varlabel="estimate",
            moerror="moerror",
            addannote=["dummy"],
        )
    assert str(excinfo.value) == "the field dummy is not found in dataframe."

    # Confirm no exception if annotation has column not in dataframe, but is found
    # processed dataframe (eg 'ci_range')
    processed_df = check_data(
        dataframe=_df,
        estimate="estimate",
        varlabel="moerror",
        moerror="moerror",
        addannote=["ci_range"],
    )

    ##########################################################################
    ## Check rightannote
    ##########################################################################
    # Assert assertion that rightannote and right_annoteheaders is same length works
    _df = pd.DataFrame({"estimate": numeric_as_string, "moerror": numeric})
    with pytest.raises(AssertionError) as excinfo:
        check_data(
            dataframe=_df,
            estimate="estimate",
            varlabel="estimate",
            moerror="moerror",
            rightannote=["col1", "col2"],
            right_annoteheaders=["header1"],
        )
    assert (
        str(excinfo.value)
        == "rightannote and right_annoteheaders should have same length."
    )

    # No errors if rightannote can be found in dataframe columns
    processed_df = check_data(
        dataframe=_df,
        estimate="estimate",
        varlabel="estimate",
        moerror="moerror",
        rightannote=["moerror"],
    )

    # Raise error if rightannote cannot be found in dataframe columns
    with pytest.raises(AssertionError) as excinfo:
        processed_df = check_data(
            dataframe=_df,
            estimate="estimate",
            varlabel="estimate",
            moerror="moerror",
            rightannote=["dummy"],
        )
    assert str(excinfo.value) == "the field dummy is not found in dataframe."

    # Confirm no exception if annotation has column not in dataframe, but is found
    # processed dataframe (eg 'ci_range')
    processed_df = check_data(
        dataframe=_df,
        estimate="estimate",
        varlabel="moerror",
        moerror="moerror",
        rightannote=["ci_range"],
    )
