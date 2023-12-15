from typing import Any, List, Optional, Sequence, Tuple, Union

import pandas as pd

from forestplot.dataframe_utils import insert_empty_row
from forestplot.text_utils import _get_max_varlen


def insert_group_model(
    dataframe: pd.core.frame.DataFrame, groupvar: str, varlabel: str, model_col: str
) -> pd.core.frame.DataFrame:
    """
    Inserts rows for group labels into a pandas DataFrame based on specified model groupings.

    This function iterates over unique values in the 'model_col' and 'groupvar' columns of the input DataFrame.
    For each unique combination of model and group, it inserts a new row with the group label.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        The DataFrame into which the group labels will be inserted.
    groupvar : str
        The name of the column in 'dataframe' that contains the grouping variable.
    varlabel : str
        The label to assign to the inserted group label rows.
    model_col : str
        The name of the column in 'dataframe' that contains the model variable.

    Returns
    -------
    pd.core.frame.DataFrame
        A new DataFrame with additional rows inserted that contain the group labels for each group and model
        combination.
    """
    models = dataframe[model_col].unique()
    groups = dataframe[groupvar].unique()

    df_groupmodel_asvar = pd.DataFrame()
    for model in models:
        for group in groups:
            _df = dataframe.query(f"{model_col}==@model and {groupvar}==@group")
            addgroupvar = pd.DataFrame(
                {varlabel: [group], groupvar: [group], model_col: [model]}
            )
            df_groupmodel_asvar = pd.concat(
                [df_groupmodel_asvar, addgroupvar, _df], ignore_index=True
            )
    return df_groupmodel_asvar


def _insert_headers_models(
    dataframe: pd.core.frame.DataFrame, model_col: str, models: Union[Sequence[str], None]
) -> pd.core.frame.DataFrame:
    """
    Inserts an empty row as a header for each unique model in a pandas DataFrame.

    This function iterates over a specified list of models or, if not provided, over the unique values in the 'model_col' column of the input DataFrame. For each model, it filters the DataFrame to include only the rows corresponding to that model, inserts an empty row at the beginning, and then concatenates these modified DataFrames.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        The DataFrame into which the headers (empty rows) will be inserted.
    model_col : str
        The name of the column in 'dataframe' that contains the model identifiers.
    models : Union[Sequence[str], None], optional
        A sequence of model identifiers for which headers are to be inserted. If None, headers are inserted for all unique values in the 'model_col' column.

    Returns
    -------
    pd.core.frame.DataFrame
        A new DataFrame with empty rows inserted as headers for each specified model.

    Notes
    -----
    The function relies on an external function `insert_empty_row` to insert the empty rows. Ensure this function is defined and properly handles the insertion of empty rows into a DataFrame.
    """
    if models is None:
        models = dataframe[model_col].unique()

    df = pd.DataFrame()
    for model in models:
        _df = dataframe.query(f"{model_col}==@model")
        _df = insert_empty_row(_df)
        df = pd.concat([df, _df], ignore_index=True)
    return df


def make_multimodel_tableheaders(
    dataframe: pd.core.frame.DataFrame,
    varlabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    annote: Optional[Union[Sequence[str], None]],
    annoteheaders: Optional[Union[Sequence[str], None]],
    rightannote: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    flush: bool = True,
    **kwargs: Any,
) -> pd.core.frame.DataFrame:
    """Make additional column for table headers taking in account models and groups.

    This function is designed to prepare a pandas DataFrame for tabular display or plotting, especially
    when the data is categorized by different models. It adds additional columns for table headers,
    considering various models, groups, and annotations.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        The DataFrame to be processed and enhanced.
    varlabel : str
        The label of a key column in the DataFrame to be used in header formatting.
    model_col : str
        The column name in the DataFrame that contains model identifiers.
    models : Optional[Sequence[str]], optional
        A sequence of model identifiers. If None, the function uses unique values from 'model_col'.
    annote : Optional[Sequence[str]], optional
        A sequence of columns in the DataFrame to be used for left-side annotations.
    annoteheaders : Optional[Sequence[str]], optional
        Headers corresponding to 'annote', for left-side annotations.
    rightannote : Optional[Sequence[str]], optional
        A sequence of columns in the DataFrame to be used for right-side annotations.
    right_annoteheaders : Optional[Sequence[str]], optional
        Headers corresponding to 'rightannote', for right-side annotations.
    flush : bool, default True
        Determines if headers should be left-aligned (flushed). If False, headers are aligned as per their natural alignment.
    **kwargs : Any
        Additional keyword arguments. Includes 'variable_header' for the main variable header and
        'col_spacing' for spacing between columns.

    Returns
    -------
    pd.core.frame.DataFrame
        A modified DataFrame with additional columns and headers, formatted for plotting or tabular display.

    Notes
    -----
    This function relies on external functions '_insert_headers_models' and '_get_max_varlen'.
    """
    # No table headers
    variable_header = kwargs.get("variable_header", "")
    if (variable_header == "") or (variable_header is None):
        if (annoteheaders is None) and (right_annoteheaders is None):
            return dataframe
    col_spacing = kwargs.get("col_spacing", 2)
    spacing = "".ljust(col_spacing)

    # Get the pads
    pad = _get_max_varlen(dataframe=dataframe, varlabel=varlabel, extrapad=0)
    variable_header = kwargs.get("variable_header", "Variable")
    if flush:
        left_headers = variable_header.ljust(pad)
    else:
        left_headers = variable_header

    # Insert the rows
    if (annoteheaders is not None) or (right_annoteheaders is not None):
        dataframe = _insert_headers_models(dataframe, model_col=model_col, models=models)
        # return dataframe
        # pass  # function to insert the rows

    # Get the indexes where models start
    if models is None:
        models = dataframe[model_col].dropna().unique()
    indices = [0]  # init
    for ix, model in enumerate(models):
        if ix == len(models) - 1:
            break
        else:
            _next_index = indices[-1] + 1 + (ix + 1 * dataframe[varlabel].nunique())
            indices.append(_next_index)

    # Prep the headers
    if annoteheaders is not None:
        for ix, header in enumerate(annoteheaders):
            corresponding_col = annote[ix]
            pad = _get_max_varlen(dataframe=dataframe, varlabel=corresponding_col, extrapad=0)
            pad = max(pad, len(header))
            left_headers = spacing.join([left_headers, header.ljust(pad)])
    if right_annoteheaders is not None:
        right_headers = ""
        for ix, header in enumerate(right_annoteheaders):
            corresponding_col = rightannote[ix]
            # get max length for variables
            pad = _get_max_varlen(dataframe=dataframe, varlabel=corresponding_col, extrapad=0)
            pad = max(pad, len(header))
            if right_headers == "":
                right_headers = header.ljust(pad)
            else:
                right_headers = spacing.join([right_headers, header.ljust(pad)])
    else:
        right_headers = ""

    # Fill in the na
    c = 0
    for ix in indices:
        dataframe.loc[ix, "yticklabel"], dataframe.loc[ix, "yticklabel2"] = (
            left_headers,
            right_headers,
        )
        dataframe.loc[ix, "model"] = models[c]
        c += 1

    return dataframe
