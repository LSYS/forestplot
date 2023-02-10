from typing import Any, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

np.seterr(all="ignore")
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from pyforestplot.arg_validators import check_data
from pyforestplot.dataframe_utils import (
    insert_groups,
    reverse_dataframe,
    sort_data,
    sort_groups,
)
from pyforestplot.graph_utils import (
    despineplot,
    draw_alt_row_colors,
    draw_ci,
    draw_est_markers,
    draw_pval_right,
    draw_ref_xline,
    draw_tablelines,
    draw_xticks,
    draw_ylabel1,
    draw_yticklabel2,
    format_grouplabels,
    format_tableheader,
    format_xlabel,
    format_xticks,
    remove_ticks,
    right_flush_yticklabels,
)
from pyforestplot.text_utils import (
    form_est_ci,
    format_varlabels,
    indent_nongroupvar,
    make_tableheaders,
    normalize_varlabels,
    prep_annote,
    prep_rightannnote,
    star_pval,
)


def forestplot(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    moerror: Optional[str] = None,
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    form_ci_report: bool = True,
    ci_report: bool = True,
    groupvar: Optional[str] = None,
    group_order: Optional[Union[list, tuple]] = None,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    pval: Optional[str] = None,
    starpval: bool = True,
    sort: bool = False,
    sortby: Optional[str] = None,
    flush: bool = True,
    decimal_precision: int = 2,
    figsize: Union[Tuple, List] = (4, 8),
    xticks: Optional[Union[list, range]] = None,
    ylabel: Optional[str] = None,
    xlabel: Optional[str] = None,
    yticker2: Optional[str] = None,
    color_alt_rows: bool = False,
    return_df: bool = False,
    preprocess: bool = True,
    table: bool = False,
    **kwargs: Any,
) -> Axes:
    """
    Draw forest plot using the pandas dataframe provided.

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
    moerror (str)
            Name of column containing the margin of error in the confidence intervals.
            Should be available if 'll' and 'hl' are left empty.
    ll (str)
            Name of column containing the lower limit of the confidence intervals.
            Optional
    hl (str)
            Name of column containing the upper limit of the confidence intervals.
            Optional
    form_ci_report (bool)
            If True, form the formatted confidence interval as a string.
    ci_report (bool)
            If True, form the formatted confidence interval as a string.
    groupvar (str)
            Name of column containing group of variables.
    group_order (list-like)
            List of groups by order to report in the figure.
    annote (list-like)
            List of columns to add as additional annotation on the left-hand side of the plot.
    annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations
            on the left-hand side of the plot.
    rightannote (list-like)
            List of columns to add as additional annotation on the right-hand side of the plot.
    right_annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations
            on the right-hand side of the plot.
    pval (str)
            Name of column containing the p-values.
    starpval (bool)
            If True, use 'thresholds' and 'symbols' to "star" the p-values.
    sort (bool)
            If True, sort rows by estimate size
    sortby (str)
            Name of column to sort the dataframe by. Default is 'estimate'.
    flush (bool)
            Left-flush the variable labels.
    decimal_precision (int)
            Precision of 2 means we go from '0.1234' -> '0.12'.
    figsize (list-like):
            Figure size setting. E.g. (5,10) means width-to-height is 5 to 10.
            Size is for the dot-and-whisker plot region only. Does not control eventual
            figure size that comes from the length of the right and left y-axis ticker labels.
    xticks (list-like)
            List of xtickers to print on the x-axis.
    ylabel (str)
            Title of the left-hand side y-axis.
    xlabel (str)
            Title of the left-hand side x-axis.
    yticker2 (str)
            Name of column containing the second set of values to print on the right-hand side ytickers.
            If 'pval' is provided, then yticker2 will be set to the 'formatted_pval'.
    color_alt_rows (bool)
            If True, color alternative rows.
    preprocess (bool)
            If True, call the preprocess_dataframe() function to prepare the data for plotting.
    return_df (bool)
            If True, in addition to the Matplotlib Axes object, returns the intermediate dataframe
            created from preprocess_dataframe().
            A tuple of (preprocessed_dataframe, Ax) will be returned.

    Returns
    -------
            Matplotlib Axes object.
    """
    _local_df = dataframe.copy(deep=True)
    _local_df = check_data(
        dataframe=_local_df,
        estimate=estimate,
        varlabel=varlabel,
        moerror=moerror,
        pval=pval,
        ll=ll,
        hl=hl,
        groupvar=groupvar,
        group_order=group_order,
        annote=annote,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
    )
    if (ll is None) or (hl is None):
        ll, hl = "ll", "hl"
    if ci_report is True:
        form_ci_report = True
    if preprocess:
        _local_df = _preprocess_dataframe(
            dataframe=_local_df,
            estimate=estimate,
            varlabel=varlabel,
            moerror=moerror,
            ll=ll,
            hl=hl,
            form_ci_report=form_ci_report,
            ci_report=ci_report,
            groupvar=groupvar,
            group_order=group_order,
            annote=annote,
            annoteheaders=annoteheaders,
            rightannote=rightannote,
            right_annoteheaders=right_annoteheaders,
            pval=pval,
            starpval=starpval,
            sort=sort,
            sortby=sortby,
            flush=flush,
            decimal_precision=decimal_precision,
            **kwargs,
        )
    ax = _make_forestplot(
        dataframe=_local_df,
        yticklabel="yticklabel",
        estimate=estimate,
        moerror=moerror,
        groupvar=groupvar,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
        pval=pval,
        figsize=figsize,
        xticks=xticks,
        ll=ll,
        hl=hl,
        flush=flush,
        ylabel=ylabel,
        xlabel=xlabel,
        yticker2=yticker2,
        color_alt_rows=color_alt_rows,
        table=table,
        **kwargs,
    )
    return (_local_df, ax) if return_df else ax


