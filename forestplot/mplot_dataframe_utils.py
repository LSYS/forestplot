from typing import Any, List, Optional, Sequence, Tuple, Union

import pandas as pd


def insert_group_model(
    dataframe: pd.core.frame.DataFrame, groupvar: str, varlabel: str, model_col: str
) -> pd.core.frame.DataFrame:
    """Insert rows for group labels taking into account model groupings.

    Returns
    -------
    pd.core.frame.DataFrame
        Dataframe with additional columns for plotting.
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


from forestplot.dataframe_utils import insert_empty_row
from forestplot.text_utils import _get_max_varlen


def _insert_headers_models(
    dataframe: pd.core.frame.DataFrame, model_col: str, models: Union[Sequence[str], None]
) -> pd.core.frame.DataFrame:
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

    Returns
    -------
    pd.core.frame.DataFrame
        Dataframe with additional columns for plotting.
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
