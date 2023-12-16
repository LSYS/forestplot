import pandas as pd
from matplotlib.pyplot import Axes

from forestplot import mforestplot

dataname = "sleep-mmodel"
data = f"https://raw.githubusercontent.com/lsys/forestplot/mplot/examples/data/{dataname}.csv"
df = pd.read_csv(data)


std_opts = dict(
    dataframe = df,
    estimate = "coef",
    ll  ="ll", 
    hl = "hl",
    varlabel = "var",
    model_col = "model",
)

def test_vanilla_mplot():
    ax =  mforestplot(**std_opts)
    assert isinstance(ax, Axes)

    _df, ax =  mforestplot(**std_opts, return_df=True)
    assert isinstance(ax, Axes)
    assert isinstance(_df, pd.DataFrame)


# fmt: off
def test_more_options():
	_df, ax = mforestplot(**std_opts,
	                         color_alt_rows=True,
	                         groupvar="group",
	                         table=True,
	                         rightannote=["var", "group"],
	                         right_annoteheaders=["Variable", "Variable group"],
	                         xlabel="Coefficient (95% CI)",
	                         modellabels=["Have young kids", "Full sample"],
	                         xticks=[-1200,-600, 0, 600],
	                         return_df=True,
	                         # Additional kwargs for customizations
	                         **{"marker": "D",  # set maker symbol as diamond
	                            "markersize": 35,  # adjust marker size
	                            "xlinestyle": (0, (10, 5)),  # long dash for x-reference line 
	                            "xlinecolor": "#808080",  # gray color for x-reference line
	                            "xtick_size": 12,  # adjust x-ticker fontsize
	                            "despine": False,
	                           }                           
	                        )
	assert isinstance(ax, Axes)
	assert isinstance(_df, pd.DataFrame)