def _preprocess_dataframe(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    moerror: Optional[str],
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    form_ci_report: Optional[bool] = False,
    ci_report: Optional[bool] = False,
    groupvar: Optional[str] = None,
    group_order: Optional[Union[list, tuple]] = None,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    pval: Optional[str] = None,
    starpval: bool = True,
    sort: bool = False,
    sortby: Optional[str] = None,
    sortascend: bool = True,
    flush: bool = True,
    decimal_precision: int = 2,
    **kwargs: Any,
) -> pd.core.frame.DataFrame:
    """
    Preprocess the dataframe to be ready for plotting.

    Returns
    -------
            pd.core.frame.DataFrame with additional columns for plotting.
    """
    if (groupvar is not None) and (group_order is not None):
        if sort is True:
            list(group_order).reverse()
        dataframe = sort_groups(dataframe, groupvar=groupvar, group_order=group_order)
    dataframe = sort_data(
        dataframe=dataframe,
        estimate=estimate,
        groupvar=groupvar,
        sort=sort,
        sortby=sortby,
        sortascend=sortascend,
    )
    if groupvar is not None:  # Make groups
        dataframe = normalize_varlabels(dataframe=dataframe, varlabel=groupvar)
        dataframe = insert_groups(dataframe=dataframe, groupvar=groupvar, varlabel=varlabel)
    dataframe = normalize_varlabels(dataframe=dataframe, varlabel=varlabel)
    dataframe = indent_nongroupvar(dataframe=dataframe, varlabel=varlabel, groupvar=groupvar)
    if form_ci_report:
        dataframe = form_est_ci(
            dataframe=dataframe,
            estimate=estimate,
            moerror=moerror,
            ll=ll,
            hl=hl,
            decimal_precision=decimal_precision,
        )
    dataframe = star_pval(
        dataframe=dataframe,
        pval=pval,
        starpval=starpval,
        decimal_precision=decimal_precision,
    )
    if annote is None:  # Form ytickers = formatted variable labels
        dataframe = format_varlabels(
            dataframe=dataframe,
            varlabel=varlabel,
            form_ci_report=form_ci_report,
            ci_report=ci_report,
            groupvar=groupvar,
        )
    else:
        dataframe = prep_annote(
            dataframe=dataframe,
            groupvar=groupvar,
            varlabel=varlabel,
            annote=annote,
            annoteheaders=annoteheaders,
            **kwargs,
        )
    if rightannote is not None:
        dataframe = prep_rightannnote(
            dataframe=dataframe,
            groupvar=groupvar,
            varlabel=varlabel,
            rightannote=rightannote,
            right_annoteheaders=right_annoteheaders,
        )
    dataframe = make_tableheaders(
        dataframe=dataframe,
        varlabel=varlabel,
        annote=annote,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
        **kwargs,
    )
    return reverse_dataframe(dataframe)  # since plotting starts from bottom


