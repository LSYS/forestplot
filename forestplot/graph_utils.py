"""Holds functions to draw the plot."""
import warnings
from typing import Any, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import Axes

warnings.filterwarnings("ignore")


def draw_ci(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    yticklabel: str,
    ll: str,
    hl: str,
    logscale: bool,
    ax: Axes,
    **kwargs: Any
) -> Axes:
    """
    Draw the confidence intervals using the Matplotlib errorbar API.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    estimate (str)
            Name of column containing the estimates (e.g. pearson correlation coefficient,
            OR, regression estimates, etc.).
    yticklabel (str)
            Name of column in intermediate dataframe containing the formatted yticklabels.
    ll (str)
            Name of column containing the lower limit of the confidence intervals.
    hl (str)
            Name of column containing the upper limit of the confidence intervals.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    lw = kwargs.get("lw", 1.4)
    linecolor = kwargs.get("linecolor", ".6")
    ax.errorbar(
        x=dataframe[estimate],
        y=dataframe[yticklabel],
        xerr=[dataframe[estimate] - dataframe[ll], dataframe[hl] - dataframe[estimate]],
        ecolor=linecolor,
        elinewidth=lw,
        ls="none",
        zorder=0,
    )
    if logscale:
        ax.set_xscale("log", base=10)
    return ax


def draw_est_markers(
    dataframe: pd.core.frame.DataFrame, estimate: str, yticklabel: str, ax: Axes, **kwargs: Any
) -> Axes:
    """
    Draws the markers of the estimates using the Matplotlib plt.scatter API.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    estimate (str)
            Name of column containing the estimates (e.g. pearson correlation coefficient,
            OR, regression estimates, etc.).
    yticklabel (str)
            Name of column in intermediate dataframe containing the formatted yticklabels.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    marker = kwargs.get("marker", "s")
    markersize = kwargs.get("markersize", 40)
    markercolor = kwargs.get("markercolor", "darkslategray")
    markeralpha = kwargs.get("markeralpha", 0.8)
    ax.scatter(
        y=yticklabel,
        x=estimate,
        data=dataframe,
        marker=marker,
        s=markersize,
        color=markercolor,
        alpha=markeralpha,
    )
    return ax


