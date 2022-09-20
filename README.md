<div id="top"></div> 
<h1 align="center" >
  <strong>Forestplot</strong>
</h1>
<p align="center">
  <a href="https://pypi.org/project/forestplot">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/forestplot?label=Python&logo=python&logoColor=white">
  </a><br>
  <b>Easy API for forest plots.</b><br>
  A Python package to make publication-ready but customizable forest plots.
</p>

<p align="center"><img width="100%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/main.png"></p>

-----------------------------------------------------------

This package makes publication-ready forest plots easy to make out-of-the-box. Users provide a `dataframe` (e.g. from a spreadsheet) where rows correspond to a variable/study with columns including estimates, variable labels, and lower and upper confidence interval limits.
Additional options allow easy addition of columns in the `dataframe` as annotations in the plot.

<!---------------------- Project shields ---------------------->

|    |    |
| --- | --- |
| Release | [![PyPI](https://img.shields.io/pypi/v/forestplot?color=blue&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/forestplot/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/lsys/forestplot?color=blue&label=Latest%20release)](https://github.com/LSYS/forestplot/releases) |
| Status | [![Notebooks](https://github.com/LSYS/forestplot/actions/workflows/nb.yml/badge.svg)](https://github.com/LSYS/forestplot/actions/workflows/nb.yml) [![CI](https://github.com/LSYS/forestplot/actions/workflows/CI.yml/badge.svg)](https://github.com/LSYS/forestplot/actions/workflows/CI.yml)  |
| Coverage |  [![Codecov](https://img.shields.io/codecov/c/github/lsys/forestplot?logo=codecov&logoColor=white)](https://app.codecov.io/gh/LSYS/forestplot) |
| Docs | [![Read the Docs (version)](https://img.shields.io/readthedocs/forestplot/stable?label=docs&logo=readthedocs&logoColor=white)](https://forestplot.readthedocs.io/en/latest/?badge=latest) [![DocLinks](https://github.com/LSYS/forestplot/actions/workflows/links.yml/badge.svg)](https://github.com/LSYS/forestplot/actions/workflows/links.yml)|
| Python | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/forestplot?label=Python%203.6%2B&logo=python&logoColor=white)](https://pypi.org/project/forestplot/) |
| Meta | ![GitHub](https://img.shields.io/github/license/lsys/forestplot?color=purple&label=License) ![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/lsys/forestplot?label=CodeFactor&logo=codefactor&logoColor=red) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LSYS/forestplot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LSYS/forestplot/context:python) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) |

<!---------------------- TABLE OF CONTENT ---------------------->
<details open><summary><b>Table of Contents</b></summary><p>

> - [Installation](#installation)
> - [Quick Start](#quick-start)
> - [Some Examples with Customizations](#some-examples-with-customizations)
> - [Gallery and API Options](#gallery-and-api-options)
> - [Known Issues](#known-issues)
> - [Background and Additional Resources](#background-and-additional-resources)
> - [Contributing](#contributing)
</p></details><p></p>

<!------------------------- INSTALLATION ------------------------->
## Installation[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#installation)

Install from PyPI<br>
 [![PyPI](https://img.shields.io/pypi/v/forestplot?color=blue&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/forestplot/)
```bash
pip install pyforestplot
```

Install from source<br>
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/lsys/forestplot?color=blue&label=Latest%20release)](https://github.com/LSYS/forestplot/releases)<br>
```bash
git clone https://github.com/LSYS/forestplot.git
cd forestplot
pip install .
```
<p align="right">(<a href="#top">back to top</a>)</p>


<!------------------------- QUICK START ------------------------->
## Quick start[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#quick-start)

```python
import forestplot as fp

df = fp.load_data("sleep")
df.head(3)
```
|    | var      |          r |   moerror | label                     | group         |    ll |    hl |   n |    power |     p-val |
|---:|:---------|-----------:|----------:|:--------------------------|:--------------|------:|------:|----:|---------:|----------:|
|  0 | age      |  0.0903729 | 0.0696271 | in years                  | age           |  0.02 |  0.16 | 706 | 0.671578 | 0.0163089 |
|  1 | black    | -0.0270573 | 0.0770573 | =1 if black               | other factors | -0.1  |  0.05 | 706 | 0.110805 | 0.472889  |
|  2 | clerical |  0.0480811 | 0.0719189 | =1 if clerical worker     | occupation    | -0.03 |  0.12 | 706 | 0.247768 | 0.201948  |

(* This is a toy example of how certain factors correlate with the amount of sleep one gets. See the [notebook that generates the data](https://nbviewer.org/github/LSYS/forestplot/blob/main/examples/get-sleep.ipynb).)

<details><summary><i>The example input dataframe above have 4 key columns</i></summary>

  | Column    | Description                                     | Required  |
  |:----------|:------------------------------------------------|:----------|
  | `var`     | Variable field                                  |           |
  | `r`       | Correlation coefficients (estimates to plot)    | &check;   |
  | `moerror` | Conf. int.'s *margin of error*.                 |           |
  | `label`   | Variable labels                                 | &check;   |
  | `group`   | Variable grouping labels                        |           |
  | `ll`      | Conf. int. *lower limits*                       | &check;*  |
  | `hl`      | Containing the conf. int. *higher limits*       | &check;*  |
  | `n`       | Sample size                                     |           |
  | `power`   | Statistical power                               |           |
  | `p-val`   | P-value                                         |           |

  (*If `ll` *and* `hl` are specified, then the `moerror` (margin of error) is not required.
  <br>
  See [Gallery and API Options](#gallery-and-api-options) for more details on required and optional arguments.)  
</details>

Make the forest plot
```python
fp.forestplot(df,  # the dataframe with results data
               estimate="r",  # col containing estimated effect size 
               ll="ll", hl="hl",  # columns containing conf. int. lower and higher limits
               varlabel="label",  # column containing variable label
               ylabel="Confidence interval",  # y-label title
               xlabel="Pearson correlation"  # x-label title
               )
```
<p align="left"><img width="55%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/vanilla.png"></p>

<p align="right">(<a href="#top">back to top</a>)</p>


<!------------------ EXAMPLES of CUSTOMIZATIONS ------------------>
## Some examples with customizations[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#examples-with-customizations)


1. Add variable groupings, add group order, and sort by estimate size.
```python
fp.forestplot(df,  # the dataframe with results data
              estimate="r",  # col containing estimated effect size 
              moerror="moerror",  # columns containing conf. int. margin of error
              varlabel="label",  # column containing variable label
              groupvar="group",  # Add variable groupings 
              # group ordering
              group_order=["labor factors", "occupation", "age", "health factors", 
                           "family factors", "area of residence", "other factors"],
              sort=True  # sort in ascending order (sorts within group if group is specified)               
              )
```
<p align="left"><img width="65%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/group-grouporder-sort.png"></p>

2. Add p-values on the right and color alternate rows gray
```python
fp.forestplot(df,  # the dataframe with results data
              estimate="r",  # col containing estimated effect size 
              ll="ll", hl="hl",  # columns containing conf. int. lower and higher limits
              varlabel="label",  # column containing variable label
              groupvar="group",  # Add variable groupings 
              # group ordering
              group_order=["labor factors", "occupation", "age", "health factors", 
                           "family factors", "area of residence", "other factors"],
              sort=True,  # sort in ascending order (sorts within group if group is specified)               
              pval="p-val",  # Column of p-value to be reported on right
              color_alt_rows=True,  # Gray alternate rows
              ylabel="Est.(95% Conf. Int.)",  # ylabel to print
              **{"ylabel1_size": 11}  # control size of printed ylabel
              )
```

<p align="left"><img width="70%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/group-grouporder-pvalue-sort-colorrows.png"></p>


3. Customize annotations and make it a table
```python
fp.forestplot(df,  # the dataframe with results data
              estimate="r",  # col containing estimated effect size 
              ll="ll", hl="hl",  # lower & higher limits of conf. int.
              varlabel="label",  # column containing the varlabels to be printed on far left
              pval="p-val",  # column containing p-values to be formatted
              annote=["n", "power", "est_ci"],  # columns to report on left of plot
              annoteheaders=["N", "Power", "Est. (95% Conf. Int.)"],  # ^corresponding headers
              rightannote=["formatted_pval", "group"],  # columns to report on right of plot 
              right_annoteheaders=["P-value", "Variable group"],  # ^corresponding headers
              xlabel="Pearson correlation coefficient",  # x-label title
              table=True,  # Format as a table
              )
```

<p align="left"><img width="75%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/leftannote-rightannote-table.png"></p>

4. Strip down all bells and whistle
```python
fp.forestplot(df,  # the dataframe with results data
              estimate="r",  # col containing estimated effect size 
              ll="ll", hl="hl",  # lower & higher limits of conf. int.
              varlabel="label",  # column containing the varlabels to be printed on far left
              ci_report=False,  # Turn off conf. int. reporting
              flush=False,  # Turn off left-flush of text
              **{'fontfamily': 'sans-serif'}  # revert to sans-serif                              
              )
```               
<p align="left"><img width="40%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/vcoefplot.png"></p>

5. Example with more customizations
```python
fp.forestplot(df,  # the dataframe with results data
              estimate="r",  # col containing estimated effect size 
              ll="ll", hl="hl",  # lower & higher limits of conf. int.
              varlabel="label",  # column containing the varlabels to be printed on far left
              pval="p-val",  # column containing p-values to be formatted
              annote=["n", "power", "est_ci"],  # columns to report on left of plot
              annoteheaders=["N", "Power", "Est. (95% Conf. Int.)"],  # ^corresponding headers
              rightannote=["formatted_pval", "group"],  # columns to report on right of plot 
              right_annoteheaders=["P-value", "Variable group"],  # ^corresponding headers
              groupvar="group",  # column containing group labels
              group_order=["labor factors", "occupation", "age", "health factors", 
                           "family factors', "area of residence", "other factors"],                   
              xlabel="Pearson correlation coefficient",  # x-label title
              xticks=[-.4,-.2,0, .2],  # x-ticks to be printed
              sort=True,  # sort estimates in ascending order
              table=True,  # Format as a table
              # Additional kwargs for customizations
              **{"marker": "D",  # set maker symbol as diamond
                 "markersize": 35,  # adjust marker size
                 "xlinestyle": (0, (10, 5)),  # long dash for x-reference line 
                 "xlinecolor": ".1",  # gray color for x-reference line
                 "xtick_size": 12,  # adjust x-ticker fontsize
                }  
              )
```
<p align="left"><img width="70%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/main.png"></p>

<details><summary><i>Annotations arguments allowed include:</i></summary>
  
  * `ci_range`: Confidence interval range (e.g. `(-0.39 to -0.25)`).
  * `est_ci`: Estimate and CI (e.g. `-0.32(-0.39 to -0.25)`).
  * `formatted_pval`: Formatted p-values (e.g. `0.01**`).
  
  To confirm what processed `columns` are available as annotations, you can do:
  
  ```python
  processed_df, ax = fp.forestplot(df, 
                                   ...  # other arguments here
                                   return_df=True  # return processed dataframe with processed columns
                                  )
  processed_df.head(3)
  ```
  
  |    | label                | group         |   n |          r | CI95%         |       p-val |      BF10 |   power | var    |    hl |    ll |   moerror |   formatted_r |   formatted_ll |   formatted_hl | ci_range         | est_ci                | formatted_pval   |   formatted_n |   formatted_power | formatted_est_ci      | yticklabel                                                        | formatted_formatted_pval   | formatted_group   | yticklabel2            |
|---:|:---------------------|:--------------|----:|-----------:|:--------------|------------:|----------:|--------:|:-------|------:|------:|----------:|--------------:|---------------:|---------------:|:-----------------|:----------------------|:-----------------|--------------:|------------------:|:----------------------|:------------------------------------------------------------------|:---------------------------|:------------------|:-----------------------|
|  0 | Mins worked per week | Labor factors | 706 | -0.321384  | [-0.39 -0.25] | 1.99409e-18 | 1.961e+15 |    1    | totwrk | -0.25 | -0.39 | 0.0686165 |         -0.32 |          -0.39 |          -0.25 | (-0.39 to -0.25) | -0.32(-0.39 to -0.25) | 0.0***           |           706 |              1    | -0.32(-0.39 to -0.25) | Mins worked per week            706  1.0    -0.32(-0.39 to -0.25) | 0.0***                     | Labor factors     | 0.0***   Labor factors |
|  1 | Years of schooling   | Labor factors | 706 | -0.0950039 | [-0.17 -0.02] | 0.0115515   | 1.137     |    0.72 | educ   | -0.02 | -0.17 | 0.0749961 |         -0.1  |          -0.17 |          -0.02 | (-0.17 to -0.02) | -0.10(-0.17 to -0.02) | 0.01**           |           706 |              0.72 | -0.10(-0.17 to -0.02) | Years of schooling              706  0.72   -0.10(-0.17 to -0.02) | 0.01**                     | Labor factors     | 0.01**   Labor factors |
  
</details>
<p align="right">(<a href="#top">back to top</a>)</p>




<!------------------- GALLERY AND API OPTIONS ------------------->
## Gallery and API Options[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#gallery-and-api-options)

[![Notebooks](https://github.com/LSYS/forestplot/actions/workflows/nb.yml/badge.svg)](https://github.com/LSYS/forestplot/actions/workflows/nb.yml)

Check out [this jupyter notebook](https://nbviewer.org/github/LSYS/forestplot/blob/main/examples/readme-examples.ipynb) for a gallery variations of forest plots possible out-of-the-box.
The table below shows the list of arguments users can pass in.
More fined-grained control for base plot options (eg font sizes, marker colors) can be inferred from the [example notebook gallery](https://nbviewer.org/github/LSYS/forestplot/blob/main/examples/readme-examples.ipynb). 


| Option      | Description                                                                                                                                                 | Required   |
|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:---|
| `dataframe`           | Pandas dataframe where rows are variables (or studies for meta-analyses) and columns include estimated effect sizes, labels, and confidence intervals, etc. | &check; |
| `estimate`            | Name of column in `dataframe` containing the *estimates*.                                                                                                   | &check; |
| `varlabel`            | Name of column in `dataframe` containing the *variable labels* (study labels if meta-analyses).                                                             | &check; |
| `ll`                  | Name of column in `dataframe` containing the conf. int. *lower limits*.                                                                                     | &check;* |
| `hl`                  | Name of column in `dataframe` containing the conf. int. *higher limits*.                                                                                    | &check;* |
| `moerror`             | Name of column in `dataframe` containing the conf. int. *margin of errors*.                                                                                 | &check;* |
| `form_ci_report`      | If True (default), report the estimates and confidence interval beside the variable labels.                                                                 |          |
| `ci_report`           | If True (default), format the confidence interval as a string.                                                                                              |          |
| `groupvar`            | Name of column in `dataframe` containing the variable *grouping labels*.                                                                                    |       |
| `group_order`         | List of group labels indicating the order of groups to report in the plot.                                                                                  |       |
| `annote`              | List of columns to add as annotations on the left-hand side of the plot.                                                                                    |       |
| `annoteheaders`       | List of column headers for the left-hand side annotations.                                                                                                  |       |
| `rightannote`         | List of columns to add as annotations on the right-hand side of the plot.                                                                                   |       |
| `right_annoteheaders` | List of column headers for the right-hand side annotations.                                                                                                 |       |
| `pval`                | Name of column in `dataframe` containing the p-values.                                                                                                      |       |
| `starpval`            | If True (default), format p-values with stars indicating statistical significance.                                                                          |          |
| `sort`                | If True, sort variables by `estimate` values in ascending order.                                                                                            |          |
| `sortby`              | Name of column to sort by. Default is `estimate`.                                                                                                           |       |
| `flush`               | If True (default), left-flush variable labels and annotations.                                                                                              |          |
| `decimal_precision`   | Number of decimal places to print. (Default = 2)                                                                                                            |          |
| `figsize`             | Tuple indicating core figure size. Default is (4, 8)                                                                                                        |          |
| `xticks`              | List of xticklabels to print on x-axis.                                                                                                                     |       |
| `ylabel`              | Y-label title.                                                                                                                                              |      |
| `xlabel`              | X-label title.                                                                                                                                              |       |
| `color_alt_rows`      | If True, shade out alternating rows in gray.                                                                                                                |          |
| `preprocess`          | If True (default), preprocess the `dataframe` before plotting.                                                                                              |          |
| `return_df`           | If True, returned the preprocessed `dataframe`.                                                                                                             |          |

(*If `ll` *and* `hl` are specified, then the `moerror` (margin of error) is not required, and vice versa.)
<p align="right">(<a href="#top">back to top</a>)</p>

<!------------------------ KNOWN ISSUES ------------------------>
## Known Issues[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#known-issues)
* Variable labels coinciding with group variables may lead to unexpected formatting issues in the graph.
* Horizontal CI lines cannot be recast as capped horizontal lines because of the backend `Matplotlib` API used.
* Left-flushing of annotations relies on the `monospace` font.
* Plot can get cluttered with too many variables/rows (~30 onwards) 
<p align="right">(<a href="#top">back to top</a>)</p>

<!----------------- BACKGROUND AND ADDITIONAL RESOURCES ----------------->
## Background and Additional Resources[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#background-and-additional-resources)

**More about forest plots:**

[Forest plots](https://en.wikipedia.org/wiki/Forest_plot) have many aliases (h/t Chris Alexiuk). Other names include coefplots, coefficient plots, meta-analysis plots, dot-and-whisker plots, blobbograms, margins plots, regression plots, and ropeladder plots. 

[Forest plots](https://en.wikipedia.org/wiki/Forest_plot) in the medical and health sciences literature are plots that report results from different studies as a meta-analysis. Markers are centered on the estimated effect and horizontal lines running through each marker depicts the confidence intervals.

The simplest version of a forest plot has two columns: one for the variables/studies, and the second for the estimated coefficients and confidence intervals.
This layout is similar to coefficient plots ([coefplots](http://repec.sowi.unibe.ch/stata/coefplot/getting-started.html)) and is thus useful for more than meta-analyses.

<details><summary>Here are more resources about forest plots:</summary><p>

* [[1]](https://doi.org/10.1038/s41433-021-01867-6) Chang, Y., Phillips, M.R., Guymer, R.H. et al. The 5 min meta-analysis: understanding how to read and interpret a forest plot. Eye 36, 673–675 (2022).
* [[2]](https://doi.org/10.1136/bmj.322.7300.1479) Lewis S, Clarke M. Forest plots: trying to see the wood and the trees BMJ 2001; 322 :1479 
</p></details><p></p>

<details><summary>Related packages:</summary><p>

* [[1]](https://www.stata-journal.com/article.html?article=gr0059) [Stata] Jann, Ben (2014). Plotting regression coefficients and other estimates. The Stata Journal 14(4): 708-737. 
* [[2]](https://www.statsmodels.org/devel/examples/notebooks/generated/metaanalysis1.html) [Python] Meta-Analysis in statsmodels
* [[3]](https://github.com/seafloor/forestplot) [Python] Matt Bracher-Smith's Forestplot
* [[4]](https://github.com/fsolt/dotwhisker) [R] Solt, Frederick and Hu, Yue (2021) dotwhisker: Dot-and-Whisker Plots of Regression Results
* [[5]](https://rpubs.com/mbounthavong/forest_plots_r) [R] Bounthavong, Mark (2021) Forest plots. RPubs by RStudio
</p></details><p></p>

**More about this package:**

[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](http://numfocus.org)

The package is lightweight, built on `pandas`, `numpy`, and `matplotlib`.

It is slightly opinioniated in that the aesthetics of the plot inherits some of my sensibilities about what makes a nice figure.
You can however easily override most defaults for the look of the graph. This is possible via `**kwargs` in the `forestplot` API (see [Gallery and API options](#gallery-and-api-options)) and the `matplotlib` API.

**Planned enhancements** include forest plots each row can have multiple coefficients (e.g. from multiple models). 

<p align="right">(<a href="#top">back to top</a>)</p>


<!----------------------- CONTRIBUTING ----------------------->
## Contributing[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#contributing)

Contributions are welcome, and they are greatly appreciated!

**Potential ways to contribute:**

* Raise issues/bugs/questions
* Write tests for missing coverage
* Add features (see [examples notebook](https://nbviewer.org/github/LSYS/forestplot/blob/main/examples/readme-examples.ipynb) for a fuller enumeration of existing features)

**Issues**

Please submit bugs, questions, or issues you encounter to the [GitHub Issue Tracker](https://github.com/lsys/forestplot/issues).
For bugs, please provide a minimal reproducible example demonstrating the problem.

<p align="right">(<a href="#top">back to top</a>)</p>