def _make_forestplot(
    dataframe: pd.core.frame.DataFrame,
    yticklabel: str,
    estimate: str,
    moerror: str,
    groupvar: str,
    pval: str,
    xticks: Optional[Union[list, range]],
    ll: str,
    hl: str,
    flush: bool,
    annoteheaders: Optional[Union[Sequence[str], None]],
    rightannote: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    ylabel: str,
    xlabel: str,
    yticker2: Optional[str],
    color_alt_rows: bool,
    figsize: Union[Tuple, List],
    despine: bool = True,
    table: bool = False,
    **kwargs: Any,
) -> Axes:
    """
    Draw the forest plot.

    Returns
    -------
            Matplotlib Axes object.
    """
    _, ax = plt.subplots(figsize=figsize, facecolor="white")
    if moerror is None:
        moerror = "moerror"
    ax = draw_ci(
        dataframe=dataframe,
        estimate=estimate,
        yticklabel=yticklabel,
        moerror=moerror,
        ax=ax,
        **kwargs,
    )
    draw_est_markers(
        dataframe=dataframe, estimate=estimate, yticklabel=yticklabel, ax=ax, **kwargs
    )
    format_xticks(dataframe=dataframe, ll=ll, hl=hl, xticks=xticks, ax=ax, **kwargs)
    draw_ref_xline(ax=ax, **kwargs)
    pad = right_flush_yticklabels(
        dataframe=dataframe, yticklabel=yticklabel, flush=flush, ax=ax, **kwargs
    )
    if rightannote is None:
        ax, righttext_width = draw_pval_right(
            dataframe=dataframe,
            pval=pval,
            annoteheaders=annoteheaders,
            rightannote=rightannote,
            yticklabel=yticklabel,
            yticker2=yticker2,
            pad=pad,
            ax=ax,
            **kwargs,
        )
    else:
        ax, righttext_width = draw_yticklabel2(dataframe=dataframe, ax=ax)
        # draw_yticklabel2(dataframe=dataframe, ax=ax)
        # pass

    draw_ylabel1(ylabel=ylabel, pad=pad, ax=ax, **kwargs)
    remove_ticks(ax)
    format_grouplabels(dataframe=dataframe, groupvar=groupvar, ax=ax, **kwargs)
    format_tableheader(
        annoteheaders=annoteheaders, right_annoteheaders=right_annoteheaders, ax=ax, **kwargs
    )
    despineplot(despine=despine, ax=ax)
    format_xlabel(xlabel=xlabel, ax=ax, **kwargs)
    if color_alt_rows:
        draw_alt_row_colors(
            dataframe,
            groupvar=groupvar,
            annoteheaders=annoteheaders,
            right_annoteheaders=right_annoteheaders,
            ax=ax,
        )
    if (annoteheaders is not None) or (
        (pval is not None) or (right_annoteheaders is not None)
    ):
        if table:
            draw_tablelines(
                dataframe=dataframe,
                righttext_width=righttext_width,
                pval=pval,
                right_annoteheaders=right_annoteheaders,
                ax=ax,
            )
    return ax


def insert_group_model(
    dataframe: pd.core.frame.DataFrame, groupvar: str, varlabel: str, model_col: str
) -> pd.core.frame.DataFrame:
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


from pyforestplot.dataframe_utils import insert_empty_row
from pyforestplot.text_utils import _get_max_varlen