def draw_ref_xline(
    ax: Axes,
    dataframe: pd.core.frame.DataFrame,
    annoteheaders: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    **kwargs: Any
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
        ax.vlines(
            x=xline,
            ymin=-0.5,
            ymax=len(dataframe) - _offset,
            linestyle=xlinestyle,
            color=xlinecolor,
            linewidth=xlinewidth,
        )
    return ax


def right_flush_yticklabels(
    dataframe: pd.core.frame.DataFrame, yticklabel: str, flush: bool, ax: Axes, **kwargs: Any
) -> float:
    """Flushes the formatted ytickers to the left. Also returns the amount of max padding in the window width.

    Padding to be used for drawing the 2nd yticklabels and ylabels.
    My reference: https://stackoverflow.com/questions/15882249/matplotlib-aligning-y-ticks-to-the-left

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    yticklabel (str)
            Name of column in intermediate dataframe containing the formatted yticklabels.
    flush (bool)
            Left-flush the variable labels.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Window wdith of figure (float)
    """
    fontfamily = kwargs.get("fontfamily", "monospace")
    fontsize = kwargs.get("fontsize", 12)
    # plt.draw()
    fig = plt.gcf()
    if flush:
        ax.set_yticklabels(
            dataframe[yticklabel], fontfamily=fontfamily, fontsize=fontsize, ha="left"
        )
    else:
        ax.set_yticklabels(
            dataframe[yticklabel], fontfamily=fontfamily, fontsize=fontsize, ha="right"
        )
    yax = ax.get_yaxis()
    pad = max(
        T.label.get_window_extent(renderer=fig.canvas.get_renderer()).width
        for T in yax.majorTicks
    )
    if flush:
        yax.set_tick_params(pad=pad)

    return pad


def draw_pval_right(
    dataframe: pd.core.frame.DataFrame,
    pval: str,
    annoteheaders: Optional[Union[Sequence[str], None]],
    yticklabel: str,
    pad: float,
    ax: Axes,
    **kwargs: Any
) -> Tuple[Axes, float]:
    """
    Draws the 2nd ytick labels on the right-hand side of the figure.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    pval (str)
            Name of column containing the p-values.
    annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations.
    yticklabel (str)
            Name of column in intermediate dataframe containing the formatted yticklabels.
    pad (float)
            Window wdith of figure
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    if pval is not None:
        inv = ax.transData.inverted()
        righttext_width = 0
        fig = plt.gcf()
        for _, row in dataframe.iterrows():
            yticklabel1 = row[yticklabel]
            yticklabel2 = row["formatted_pval"]
            if pd.isna(yticklabel2):
                yticklabel2 = ""

            extrapad = 0.05
            pad = ax.get_xlim()[1] * (1 + extrapad)
            t = ax.text(
                x=pad,
                y=yticklabel1,
                s=yticklabel2,
                horizontalalignment="left",
                verticalalignment="center",
            )
            (_, _), (x1, _) = inv.transform(
                t.get_window_extent(renderer=fig.canvas.get_renderer())
            )
            righttext_width = max(righttext_width, x1)

        # 2nd label title
        pval_title = kwargs.get("pval_title", "P-value")

        # The next few lines of code make sure that the "P-value" label title on the right columns are of the
        # same height (using negative_padding) and fontsize (using kwargs.get("fontsize", 12)) as the
        # ylabel height and fontsize. See draw_ylabel1(...).
        fontsize = kwargs.get("fontsize", 12)
        ylabel1_size = kwargs.get("ylabel1_size", 1 + fontsize)
        if annoteheaders:
            negative_padding = 1.0
        else:
            negative_padding = 0.5

        if pval_title is not None:
            if annoteheaders is None:
                t = ax.text(
                    pad,
                    ax.get_ylim()[1] - negative_padding,
                    pval_title,
                    size=ylabel1_size,
                    fontweight="bold",
                )
                (_, _), (x1, _) = inv.transform(
                    t.get_window_extent(renderer=fig.canvas.get_renderer())
                )
                righttext_width = max(righttext_width, x1)
            if annoteheaders is not None:  # if tableheaders exist
                pval_title_fontweight = kwargs.get("pval_title_fontweight", "bold")
                pval_title_fontsize = kwargs.get("pval_title_fontsize", 12)

                header_index = len(ax.get_yticklabels()) - 1
                t = ax.text(
                    x=pad,
                    y=header_index,
                    s=pval_title,
                    size=pval_title_fontsize,
                    fontweight=pval_title_fontweight,
                    horizontalalignment="left",
                    verticalalignment="center",
                )
                (_, _), (x1, _) = inv.transform(
                    t.get_window_extent(renderer=fig.canvas.get_renderer())
                )
                righttext_width = max(righttext_width, x1)
        return ax, righttext_width
    else:
        return ax, 0


def draw_yticklabel2(
    dataframe: pd.core.frame.DataFrame,
    annoteheaders: Union[Sequence[str], None],
    right_annoteheaders: Union[Sequence[str], None],
    ax: Axes,
    **kwargs: Any
) -> Tuple[Axes, float]:
    """
    Draw the second ylabel title on the right-hand side y-axis.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    grouplab_fontweight = kwargs.get("grouplab_fontweight", "bold")
    fontfamily = kwargs.get("fontfamily", "monospace")
    fontsize = kwargs.get("fontsize", 12)

    top_row_ix = len(dataframe) - 1
    inv = ax.transData.inverted()
    righttext_width = 0
    fig = plt.gcf()
    for ix, row in dataframe.iterrows():
        yticklabel1 = row["yticklabel"]
        yticklabel2 = row["yticklabel2"]

        extrapad = 0.05
        pad = ax.get_xlim()[1] * (1 + extrapad)
        if (ix == top_row_ix) and (
            annoteheaders is not None or right_annoteheaders is not None
        ):
            t = ax.text(
                x=pad,
                y=yticklabel1,
                s=yticklabel2,
                fontfamily=fontfamily,
                horizontalalignment="left",
                verticalalignment="center",
                fontsize=fontsize,
                fontweight=grouplab_fontweight,
            )
        else:
            t = ax.text(
                x=pad,
                y=yticklabel1,
                s=yticklabel2,
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


def draw_ylabel1(ylabel: str, pad: float, ax: Axes, **kwargs: Any) -> Axes:
    """
    Draw ylabel title for the left-hand side y-axis.

    Parameters
    ----------
    ylabel (str)
            Title of the left-hand side y-axis.
    pad (float)
            Window wdith of figure
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    fontsize = kwargs.get("fontsize", 12)
    ax.set_ylabel("")
    if ylabel is not None:
        # Retrieve settings from kwargs
        ylabel1_size = kwargs.get("ylabel1_size", 1 + fontsize)
        ylabel1_fontweight = kwargs.get("ylabel1_fontweight", "bold")
        ylabel_loc = kwargs.get("ylabel_loc", "top")
        ylabel_angle = kwargs.get("ylabel_angle", "horizontal")
        ax.set_ylabel(
            ylabel,
            loc=ylabel_loc,
            labelpad=-pad,
            rotation=ylabel_angle,
            size=ylabel1_size,
            fontweight=ylabel1_fontweight,
        )
    return ax


def remove_ticks(ax: Axes) -> Axes:
    """
    Remove the tickers on the top, left, and right borders.

    Parameters
    ----------
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    ax.tick_params(
        top=False,
        bottom=True,
        left=False,
        right=False,
        labelleft=True,
        labelright=False,
        labelbottom=True,
    )
    return ax


def format_grouplabels(
    dataframe: pd.core.frame.DataFrame, groupvar: str, ax: Axes, **kwargs: Any
) -> Axes:
    """
    Bold the group variable labels.

    Fontweight options in Matplotlib: [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight' ]

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    groupvar (str)
            Name of column containing group of variables.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    grouplab_size = kwargs.get("grouplab_size", 12)
    grouplab_fontweight = kwargs.get("grouplab_fontweight", "bold")
    if groupvar is not None:
        for ix, ylabel in enumerate(ax.get_yticklabels()):
            for gr in dataframe[groupvar].unique():
                try:
                    if gr.lower() == ylabel.get_text().lower().strip():
                        ax.get_yticklabels()[ix].set_fontweight(grouplab_fontweight)
                        ax.get_yticklabels()[ix].set_fontsize(grouplab_size)
                        ax.get_yticklabels()[ix].set_fontfamily("sans-serif")
                except AttributeError:
                    pass
    return ax


def despineplot(despine: bool, ax: Axes) -> Axes:
    """
    Despine the plot by removing the top, left, and right borders.

    Parameters
    ----------
    despine (bool)
            If True, despine.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    if despine:
        ax.spines["top"].set_color("None")
        ax.spines["left"].set_color("None")
        ax.spines["right"].set_color("None")
    return ax


def format_tableheader(
    annoteheaders: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    ax: Axes,
    **kwargs: Any
) -> Axes:
    """
    Format the tableheader as the first row in the data.

    Parameters
    ----------
    annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations
            on the left-hand side of the plot.
    right_annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations
            on the right-hand side of the plot.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    if (annoteheaders is not None) or (right_annoteheaders is not None):
        tableheader_fontweight = kwargs.get("tableheader_fontweight", "bold")
        tableheader_fontsize = kwargs.get("fontsize", 12)
        nlast = len(ax.get_yticklabels())  # last row is table header
        ax.get_yticklabels()[nlast - 1].set_fontweight(tableheader_fontweight)
        ax.get_yticklabels()[nlast - 1].set_fontsize(tableheader_fontsize)
    return ax


def format_xlabel(xlabel: str, ax: Axes, **kwargs: Any) -> Axes:
    """
    Format the x-axis label.

    Parameters
    ----------
    xlabel (str)
            Title of the left-hand side x-axis.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    if xlabel is not None:
        xlabel_size = kwargs.get("xlabel_size", 12)
        xlabel_fontweight = kwargs.get("xlabel_fontweight", "bold")
        ax.set_xlabel(xlabel, size=xlabel_size, fontweight=xlabel_fontweight)
    return ax


def format_xticks(
    dataframe: pd.core.frame.DataFrame,
    ll: str,
    hl: str,
    xticks: Optional[Union[list, range]],
    ax: Axes,
    **kwargs: Any
) -> Axes:
    """
    Format the xtick labels.

    This function sets the range of the x-axis using the lowest value and highest values
    in the confidence interval.
    Sets the xticks according to the user-provided 'xticks' or just use 5 tickers.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    ll (str)
            Name of column containing the lower limit of the confidence intervals.
            Optional
    hl (str)
            Name of column containing the upper limit of the confidence intervals.
            Optional
    xticks (list-like)
            List of xtickers to print on the x-axis.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    nticks = kwargs.get("nticks", 5)
    xtick_size = kwargs.get("xtick_size", 10)
    xticklabels = kwargs.get("xticklabels", None)
    xlowerlimit = dataframe[ll].min()
    xupperlimit = dataframe[hl].max()
    ax.set_xlim(xlowerlimit, xupperlimit)
    if xticks is not None:
        ax.set_xticks(xticks)
        ax.xaxis.set_tick_params(labelsize=xtick_size)
    else:
        ax.xaxis.set_major_locator(plt.MaxNLocator(nticks))
    ax.tick_params(axis="x", labelsize=xtick_size)
    if xticklabels:
        ax.set_xticklabels(xticklabels)
    for xticklab in ax.get_xticklabels():
        xticklab.set_fontfamily("sans-serif")
    return ax


def draw_alt_row_colors(
    dataframe: pd.core.frame.DataFrame,
    groupvar: str,
    annoteheaders: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    ax: Axes,
    **kwargs: Any
) -> Axes:
    """
    Color alternating rows in the plot.

    Colors the even-numbered rows gray unless they are rows that indicate groups.
    Breaks from groups will restart with gray.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    groupvar (str)
            Name of column containing group of variables.
    annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations
            on the left-hand side of the plot.
    right_annoteheaders (list-like)
            List of table headers to use as column headers for the additional annotations
            on the right-hand side of the plot.
    ax (Matplotlib Axes)
            Axes to operate on.

    Returns
    -------
            Matplotlib Axes object.
    """
    # Retrieve settings
    row_color = kwargs.get("row_color", "0.5")
    if (annoteheaders is not None) or (right_annoteheaders is not None):
        headers_exist = True
    else:
        headers_exist = False
    yticklabels = ax.get_yticklabels()
    counter = 1
    if groupvar is not None:
        groups = [
            grp_str.strip().lower()
            for grp_str in dataframe[groupvar].unique()
            if isinstance(grp_str, str)
        ]
    else:
        groups = []
    for ix, ticklab in enumerate(yticklabels):
        if headers_exist and (ix == len(yticklabels) - 1):
            break
        labtext = ticklab.get_text()
        if labtext.lower().strip() in groups:
            counter = 2  # reset
        else:  # color if even row
            if counter % 2 == 0:
                ax.axhspan(ix - 0.5, ix + 0.5, color=row_color, alpha=0.08, zorder=0)
            counter += 1
    return ax


def draw_tablelines(
    dataframe: pd.core.frame.DataFrame,
    righttext_width: float,
    pval: str,
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    ax: Axes,
) -> Axes:
    """
    Plot horizontal lines as table lines.

    Cf. draw_ylabel2 for righttext_width.

    Parameters
    ----------
    dataframe (pandas.core.frame.DataFrame)
            Pandas DataFrame where rows are variables. Columns are variable name, estimates,
            margin of error, etc.
    righttext_width (float)
            x-axis coordinate of the rightmost character of the right-side annotations.
    ax: Axes

    Returns
    -------
            Matplotlib Axes object.
    """
    first_yticklab = ax.get_yaxis().majorTicks[-1]
    bbox_disp = first_yticklab.label.get_window_extent()
    (x0, _), (x1, _) = ax.transData.inverted().transform(bbox_disp)
    upper_lw, lower_lw = 2, 1.3
    nrows = len(dataframe)
    plt.plot(
        [x0, x1], [nrows - 0.4, nrows - 0.4], color="0", linewidth=upper_lw, clip_on=False
    )
    plt.plot(
        [x0, x1], [nrows - 1.45, nrows - 1.45], color="0.5", linewidth=lower_lw, clip_on=False
    )
    if (right_annoteheaders is not None) or (pval is not None):
        extrapad = 0.05
        x0 = ax.get_xlim()[1] * (1 + extrapad)
        plt.plot(
            [x0, righttext_width],
            [nrows - 0.4, nrows - 0.4],
            color="0",
            linewidth=upper_lw,
            clip_on=False,
        )
        plt.plot(
            [x0, righttext_width],
            [nrows - 1.45, nrows - 1.45],
            color=".5",
            linewidth=lower_lw,
            clip_on=False,
        )
    return ax
