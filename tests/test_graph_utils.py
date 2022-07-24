import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from pyforestplot.graph_utils import *


x, y = [0, 1, 2], [0, 1, 2]
str_vector = ["a", "b", "c"]
input_df = pd.DataFrame(
    {
        "yticklabel": str_vector,
        "estimate": x,
        "moerror": y,
        "pval": y,
        "formatted_pval": y,
        "yticklabel1": str_vector,
        "yticklabel2": str_vector,
    }
)


def test_draw_ci():
    _, ax = plt.subplots()
    ax = draw_ci(
        input_df, estimate="estimate", yticklabel="yticklabel", moerror="moerror", ax=ax
    )
    assert isinstance(ax, Axes)

    xticklabels = [lab.get_text() for lab in ax.get_yticklabels()]
    assert all(txt in xticklabels for txt in input_df["yticklabel"])

    # Assert yticks are integers
    assert (all(tick, int) for tick in ax.get_yticks())


def test_draw_est_markers():
    _, ax = plt.subplots()

    ax = draw_est_markers(input_df, estimate="estimate", yticklabel="yticklabel", ax=ax)
    assert isinstance(ax, Axes)

    len_yticks = len(ax.get_yticks())
    len_df = len(input_df)
    assert len_yticks == len_df  # each marker is a row in the df

    # Assert yticks are integers
    assert (all(tick, int) for tick in ax.get_yticks())

    xmin, xmax = ax.get_xlim()
    assert xmin <= input_df["estimate"].min()
    assert xmax >= input_df["estimate"].max()


def test_draw_ref_xline():
    _, ax = plt.subplots()
    ax = draw_ref_xline(ax)
    assert isinstance(ax, Axes)

    # Default is x = 0 line
    assert len(ax.get_lines()) == 1
    refline = ax.get_lines()[0]
    x0, x1 = refline.get_xdata()
    assert x0 == 0
    assert x1 == 0

    # Add second x = 1 line
    ax = draw_ref_xline(ax, xline=1)
    assert isinstance(ax, Axes)
    assert len(ax.get_lines()) == 2  # two lines now

    # Assert second line is at x = 1
    refline = ax.get_lines()[1]
    x0, x1 = refline.get_xdata()
    assert x0 == 1
    assert x1 == 1


def test_right_flush_yticklabels():
    _, ax = plt.subplots()
    pad = right_flush_yticklabels(input_df, yticklabel="yticklabel", flush=True, ax=ax)
    assert isinstance(pad, float)
    assert pad >= 0


def test_draw_pval_right():
    x, y = [0, 1, 2], [0, 1, 2]
    str_vector = ["a", "b", "c"]
    input_df = pd.DataFrame(
        {"yticklabel": x, "estimate": x, "moerror": y, "pval": y, "formatted_pval": y,}
    )
    _, ax = plt.subplots()
    payload1, payload2 = draw_pval_right(
        input_df,
        pval="pval",
        annoteheaders=None,
        rightannote=None,
        yticklabel="yticklabel",
        yticker2=None,
        ylabel2=None,
        pad=None,
        ax=ax,
    )
    assert isinstance(payload1, Axes)
    assert isinstance(payload2, float)


def test_draw_yticklabel2():
    x = [0, 1, 2]
    str_vector = ["a", "b", "c"]
    input_df = pd.DataFrame({"yticklabel": x, "yticklabel2": str_vector,})
    _, ax = plt.subplots()
    payload1, payload2 = draw_yticklabel2(input_df, pad=None, ax=ax)
    assert isinstance(payload1, Axes)
    assert isinstance(payload2, float)


def test_draw_ylabel1():
    _, ax = plt.subplots()
    ylabel_str = "ylabel"
    ax = draw_ylabel1(ylabel=ylabel_str, pad=0, ax=ax)
    assert isinstance(ax, Axes)
    assert ax.get_ylabel() == ylabel_str

    # No ylabel
    _, ax = plt.subplots()
    ylabel_str = None
    ax = draw_ylabel1(ylabel=ylabel_str, pad=0, ax=ax)
    assert isinstance(ax, Axes)
    assert ax.get_ylabel() == ""


def test_remove_ticks():
    _, ax = plt.subplots()
    ax = remove_ticks(ax=ax)
    assert isinstance(ax, Axes)


def test_format_grouplabels():
    input_df = pd.DataFrame(
        {
            "var": ["var1", "var2", "group"],
            "groupvar": ["group", "group", "group"],
            "estimate": [1, 2, 3],
        }
    )
    _, ax = plt.subplots()
    # No change if groupvar is none
    output_ax = format_grouplabels(input_df, groupvar=None, ax=ax)
    assert isinstance(output_ax, Axes)
    assert output_ax == ax

    # With group
    _, ax = plt.subplots()
    output_ax = format_grouplabels(input_df, groupvar="groupvar", ax=ax)
    assert isinstance(output_ax, Axes)


def test_despineplot():
    _, ax = plt.subplots()
    ax = despineplot(despine=True, ax=ax)
    assert isinstance(ax, Axes)


