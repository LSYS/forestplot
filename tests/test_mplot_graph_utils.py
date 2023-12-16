import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.pyplot import Axes

from forestplot.mplot_graph_utils import (
    mdraw_ci,
    mdraw_est_markers,
    mdraw_legend,
    mdraw_ref_xline,
    mdraw_yticklabels, mdraw_yticklabel2
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


def test_mdraw_legend():
    # Create a simple plot
    _, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], marker="o", color="0")
    ax.plot([0, 1], [1, 0], marker="s", color="0.4")

    # Sample parameters for the legend
    modellabels = ["Model 1", "Model 2"]
    msymbols = ["o", "s"]
    mcolor = ["0", "0.4"]

    # Call the function
    ax = mdraw_legend(ax, None, modellabels, msymbols, mcolor)

    # Assertions
    legend = ax.get_legend()
    assert legend is not None, "Legend was not created."

    # Check number of legend entries
    assert len(legend.get_texts()) == len(modellabels), "Incorrect number of legend entries."

    # Check legend labels
    for label, model_label in zip(legend.get_texts(), modellabels):
        assert label.get_text() == model_label, "Legend labels do not match."

    # Check legend marker colors and symbols
    for line, color in zip(legend.legendHandles, mcolor):
        assert isinstance(line, Line2D), "Legend entry is not a Line2D instance."
        assert line.get_color() == color, "Legend marker color does not match."


    
def test_mdraw_yticklabel2():
    # Create sample DataFrame
    df = pd.DataFrame({
        'yticklabel2': ['Label 1', 'Label 2', 'Label 3']
    })

    # Initialize Matplotlib Axes
    _, ax = plt.subplots()

    # Call the function
    ax, righttext_width = mdraw_yticklabel2(df, None, None, ax)

    # Assertions
    # Check if righttext_width is a float (or int, based on your implementation)
    assert isinstance(righttext_width, (float, int)), "righttext_width is not a numeric value."

    # Additional checks can be made for text properties like content, font size, and alignment
    texts = [text for text in ax.get_children() if isinstance(text, plt.Text)]
    for text, expected_label in zip(texts, df['yticklabel2']):
        assert text.get_text() == expected_label, "Text label content does not match."

