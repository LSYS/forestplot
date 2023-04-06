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
    **kwargs: Any,
) -> Axes:
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
        **kwargs,
    )
    return _local_df, ax


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
    Preprocess the dataframe to be ready for plotting.

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
    **kwargs: Any,
) -> Axes:
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
    ax = mdraw_legend(models=models, modellabels=modellabels, ax=ax, xlabel=xlabel, **kwargs)

    format_xticks(
        dataframe=dataframe, estimate=estimate, ll=ll, hl=hl, xticks=xticks, ax=ax, **kwargs
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


def mdraw_ref_xline(
    ax: Axes,
    dataframe: pd.core.frame.DataFrame,
    model_col: str,
    annoteheaders: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    **kwargs: Any,
) -> Axes:
    """
    Draw the vertical reference xline at zero. Unless defaults are overridden in kwargs.

    Parameters
    ----------
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    xline = kwargs.get("xline", 0)
    if xline is not None:
        xlinestyle = kwargs.get("xlinestyle", "-")
        xlinecolor = kwargs.get("xlinecolor", ".2")
        xlinewidth = kwargs.get("xlinewidth", 1)

        if (annoteheaders is None) and (right_annoteheaders is None):
            _offset = 0.5
        else:
            _offset = 1.5
        models = dataframe[model_col].unique()
        _df = dataframe.query(f'{model_col}=="{models[-1]}"')
        ax.vlines(
            x=xline,
            ymin=-0.5,
            ymax=len(_df) - _offset,
            linestyle=xlinestyle,
            color=xlinecolor,
            linewidth=xlinewidth,
        )
    return ax


# =============================================================================================
# =============================================================================================
# =============================================================================================
def mdraw_yticklabels(
    dataframe: pd.core.frame.DataFrame,
    yticklabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    flush: bool,
    ax: Axes,
    **kwargs: Any,
) -> Axes:
    ax.set_yticks(range(len(dataframe)))

    fontfamily = kwargs.get("fontfamily", "monospace")
    fontsize = kwargs.get("fontsize", 12)
    if flush:
        ax.set_yticklabels(
            dataframe[yticklabel], fontfamily=fontfamily, fontsize=fontsize, ha="left"
        )
        yax = ax.get_yaxis()
        fig = plt.gcf()
        pad = max(
            T.label.get_window_extent(renderer=fig.canvas.get_renderer()).width
            for T in yax.majorTicks
        )
        yax.set_tick_params(pad=pad)
    else:
        ax.set_yticklabels(
            dataframe[yticklabel], fontfamily=fontfamily, fontsize=fontsize, ha="right"
        )
    return ax


def mdraw_est_markers(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    yticklabel: str,
    model_col: str,
    models: Sequence[str],
    ax: Axes,
    msymbols: Union[Sequence[str], None] = "soDx",
    mcolor: Union[Sequence[str], None] = ["0", "0.4", ".8", "0.2"],
    **kwargs: Any,
) -> Axes:
    """docstring"""
    markersize = kwargs.get("markersize", 40)
    n = len(models)
    offset = kwargs.get("offset", 0.3 - (n - 2) * 0.05)
    for ix, modelgroup in enumerate(models):
        _df = dataframe.query(f'{model_col}=="{modelgroup}"')
        base_y_vector = np.arange(len(_df)) - offset / 2 - (offset / 2) * (n - 2)
        _y = base_y_vector + (ix * offset)
        ax.scatter(y=_y, x=_df[estimate], marker=msymbols[ix], color=mcolor[ix], s=markersize)
    return ax


def mdraw_ci(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    yticklabel: str,
    ll: str,
    hl: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    logscale: bool,
    ax: Axes,
    mcolor: Union[Sequence[str], None] = ["0", "0.4", ".8", "0.2"],
    **kwargs: Any,
) -> Axes:
    """Docstring"""
    lw = kwargs.get("lw", 1.4)
    n = len(models)
    offset = kwargs.get("offset", 0.3 - (n - 2) * 0.05)

    for ix, modelgroup in enumerate(models):
        _df = dataframe.query(f'{model_col}=="{modelgroup}"')
        base_y_vector = np.arange(len(_df)) - offset / 2 - (offset / 2) * (n - 2)
        _y = base_y_vector + (ix * offset)

        ax.errorbar(
            x=_df[estimate],
            y=_y,
            xerr=[_df[estimate] - _df[ll], _df[hl] - _df[estimate]],
            ecolor=mcolor[ix],
            alpha=0.5,
            elinewidth=lw,
            ls="none",
            zorder=0,
        )
    if logscale:
        ax.set_xscale("log", base=10)
    return ax


from matplotlib.lines import Line2D


def mdraw_legend(
    ax: Axes,
    xlabel: Union[Sequence[str], None],
    modellabels: Optional[Union[Sequence[str], None]],
    msymbols: Union[Sequence[str], None] = "soDx",
    mcolor: Union[Sequence[str], None] = ["0", "0.4", ".8", "0.2"],
    **kwargs: Any,
) -> Axes:
    leg_markersize = kwargs.get("leg_markersize", 8)
    leg_artists = []
    for ix, symbol in enumerate(msymbols):
        leg_artists.append(
            Line2D([0], [0], marker=symbol, color=mcolor[ix], markersize=leg_markersize)
        )
    # Handle position of legend
    # bbox_to_anchor = kwargs.get("bbox_to_anchor", None)
    if len(modellabels) <= 2:
        bbox_y = -0.12
    else:
        bbox_y = -0.17
    if xlabel:
        bbox_y -= 0.04
    bbox_to_anchor = (0.5, bbox_y)
    bbox_to_anchor = kwargs.get("bbox_to_anchor", bbox_to_anchor)
    if bbox_to_anchor:
        leg_loc = kwargs.get("leg_loc", "lower center")
        leg_ncol = kwargs.get("leg_ncol", 2)
    else:
        leg_loc = kwargs.get("leg_loc", "best")
        leg_ncol = kwargs.get("leg_ncol", 1)
    leg_fontsize = kwargs.get("leg_fontsize", 12)
    ax.legend(
        leg_artists,
        modellabels,
        loc=leg_loc,
        handleheight=1,
        handlelength=3,
        handletextpad=0.5,
        frameon=True,
        ncol=leg_ncol,
        fontsize=leg_fontsize,
        bbox_to_anchor=bbox_to_anchor,
    )

    return ax


def mdraw_yticklabel2(
    dataframe: pd.core.frame.DataFrame,
    annoteheaders: Union[Sequence[str], None],
    right_annoteheaders: Union[Sequence[str], None],
    ax: Axes,
    **kwargs: Any,
) -> Axes:
    grouplab_fontweight = kwargs.get("grouplab_fontweight", "bold")
    fontfamily = kwargs.get("fontfamily", "monospace")
    fontsize = kwargs.get("fontsize", 12)

    top_row_ix = len(dataframe) - 1
    inv = ax.transData.inverted()
    righttext_width = 0
    fig = plt.gcf()
    extrapad = 0.03
    pad = ax.get_xlim()[1] * (1 + extrapad)
    for ix, row in dataframe.reset_index().iterrows():
        ticklabel = row["yticklabel2"]
        if (ix == top_row_ix) and (
            annoteheaders is not None or right_annoteheaders is not None
        ):
            t = ax.text(
                x=pad,
                y=ix,
                s=ticklabel,
                fontfamily=fontfamily,
                horizontalalignment="left",
                verticalalignment="center",
                fontweight=grouplab_fontweight,
                fontsize=fontsize,
            )
        else:
            t = ax.text(
                x=pad,
                y=ix,
                s=ticklabel,
                fontfamily=fontfamily,
                horizontalalignment="left",
                verticalalignment="center",
                fontsize=fontsize,
            )
        (_, _), (x1, _) = inv.transform(
            t.get_window_extent(renderer=fig.canvas.get_renderer())
        )
        righttext_width = max(righttext_width, x1)
    return ax, righttext_width