def test_format_tableheader():
    _, ax = plt.subplots()
    ax = format_tableheader(annoteheaders=["test"], right_annoteheaders=["test"], ax=ax)
    assert isinstance(ax, Axes)
    assert ax.get_yticklabels()[-1].get_fontweight() == "bold"

    # Check no formatting happens with no headers
    _, ax = plt.subplots()
    ax = format_tableheader(annoteheaders=None, right_annoteheaders=None, ax=ax)
    assert isinstance(ax, Axes)
    assert ax.get_yticklabels()[-1].get_fontweight() == "normal"


def test_format_xlabel():
    # no label
    _, ax = plt.subplots()
    ax = format_xlabel(xlabel=None, ax=ax)
    assert isinstance(ax, Axes)
    assert ax.get_xlabel() == ""

    # with label
    _, ax = plt.subplots()
    label = "xlabel"
    ax = format_xlabel(xlabel=label, ax=ax)
    assert isinstance(ax, Axes)
    assert ax.get_xlabel() == label

    # with label, normal fontweight, 12 fontsize
    _, ax = plt.subplots()
    label = "xlabel"
    ax = format_xlabel(xlabel=label, ax=ax, xlabel_fontweight="normal", xlabel_size=12)
    assert isinstance(ax, Axes)
    assert ax.xaxis.label.get_fontweight() == "normal"
    assert ax.xaxis.label.get_fontsize() == 12


def test_format_xticks():
    input_df = pd.DataFrame(
        {
            "var": ["var1", "var2", "var3"],
            "groupvar": ["group1", "group1", "group1"],
            "estimate": [1, 2, 3],
            "ll": [1, 2, 3],
            "hl": [1, 2, 3],
        }
    )
    # No ticks set
    _, ax = plt.subplots()
    ax = format_xticks(input_df, ll="ll", hl="hl", xticks=None, ax=ax)
    assert isinstance(ax, Axes)
    ax_xmin, ax_xmax = ax.get_xlim()
    data_xmin, data_xmax = input_df.ll.min(), input_df.hl.max()
    assert ax_xmin <= data_xmin
    assert ax_xmax <= data_xmax

    # Set xticks
    _, ax = plt.subplots()
    ax = format_xticks(input_df, ll="ll", hl="hl", xticks=[1, 2, 3], ax=ax)
    assert isinstance(ax, Axes)
    ax_xmin, ax_xmax = ax.get_xlim()
    data_xmin, data_xmax = input_df.ll.min(), input_df.hl.max()
    assert ax_xmin <= data_xmin
    assert ax_xmax <= data_xmax


def test_draw_xticks():
    _, ax = plt.subplots()
    ax = draw_xticks(xticks=None, ax=ax)
    assert isinstance(ax, Axes)

    _, ax = plt.subplots()
    ax = draw_xticks(xticks=[1, 2, 3], ax=ax)
    assert isinstance(ax, Axes)


def test_draw_alt_row_colors():
    input_df = pd.DataFrame({"groupvar": ["group1", "group1", "group1"]})

    # Group exists
    _, ax = plt.subplots()
    ax = draw_alt_row_colors(
        input_df, groupvar="groupvar", annoteheaders=None, right_annoteheaders=None, ax=ax,
    )
    assert (all(tick, int) for tick in ax.get_yticks())
    assert isinstance(ax, Axes)

    # No Group
    _, ax = plt.subplots()
    ax = draw_alt_row_colors(
        input_df, groupvar=None, annoteheaders=None, right_annoteheaders=None, ax=ax
    )
    assert (all(tick, int) for tick in ax.get_yticks())
    assert isinstance(ax, Axes)

    # Group exists w/ headers
    _, ax = plt.subplots()
    ax = draw_alt_row_colors(
        input_df,
        groupvar="groupvar",
        annoteheaders=["left head"],
        right_annoteheaders=["right head"],
        ax=ax,
    )
    assert (all(tick, int) for tick in ax.get_yticks())
    assert isinstance(ax, Axes)


def test_draw_tablelines():
    _, ax = plt.subplots()
    draw_tablelines(input_df, righttext_width=0, pval=None, right_annoteheaders=None, ax=ax)
    assert isinstance(ax, Axes)
    assert len(ax.get_lines()) == 2

    _, ax = plt.subplots()
    draw_tablelines(
        input_df,
        righttext_width=0,
        pval="pval",
        right_annoteheaders=["right_annoteheaders"],
        ax=ax,
    )
    assert isinstance(ax, Axes)
    assert len(ax.get_lines()) == 4

    _, ax = plt.subplots()
    draw_tablelines(input_df, righttext_width=0, pval="pval", right_annoteheaders=None, ax=ax)
    assert isinstance(ax, Axes)
    assert len(ax.get_lines()) == 4

    _, ax = plt.subplots()
    draw_tablelines(
        input_df,
        righttext_width=0,
        pval=None,
        right_annoteheaders=["right_annoteheaders"],
        ax=ax,
    )
    assert isinstance(ax, Axes)
    assert len(ax.get_lines()) == 4
