from forestplot.mplot_graph_utils import mdraw_ref_xline, mdraw_yticklabels
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import Axes


x, y = [0, 1, 2], [0, 1, 2]
str_vector = ["a", "b", "c"]
input_df = pd.DataFrame(
    {
        "yticklabel": str_vector,
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
    ax = mdraw_ref_xline(ax, dataframe=input_df, model_col="yticklabel", annoteheaders=None, right_annoteheaders=None)
    assert isinstance(ax, Axes)


def test_mdraw_yticklabels():
    # Prepare the input DataFrame
    x = [0, 1, 2]
    str_vector = ["a", "b", "c"]
    input_df = pd.DataFrame({
        "yticklabel": str_vector,
    })

    # Create a matplotlib Axes object
    _, ax = plt.subplots()

    # Call the function
    ax = mdraw_yticklabels(input_df, yticklabel='yticklabel',flush=True, ax=ax)

    assert isinstance(ax, Axes)
    assert [label.get_text() for label in ax.get_yticklabels()] == str_vector

