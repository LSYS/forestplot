"""Holds functions to check data and validate arguments from users."""
import warnings
from typing import Optional, Sequence, Union

import pandas as pd
import pandas.api.types as ptypes


def check_data(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    groupvar: Optional[str] = None,
    group_order: Optional[Sequence] = None,
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    form_ci_report: bool = None,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    pval: Optional[str] = None,
    ylabel2: Optional[str] = None,
) -> pd.core.frame.DataFrame:
    """Check and validate that dataframe has the correct data. If data is missing, create them.

    Checks and validates key arguments.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    estimate (str)
            Name of column containing the estimates (e.g. pearson correlation coefficient,
            OR, regression estimates, etc.).
    varlabel (str)
            Name of column containing the variable label to be printed out.
    groupvar (str)
            Name of column containing group of variables.
    group_order (list-like)
            List of groups by order to report in the figure.
    ll (str)
            Name of column containing the lower limit of the confidence intervals.
    hl (str)
            Name of column containing the upper limit of the confidence intervals.
    form_ci_report (bool)
            If True, form the formatted confidence interval as a string.
    annote (list-like)
            List of columns to add as additional annotation in the plot.
    annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations.
    rightannote (list-like)
            List of columns to add as additional annotation on the right-hand side of the plot.
    right_annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations
            on the right-hand side of the plot.
    pval (str)
            Name of column containing the p-values.
    ylabel2 (str)
            Title of the right-hand side y-axis.

    Returns
    -------
            pd.core.frame.DataFrame.
    """
    ##########################################################################
    ## Check that CI options (ll, hl, form_ci_report) are consistent
    ##########################################################################
    if ll is None:
        try:
            assert hl is None
        except Exception:
            raise TypeError("'ll' is None. 'hl' should also be None.")

    if hl is None:
        try:
            assert ll is None
        except Exception:
            raise TypeError("'hl' is None. 'll' should also be None.")

    if ll is None and form_ci_report:
        warnings.warn("'ll' is None. 'form_ci_report' will be set to False.")

    ##########################################################################
    ## Check that numeric data are numeric
    ##########################################################################
    if not isinstance(dataframe, pd.core.frame.DataFrame):
        raise TypeError("Expect data as Pandas DataFrame")

    if not ptypes.is_numeric_dtype(dataframe[estimate]):
        try:
            dataframe[estimate] = dataframe[estimate].astype(float)
        except ValueError:
            raise TypeError("Estimates should be float or int")

    if (ll is not None) and (not ptypes.is_numeric_dtype(dataframe[ll])):
        try:
            dataframe[ll] = dataframe[ll].astype(float)
        except ValueError:
            raise TypeError("CI lowerlimit values should be float or int")

    if (hl is not None) and (not ptypes.is_numeric_dtype(dataframe[hl])):
        try:
            dataframe[hl] = dataframe[hl].astype(float)
        except ValueError:
            raise TypeError("CI higherlimit values should be float or int")

    ##########################################################################
    ## Check that the annotations and headers specified are list-like
    ##########################################################################
    if annote is not None:
        try:
            assert ptypes.is_list_like(annote)
        except Exception:
            raise TypeError("annote should be list-like.")

    if annoteheaders is not None:
        try:
            assert ptypes.is_list_like(annoteheaders)
        except Exception:
            raise TypeError("annoteheaders should be list-like.")

    if rightannote is not None:
        try:
            assert ptypes.is_list_like(rightannote)
        except Exception:
            raise TypeError("rightannote should be list-like.")

    if right_annoteheaders is not None:
        try:
            assert ptypes.is_list_like(right_annoteheaders)
        except Exception:
            raise TypeError("right_annoteheaders should be list-like.")

    ##########################################################################
    ## Check that annotations and corresponding headers have same length
    ##########################################################################
    if (annote is not None) & (annoteheaders is not None):
        check_iterables_samelen(annote, annoteheaders)

    if (rightannote is not None) & (right_annoteheaders is not None):
        check_iterables_samelen(rightannote, right_annoteheaders)

    ##########################################################################
    ## Check that specified annotations can be found in input or processed dataframe
    ##########################################################################
    acceptable_annotations = [  # from processed data
        "ci_range",
        "est_ci",
        "formatted_pval",
    ]

    if annote is not None:
        for col in annote:
            try:
                assert (col in dataframe.columns) or (col in acceptable_annotations)
            except Exception:
                raise AssertionError(f"the field {col} is not found in dataframe.")

    if rightannote is not None:
        for col in rightannote:
            try:
                assert (col in dataframe.columns) or (col in acceptable_annotations)
            except Exception:
                raise AssertionError(f"the field {col} is not found in dataframe.")

    if groupvar is not None:
        check_groups(dataframe, groupvar=groupvar, group_order=group_order)

    ##########################################################################
    ## Check that column names to add as annotations are provided if the
    ##   annotation headers are provided
    ##########################################################################
    if (annoteheaders is not None) and (annote is None):
        raise TypeError("Annotation headers are provided but no columns provided ('annote').")

    if (right_annoteheaders is not None) and (rightannote is None):
        raise TypeError(
            "Right annotation headers are provided but no columns provided ('rightannote')."
        )

    ##########################################################################
    ## Warnings
    ##########################################################################
    # Warn: Check that var itself is not in annote
    if (annote is not None) and (varlabel in annote):
        warnings.warn(
            f'{varlabel} is a variable is already printed. Specifying {varlabel} in "annote" will lead to duplicate printing of {varlabel}.'
        )

    if (rightannote is not None) and (varlabel in rightannote):
        warnings.warn(f"{varlabel} is a variable is already printed.")
        # warnings.warn(f'Specifying {varlabel} in "rightannote" will lead to duplicate printing of {varlabel}.')
        warnings.warn(
            f'{varlabel} is a variable is already printed. Specifying {varlabel} in "rightannote" will lead to duplicate printing of {varlabel}.'
        )

    if (annote is not None) and (rightannote is not None):
        if any(col in annote for col in rightannote):
            warnings.warn("Duplicates found in annote and rightannote.")

    # Overriding default to plot p-value on the right-hand side since rightannote is specified
    if (pval is not None) and (rightannote is not None):
        warnings.warn(
            "p-value will not be plotted in the right annotation column by default since rightannote is specificied."
        )

    # Warn: need to ignore ylabel2 if right_annote headers are specified
    if (ylabel2 is not None) and (right_annoteheaders is not None):
        warnings.warn("ylabel2 is ignored since right_annoteheaders is specified.")

    # Warn: duplicates found in varlabels and grouplabels
    if groupvar is not None:
        grouplabels = dataframe[groupvar].dropna().unique()
        grouplabels = [grplab_str.lower().strip() for grplab_str in grouplabels]
        varlabels = dataframe[varlabel].dropna().unique()
        varlabels = [varlab_str.lower().strip() for varlab_str in varlabels]
        if any(varlab_str in grouplabels for varlab_str in varlabels):
            warnings.warn(
                "Duplicates found in variable labels ('varlabel') and group labels ('groupvar'). Formatting of y-axis labels may lead to unexpected errors."
            )

    return dataframe


