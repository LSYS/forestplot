"""Main functions for coefficient plots (coefplots) of multiple regression models."""
from typing import Any, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

np.seterr(all="ignore")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.pyplot import Axes

from forestplot.arg_validators import check_data
from forestplot.dataframe_utils import reverse_dataframe, sort_groups
from forestplot.graph_utils import (  # draw_ci,; draw_est_markers,; draw_pval_right,; draw_ref_xline,; draw_ylabel1,; draw_yticklabel2,; right_flush_yticklabels,
    despineplot,
    draw_alt_row_colors,
    draw_tablelines,
    format_grouplabels,
    format_tableheader,
    format_xlabel,
    format_xticks,
    remove_ticks,
)
from forestplot.mplot_dataframe_utils import insert_group_model, make_multimodel_tableheaders
from forestplot.mplot_graph_utils import (
    mdraw_ci,
    mdraw_est_markers,
    mdraw_legend,
    mdraw_ref_xline,
    mdraw_yticklabel2,
    mdraw_yticklabels,
)
from forestplot.text_utils import (  # form_est_ci,; make_tableheaders,; star_pval,
    format_varlabels,
    indent_nongroupvar,
    normalize_varlabels,
    prep_annote,
    prep_rightannnote,
)

rcParams["font.monospace"] = [
    "Lucida Sans Typewriter",
    "DejaVu Sans Mono",
    "Courier New",
    "Lucida Console",
]


