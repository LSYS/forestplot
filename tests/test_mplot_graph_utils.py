import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import Axes

from forestplot.mplot_graph_utils import (
    mdraw_ci,
    mdraw_est_markers,
    mdraw_ref_xline,
    mdraw_yticklabels,
)

x, y = [0, 1, 2], [0, 1, 2]
str_vector = ["a", "b", "c"]
models_vector = ["m1", "m1", "m2"]
input_df = pd.DataFrame(
    {
        "yticklabel": str_vector,
        "model": models_vector,
        "estimate": x,
        "moerror": y,
        "ll": x,
        "hl": y,
        "pval": y,
        "formatted_pval": y,
        "yticklabel1": str_vector,
        "yticklabel2": str_vector,
    }
)


def test_mdraw_ref_xline():
    _, ax = plt.subplots()
    ax = mdraw_ref_xline(
        ax,
        dataframe=input_df,
        model_col="yticklabel",
        annoteheaders=None,
        right_annoteheaders=None,
    )
    assert isinstance(ax, Axes)


def test_mdraw_yticklabels():
    # Prepare the input DataFrame
    str_vector = ["a", "b", "c"]
    input_df = pd.DataFrame(
        {
            "yticklabel": str_vector,
        }
    )

    # Create a matplotlib Axes object
    _, ax = plt.subplots()

    # Call the function
    ax = mdraw_yticklabels(input_df, yticklabel="yticklabel", flush=True, ax=ax)

    assert isinstance(ax, Axes)
    assert [label.get_text() for label in ax.get_yticklabels()] == str_vector


def test_mdraw_est_markers():
    _, ax = plt.subplots()
    ax = mdraw_est_markers(
        input_df,
        estimate="estimate",
        model_col="model",
        models=list(set(models_vector)),
        ax=ax,
    )
    assert isinstance(ax, Axes)
    assert (all(isinstance(tick, int)) for tick in ax.get_yticks())

    xmin, xmax = ax.get_xlim()
    assert xmin <= input_df["estimate"].min()
    assert xmax >= input_df["estimate"].max()
    assert len(ax.collections) == len(set(models_vector))


def test_mdraw_ci():
    _, ax = plt.subplots()

    # Call the function
    ax = mdraw_ci(
        input_df,
        estimate="estimate",
        ll="ll",
        hl="hl",
        model_col="model",
        models=list(set(models_vector)),
        logscale=False,
        ax=ax,
    )

    # Assertions
    assert isinstance(ax, Axes)
    assert len(ax.collections) == len(set(models_vector))
