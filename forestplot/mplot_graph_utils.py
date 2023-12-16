from typing import Any, List, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
from matplotlib.pyplot import Axes


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


def mdraw_yticklabels(
    dataframe: pd.core.frame.DataFrame,
    yticklabel: str,
    flush: bool,
    ax: Axes,
    **kwargs: Any,
) -> Axes:
    """
    Set custom y-axis tick labels on a matplotlib Axes object using the yticklabel column in the provided
    pandas dataframe.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        The pandas DataFrame from which the y-axis tick labels are derived.
    yticklabel : str
        Column name in the DataFrame whose values are used as y-axis tick labels.
    flush : bool
        If True, aligns y-axis tick labels to the left with adjusted padding to prevent overlap. 
        If False, aligns labels to the right.
    ax : Axes
        The matplotlib Axes object to be modified.
    **kwargs : Any
        Additional keyword arguments for customizing the appearance of the tick labels.
        Supported customizations include 'fontfamily' (default 'monospace') and 'fontsize' (default 12).

    Returns
    -------
    Axes
        The modified matplotlib Axes object with updated y-axis tick labels.
    """
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