def mforestplot(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]] = None,
    modellabels: Optional[Union[Sequence[str], None]] = None,
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    groupvar: Optional[str] = None,
    group_order: Optional[Union[list, tuple]] = None,
    logscale: bool = False,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    pval: Optional[str] = None,
    capitalize: Optional[str] = None,
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
    legend: bool = True,
    xlim: Optional[Union[Tuple, List]] = None,
    **kwargs: Any,
) -> Axes:
    """
    Generate a forest plot from a DataFrame using Matplotlib.

    This function creates a forest plot, which is useful for displaying the estimates from different models
    or groups, along with their confidence intervals. It provides a range of customization options for the plot,
    including sorting, annotations, and visual style.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        The DataFrame containing the data to be plotted.
    estimate : str
        The name of the column in the DataFrame that contains the estimate values.
    varlabel : str
        The name of the column used for variable labels on the y-axis.
    model_col : str
        The name of the column that categorizes data into different models or groups.
    models : Optional[Sequence[str]]
        The list of models to include in the plot. If None, all models in model_col are used.
    modellabels : Optional[Sequence[str]]
        Labels for the models, used in the plot legend. If None, model names are used as labels.
    ll : Optional[str]
        The name of the column representing the lower limit of the confidence intervals.
    hl : Optional[str]
        The name of the column representing the upper limit of the confidence intervals.
    groupvar: Optional[str] = None
        The name of the column used for grouping the variables. If specified, it allows the plot to visually
        distinguish between different groups of variables.
    group_order: Optional[Union[list, tuple]] = None
        Specifies the order in which groups (as defined by `groupvar`) should be displayed in the plot.
        If None, the groups are displayed in the order they appear in the DataFrame.
    logscale: bool = False
        If True, the x-axis will be log-scaled. Useful for variables that span several orders of magnitude.
    annote: Optional[Union[Sequence[str], None]] = None
        A list of column names in the DataFrame that contain additional annotations for each variable.
    annoteheaders: Optional[Union[Sequence[str], None]] = None
        Headers for the annotation columns. If None, the column names specified in `annote` are used as headers.
    rightannote: Optional[Union[Sequence[str], None]] = None
        A list of column names for annotations that should be placed on the right side of the plot.
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None
        Headers for the right-side annotation columns.
    pval: Optional[str] = None
        The name of the column containing p-values for each estimate. Used for displaying statistical significance.
    capitalize: Optional[str] = None
        Column name for which the text should be capitalized.
    starpval: bool = True
        If True, display stars (*) next to estimates to indicate statistical significance based on p-values.
    sort: bool = False
        If True, the variables will be sorted based on the `sortby` parameter.
    sortby: Optional[str] = None
        Column name to sort the variables by. Only relevant if `sort` is True.
    flush: bool = True
        If True, aligns all the estimates along a vertical line for better visual comparison.
    decimal_precision: int = 2
        The number of decimal places for numeric values displayed in the plot.
    figsize: Union[Tuple, List] = (4, 8)
        Size of the plot specified as (width, height) in inches.
    xticks: Optional[Union[list, range]] = None
        Custom x-axis tick values. If None, Matplotlib's default ticks are used.
    ylabel: Optional[str] = None
        Label for the y-axis. If None, no label is displayed.
    xlabel: Optional[str] = None
        Label for the x-axis. If None, no label is displayed.
    yticker2: Optional[str] = None
        Secondary y-axis tick labels, if applicable.
    color_alt_rows: bool = False
        If True, alternate rows will have different background colors for better readability.
    return_df: bool = False
        If True, returns the processed DataFrame along with the Axes object.
    preprocess: bool = True
        If True, performs preprocessing on the DataFrame before plotting.
    table: bool = False
        If True, displays a table at the bottom of the plot with variable names and their corresponding estimates.
    legend: bool = True
        If True, displays a legend for the models or groups.
    xlim: Optional[Union[Tuple, List]] = None
        Custom limits for the x-axis. Specified as (xmin, xmax).
    **kwargs: Any
        Additional keyword arguments to pass to Matplotlib plotting functions.

    Returns
    -------
    Tuple
        A tuple containing a modified DataFrame (if return_df is True) and the matplotlib Axes object
        with the forest plot.

    Notes
    -----
    - The function is highly customizable with several optional parameters to adjust the appearance and functionality
      of the plot.
    - If `return_df` is True, the function also returns the DataFrame after preprocessing and sorting based on the
      specified parameters.
    - The `preprocess` parameter controls whether the input DataFrame should be preprocessed before plotting.
    """
    _local_df = dataframe.copy(deep=True)
    _local_df = check_data(
        dataframe=_local_df,
        estimate=estimate,
        varlabel=varlabel,
        pval=None,
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
    if preprocess:
        _local_df = _mpreprocess_dataframe(
            dataframe=_local_df,
            estimate=estimate,
            varlabel=varlabel,
            ll=ll,
            hl=hl,
            model_col=model_col,
            models=models,
            capitalize=capitalize,
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
    ax = _make_mforestplot(
        dataframe=_local_df,
        yticklabel="yticklabel",
        estimate=estimate,
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
        logscale=logscale,
        flush=flush,
        ylabel=ylabel,
        xlabel=xlabel,
        yticker2=yticker2,
        color_alt_rows=color_alt_rows,
        table=table,
        legend=legend,
        xlim=xlim,
        **kwargs,
    )
    if return_df:
        return _local_df, ax
    else:
        return ax


def _mpreprocess_dataframe(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    ll: Optional[str],
    hl: Optional[str],
    groupvar: Optional[str] = None,
    group_order: Optional[Union[list, tuple]] = None,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    capitalize: Optional[str] = None,
    flush: bool = True,
    decimal_precision: int = 2,
    **kwargs: Any,
) -> pd.core.frame.DataFrame:
    """
    Preprocess the dataframe to be ready for plotting in the `mforestplot` function.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        The DataFrame containing the data to be plotted.
    estimate : str
        The name of the column in the DataFrame that contains the estimate values.
    varlabel : str
        The name of the column used for variable labels on the y-axis.
    model_col : str
        The name of the column that categorizes data into different models or groups.
    models : Optional[Union[Sequence[str], None]]
        The list of models to include in the plot. If None, all models in model_col are used.
    ll : Optional[str]
        The name of the column representing the lower limit of the confidence intervals.
    hl : Optional[str]
        The name of the column representing the upper limit of the confidence intervals.
    groupvar : Optional[str]
        The name of the column used for grouping the variables. If provided, the DataFrame will be sorted and/or
        grouped based on this column.
    group_order : Optional[Union[list, tuple]]
        The order in which to display the groups defined by `groupvar`. This affects the sorting of the DataFrame.
    annote : Optional[Union[Sequence[str], None]]
        A list of column names in the DataFrame that contain additional annotations for each variable.
    annoteheaders : Optional[Union[Sequence[str], None]]
        Headers for the annotation columns. If None, the column names specified in `annote` are used as headers.
    rightannote : Optional[Union[Sequence[str], None]]
        A list of column names for annotations that should be placed on the right side of the plot.
    right_annoteheaders : Optional[Union[Sequence[str], None]]
        Headers for the right-side annotation columns.
    capitalize : Optional[str]
        Column name for which the text should be capitalized.
    flush : bool
        If True, aligns all the estimates along a vertical line for better visual comparison.
    decimal_precision : int
        The number of decimal places for numeric values in the DataFrame.
    **kwargs : Any
        Additional keyword arguments that might be used in other preprocessing steps.

    Returns
    -------
    pd.core.frame.DataFrame
        Dataframe with additional columns for plotting.
    """
    if groupvar is not None:
        dataframe = sort_groups(dataframe, groupvar=groupvar, group_order=group_order)
        dataframe = insert_group_model(
            dataframe=dataframe, groupvar=groupvar, varlabel=varlabel, model_col=model_col
        )

    dataframe = normalize_varlabels(
        dataframe=dataframe, varlabel=varlabel, capitalize=capitalize
    )

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
    return reverse_dataframe(dataframe)  # since plotting starts from bottom


def _make_mforestplot(
    dataframe: pd.core.frame.DataFrame,
    yticklabel: str,
    estimate: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    modellabels: Optional[Union[Sequence[str], None]],
    groupvar: str,
    xticks: Optional[Union[list, range]],
    ll: str,
    hl: str,
    logscale: bool,
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
    table: bool = False,
    legend: bool = True,
    xlim: Optional[Union[Tuple, List]] = None,
    **kwargs: Any,
) -> Axes:
    """
    Constructs a forest plot from a preprocessed DataFrame.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        The DataFrame containing the data to be plotted.
    yticklabel : str
        The name of the column used for y-axis tick labels.
    estimate : str
        The name of the column in the DataFrame that contains the estimate values.
    model_col : str
        The name of the column that categorizes data into different models or groups.
    models : Optional[Union[Sequence[str], None]]
        The list of models to include in the plot. If None, all models in model_col are used.
    modellabels : Optional[Union[Sequence[str], None]]
        Labels for the models, used in the plot legend. If None, model names are used as labels.
    groupvar : str
        The name of the column used for grouping the variables.
    xticks : Optional[Union[list, range]]
        Custom x-axis tick values. If None, Matplotlib's default ticks are used.
    ll : str
        The name of the column representing the lower limit of the confidence intervals.
    hl : str
        The name of the column representing the upper limit of the confidence intervals.
    logscale : bool
        If True, the x-axis will be log-scaled.
    flush : bool
        If True, aligns all the estimates along a vertical line for better visual comparison.
    annoteheaders : Optional[Union[Sequence[str], None]]
        Headers for the annotation columns.
    rightannote : Optional[Union[Sequence[str], None]]
        A list of column names for annotations to be placed on the right side of the plot.
    right_annoteheaders : Optional[Union[Sequence[str], None]]
        Headers for the right-side annotation columns.
    ylabel : str
        Label for the y-axis.
    xlabel : str
        Label for the x-axis.
    yticker2 : Optional[str]
        Secondary y-axis tick labels, if applicable.
    figsize : Union[Tuple, List]
        Size of the plot specified as (width, height) in inches.
    despine : bool
        If True, removes the top and right spines from the plot.
    color_alt_rows : bool
        If True, alternate rows will have different background colors for better readability.
    table : bool
        If True, displays a table at the bottom of the plot with variable names and their corresponding estimates.
    legend : bool
        If True, displays a legend for the models or groups.
    xlim : Optional[Union[Tuple, List]]
        Custom limits for the x-axis. Specified as (xmin, xmax).
    **kwargs : Any
        Additional keyword arguments to pass to plotting functions.

    Returns
    -------
    Axes
        A Matplotlib Axes object containing the forest plot.
    """
    if models is None:
        models = dataframe[model_col].dropna().unique()
    if modellabels is None:
        modellabels = models

    _, ax = plt.subplots(figsize=figsize, facecolor="white")

    ax = mdraw_est_markers(
        dataframe,
        estimate=estimate,
        yticklabel=yticklabel,
        model_col=model_col,
        models=models,
        ax=ax,
        **kwargs,
    )
    ax = mdraw_ci(
        dataframe,
        estimate=estimate,
        yticklabel=yticklabel,
        ll=ll,
        hl=hl,
        model_col=model_col,
        models=models,
        logscale=logscale,
        ax=ax,
        **kwargs,
    )
    if legend:
        ax = mdraw_legend(
            models=models, modellabels=modellabels, ax=ax, xlabel=xlabel, **kwargs
        )

    format_xticks(
        dataframe=dataframe,
        estimate=estimate,
        ll=ll,
        hl=hl,
        xticks=xticks,
        xlim=xlim,
        ax=ax,
        **kwargs,
    )
    mdraw_ref_xline(
        ax=ax,
        dataframe=dataframe,
        model_col=model_col,
        annoteheaders=annoteheaders,
        right_annoteheaders=right_annoteheaders,
        **kwargs,
    )
    df_subset = dataframe.query(f'{model_col}=="{models[-1]}"').reset_index(drop=True)
    mdraw_yticklabels(
        df_subset,
        yticklabel=yticklabel,
        model_col=model_col,
        models=models,
        flush=flush,
        ax=ax,
        **kwargs,
    )
    if rightannote is not None:
        ax, righttext_width = mdraw_yticklabel2(
            df_subset,
            annoteheaders=annoteheaders,
            right_annoteheaders=right_annoteheaders,
            ax=ax,
            **kwargs,
        )
    else:
        righttext_width = 0
    remove_ticks(ax)
    format_grouplabels(dataframe=dataframe, groupvar=groupvar, ax=ax, **kwargs)
    format_tableheader(
        annoteheaders=annoteheaders, right_annoteheaders=right_annoteheaders, ax=ax, **kwargs
    )

    format_xlabel(xlabel=xlabel, ax=ax, **kwargs)
    if color_alt_rows:
        draw_alt_row_colors(
            dataframe,
            groupvar=groupvar,
            annoteheaders=annoteheaders,
            right_annoteheaders=right_annoteheaders,
            ax=ax,
        )
    if (annoteheaders is not None) or (right_annoteheaders is not None):
        if table:
            draw_tablelines(
                dataframe=df_subset,
                righttext_width=righttext_width,
                pval=None,
                right_annoteheaders=right_annoteheaders,
                ax=ax,
                extrapad=0.03,  # To tune where the right tablelines start
                **kwargs,
            )
    if annoteheaders or right_annoteheaders:
        negative_padding = 1.0
    else:
        negative_padding = 0.5
    ax.set_ylim(-0.5, ax.get_ylim()[1] - negative_padding)
    despineplot(despine=despine, ax=ax)

    return ax