def check_iterables_samelen(*args):  # type: ignore
    """Assert that provided iterables have same length."""
    try:
        assert all(len(args[0]) == len(_arg) for _arg in args[1:])
    except Exception:
        raise ValueError("Iterables not of the same length.")
    return None


def check_groups(
    dataframe: pd.core.frame.DataFrame, groupvar: str, group_order: Optional[Sequence]
) -> None:
    """Check that provided group-related args are well-behaved.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
        Pandas DataFrame where rows are variables. Columns are variable name, estimates,
        margin of error, etc.
    groupvar (str)
        Name of column containing group of variables.
    group_order (list-like)
        List of groups by order to report in the figure.

    Returns
    -------
    None
    """
    if (group_order is not None) and (groupvar is None):
        raise TypeError(
            "Group ordering ('group_order') provided but no group column provided ('groupvar')."
        )
    # Check detected unique groups and group_order have same length
    groups: Sequence = dataframe[groupvar].dropna().unique()
    if group_order is not None:
        check_iterables_samelen(groups, group_order)
    # Check that groups in group_order exists
    if (group_order is not None) and (groupvar is not None):
        try:
            assert all(group in groups for group in group_order)
        except Exception:
            raise AssertionError("Groups specified in `group_order` should exist in the data.")
    return None