def mforestplot(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]] = None,
    modellabels: Optional[Union[Sequence[str], None]] = None,
    moerror: Optional[str] = None,
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    groupvar: Optional[str] = None,
    group_order: Optional[Union[Sequence[str], None]] = None,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    flush: bool = True,
    decimal_precision: int = 2,
    figsize: Union[Tuple, List] = (4, 8),
    xticks: Optional[Union[list, range]] = None,
    ylabel: Optional[str] = None,
    xlabel: Optional[str] = None,
    yticker2: Optional[str] = None,
    color_alt_rows: bool = False,
    return_df: bool = False,
    preprocess: bool = True,
    **kwargs: Any,
) -> Axes:

    df = check_data(
        dataframe=dataframe,
        estimate=estimate,
        varlabel=varlabel,
        moerror=moerror,
        pval=None,
        ll=ll,
        hl=hl,
        annote=annote,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
    )

    if ll is None:
        ll, hl = "ll", "hl"

    if preprocess:
        df = _preprocess_multmodel_dataframe(
            dataframe=dataframe,
            estimate=estimate,
            varlabel=varlabel,
            moerror=moerror,
            model_col=model_col,
            models=models,
            ll=ll,
            hl=hl,
            groupvar=groupvar,
            annote=annote,
            annoteheaders=annoteheaders,
            rightannote=rightannote,
            right_annoteheaders=right_annoteheaders,
            flush=flush,
            decimal_precision=decimal_precision,
            **kwargs,
        )
    # return df, df
    ax = _make_mforestplot(
        dataframe=df,
        yticklabel="yticklabel",
        estimate=estimate,
        moerror=moerror,
        model_col=model_col,
        models=models,
        modellabels=modellabels,
        groupvar=groupvar,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
        figsize=figsize,
        xticks=xticks,
        ll=ll,
        hl=hl,
        flush=flush,
        ylabel=ylabel,
        xlabel=xlabel,
        yticker2=yticker2,
        color_alt_rows=color_alt_rows,
        **kwargs,
    )

    return df, ax


def _preprocess_multmodel_dataframe(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    moerror: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    ll: Optional[str],
    hl: Optional[str],
    groupvar: Optional[str],
    annote: Optional[Union[Sequence[str], None]],
    annoteheaders: Optional[Union[Sequence[str], None]],
    rightannote: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    flush: bool = True,
    decimal_precision: int = 2,
    **kwargs: Any,
) -> pd.core.frame.DataFrame:
    """
    Preprocess the dataframe to be ready for plotting.

    Returns
    -------
            pd.core.frame.DataFrame with additional columns for plotting.
    """
    if groupvar is not None:
        dataframe = insert_group_model(
            dataframe=dataframe, groupvar=groupvar, varlabel=varlabel, model_col=model_col
        )

    dataframe = normalize_varlabels(dataframe=dataframe, varlabel=varlabel)

    dataframe = indent_nongroupvar(dataframe=dataframe, varlabel=varlabel, groupvar=groupvar)

    if annote is None:  # Form ytickers = formatted variable labels
        dataframe = format_varlabels(
            dataframe=dataframe,
            varlabel=varlabel,
            form_ci_report=False,
            ci_report=False,
            groupvar=groupvar,
        )
    else:
        dataframe = prep_annote(
            dataframe=dataframe,
            groupvar=groupvar,
            varlabel=varlabel,
            annote=annote,
            annoteheaders=annoteheaders,
            **kwargs,
        )

    if rightannote is not None:
        dataframe = prep_rightannnote(
            dataframe=dataframe,
            groupvar=groupvar,
            varlabel=varlabel,
            rightannote=rightannote,
            right_annoteheaders=right_annoteheaders,
        )

    dataframe = make_multimodel_tableheaders(
        dataframe=dataframe,
        varlabel=varlabel,
        model_col=model_col,
        models=models,
        annote=annote,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
        flush=flush,
        **kwargs,
    )

    dataframe = reverse_dataframe(
        dataframe
    )  # Reverse the dataframe since plotting starts from bottom

    return dataframe


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
        dataframe = insert_headers_models(dataframe, model_col=model_col, models=models)
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


