#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from forestplot import forestplot
from matplotlib.pyplot import Axes

dataname = "sleep"
data = f"https://raw.githubusercontent.com/lsys/pyforestplot/main/examples/data/{dataname}.csv"
df = pd.read_csv(data).assign(n=lambda df: df["n"].map(str))

# fmt: off
def test_vanilla():
    ax = forestplot(df,  # the dataframe with results data # fmt: off
                    estimate='r',  # col containing estimated effect size 
                    ll="ll", hl="hl",  # columns containing conf. int. lower and higher limits
                    varlabel='label',  # column containing variable label
                    ylabel="Confidence interval",  # y-label title
                    xlabel="Pearson correlation"  # x-label title
                    )
    assert isinstance(ax, Axes)


# fmt: off
def test_more_options():
    output_df, ax = forestplot(df,  # the dataframe with results data
                               estimate='r',  # col containing estimated effect size 
                               ll='ll', hl='hl',  # lower & higher limits of conf. int.
                               varlabel='label',  # column containing the varlabels to be printed on far left
                               pval='p-val',  # column containing p-values to be formatted
                               annote=['n', 'power', "est_ci"],  # columns to report on left of plot
                               annoteheaders=['N', 'Power', 'Est. (95% Conf. Int.)'],  # ^corresponding headers
                               rightannote=['formatted_pval', 'group'],  # columns to report on right of plot 
                               right_annoteheaders=['P-value', 'Variable group'],  # ^corresponding headers
                               groupvar='group',  # column containing group labels
                               group_order=['labor factors', 'occupation', 'age', 'health factors', 
                               'family factors', 'area of residence', 'other factors'],                   
                               xlabel='Pearson correlation coefficient',  # x-label title
                               xticks=[-.4,-.2,0, .2],  # x-ticks to be printed
                               sort=True,  # sort estimates in ascending order
                               table=True,  # Format as a table
                               return_df=True, 
                               **{'marker': 'D',  # set maker symbol as diamond
                                  'markersize': 35,  # adjust marker size
                                  'xlinestyle': (0, (10, 5)),  # long dash for x-reference line 
                                  'xlinecolor': '.1',  # gray color for x-reference line
                                  'xtick_size': 12,  # adjust x-ticker fontsize
                                 }  
                               )
    assert isinstance(ax, Axes)
    assert isinstance(output_df, pd.DataFrame)