def insert_headers_models(
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


def _make_mforestplot(
    dataframe: pd.core.frame.DataFrame,
    yticklabel: str,
    estimate: str,
    moerror: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    modellabels: Optional[Union[Sequence[str], None]],
    groupvar: str,
    xticks: Optional[Union[list, range]],
    ll: str,
    hl: str,
    flush: bool,
    annoteheaders: Optional[Union[Sequence[str], None]],
    rightannote: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    ylabel: str,
    xlabel: str,
    yticker2: Optional[str],
    figsize: Union[Tuple, List],
    despine: bool = True,
    color_alt_rows: bool = False,
    **kwargs: Any,
) -> Axes:
    if moerror is None:
        moerror = "moerror"
    if models is None:
        models = dataframe[model_col].dropna().unique()
    if modellabels is None:
        modellabels = models

    _, ax = plt.subplots(figsize=figsize, facecolor="white")
    draw_multi_marker_ci(
        dataframe,
        estimate=estimate,
        yticklabel=yticklabel,
        model_col=model_col,
        models=models,
        modellabels=modellabels,
        moerror=moerror,
        ax=ax,
        **kwargs,
    )

    format_xticks(dataframe=dataframe, ll=ll, hl=hl, xticks=xticks, ax=ax)
    draw_ref_xline(ax=ax, **kwargs)

    df_subset = dataframe.query(f'{model_col}=="{models[-1]}"').reset_index(drop=True)
    if rightannote is not None:
        draw_yticklabel2_multmodel(df_subset, ax, **kwargs)
    remove_ticks(ax)
    format_grouplabels(dataframe=dataframe, groupvar=groupvar, ax=ax, **kwargs)
    # format_tableheader not working?
    format_tableheader(
        annoteheaders=annoteheaders, right_annoteheaders=right_annoteheaders, ax=ax, **kwargs
    )

    despineplot(despine=despine, ax=ax)

    format_xlabel(xlabel=xlabel, ax=ax, **kwargs)
    if color_alt_rows:
        draw_alt_row_colors(
            dataframe,
            groupvar=groupvar,
            annoteheaders=annoteheaders,
            right_annoteheaders=right_annoteheaders,
            ax=ax,
        )

    ax.set_ylim(-0.5, len(df_subset))
    return ax


from matplotlib.lines import Line2D


def draw_multi_marker_ci(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    yticklabel: str,
    model_col: str,
    models: Union[Sequence[str], None],
    modellabels: Union[Sequence[str], None],
    moerror: str,
    ax: Axes,
    msymbols: Union[Sequence[str], None] = "soD",
    mcolor: Union[Sequence[str], None] = ["0", "0.4", ".8"],
    offset: float = 0.3,
    **kwargs: Any,
) -> Tuple[Axes, pd.core.frame.DataFrame]:

    assert len(msymbols) == len(mcolor)
    assert len(msymbols) >= len(models)
    assert len(msymbols) >= len(modellabels)

    leg_fontsize = kwargs.get("leg_fontsize", 10)
    leg_loc = kwargs.get("leg_loc", "best")
    leg_markersize = kwargs.get("leg_markersize", 6)
    msize = kwargs.get("msize", 20)

    for ix, modelgroup in enumerate(models):
        _df = dataframe.query(f'{model_col}=="{modelgroup}"')

        base_y_vector = np.arange(len(_df)) - offset / 2
        _y = base_y_vector + (ix * offset)

        ax.barh(
            y=_y, xerr=_df[moerror], width=_df[estimate], error_kw=dict(lw=0.5), color="none"
        )
        ax.scatter(y=_y, x=_df[estimate], marker=msymbols[ix], color=mcolor[ix], s=msize)

    ax.set_yticks(range(len(_df)))

    leg_artists = []
    for ix, symbol in enumerate(msymbols):
        leg_artists.append(
            Line2D([0], [0], marker=symbol, color=mcolor[ix], markersize=leg_markersize)
        )
    ax.legend(
        leg_artists,
        modellabels,
        loc=leg_loc,
        handleheight=1,
        handlelength=3,
        handletextpad=0.5,
        frameon=True,
        ncol=1,
        fontsize=leg_fontsize,
    )

    return ax, _df


def draw_yticklabel2_multmodel(
    dataframe: pd.core.frame.DataFrame, ax: Axes, **kwargs: Any
) -> Axes:
    grouplab_size = kwargs.get("grouplab_size", 10)
    grouplab_fontweight = kwargs.get("grouplab_fontweight", "bold")

    group_row_ix = len(dataframe) - 1
    extrapad = 0.03
    pad = ax.get_xlim()[1] * (1 + extrapad)
    for ix, row in dataframe.reset_index().iterrows():
        ticklabel = row["yticklabel2"]
        if ix == group_row_ix:
            ax.text(
                x=pad,
                y=ix,
                s=ticklabel,
                fontfamily="monospace",
                horizontalalignment="left",
                verticalalignment="center",
                fontweight=grouplab_fontweight,
                fontsize=grouplab_size,
            )
        else:
            ax.text(
                x=pad,
                y=ix,
                s=ticklabel,
                fontfamily="monospace",
                horizontalalignment="left",
                verticalalignment="center",
            )
    return ax
