<div id="top"></div> 
<h1 align="center" >
  <strong>Forestplot</strong>
</h1>
<!----------------- PROJECT SHIELDS ----------------->
<p align="center">
  <a href="https://pypi.org/project/forestplot">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/forestplot?label=Python&logo=python&logoColor=white">
  </a><br>
  <b>Easy API for forest plots.</b><br>
  A Python package to make publication-ready but customizable forest plots.
</p>

<p align="center"><img width="100%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/main.png"></p>

-----------------------------------------------------------

This package makes publication-ready forest plots easy to make out-of-the-box. Users provide a `dataframe` (eg from a spreadsheet) where rows correspond to a variable/study with columns for estimates, confidence intervals, etc. (see below for example).
Additional options allow easy addition of columns in the `dataframe` as annotations in the plot.

|    |    |
| --- | --- |
| Release | [![PyPI](https://img.shields.io/pypi/v/forestplot?color=blue&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/forestplot/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/lsys/forestplot?color=blue&label=Latest%20release)](https://github.com/LSYS/forestplot/releases) |
| Status | [![CI](https://github.com/LSYS/forestplot/actions/workflows/CI.yml/badge.svg)](https://github.com/LSYS/forestplot/actions/workflows/CI.yml) [![Notebooks](https://github.com/LSYS/forestplot/actions/workflows/nb.yml/badge.svg)](https://github.com/LSYS/forestplot/actions/workflows/nb.yml) |
| Coverage |  [![Codecov](https://img.shields.io/codecov/c/github/lsys/forestplot?logo=codecov&logoColor=white)](https://app.codecov.io/gh/LSYS/forestplot) |
| Docs | [![Documentation Status](https://readthedocs.org/projects/forestplot/badge/?version=latest)](https://forestplot.readthedocs.io/en/latest/?badge=latest) |
| Python | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/forestplot?label=Python%203.6%2B&logo=python&logoColor=white)](https://pypi.org/project/forestplot/) |
| Meta | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) |

<!----------------- TABLE OF CONTENT ----------------->
<details open><summary><b>Table of Contents</b></summary><p>

> - [Installation](#installation)
> - [Quick Start](#quick-start)
> - [Some Examples with Customizations](#some-examples-with-customizations)
> - [Gallery and API Options](#gallery-and-api-options)
> - [Known Issues](#known-issues)
> - [Background and Additional Resources](#background-and-additional-resources)
> - [Contributing](#contributing)
</p></details><p></p>

<!------------------- INSTALLATION ------------------->
## Installation[![](https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/pin.svg)](#installation)
Install from PyPI

<a href="https://pypi.org/project/forestplot">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/forestplot?color=blue&label=PyPI&logo=pypi&logoColor=white">
</a>

```bash
pip install pyforestplot
```

Install from source
```bash
git clone https://github.com/LSYS/forestplot.git
cd forestplot
pip install .
```
<p align="right">(<a href="#top">back to top</a>)</p>


<!-------------------- QUICK START -------------------->
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

The example input `dataframe` above have 4 key columns:

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
<p align="left"><img width="65%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/vanilla.png"></p>

<p align="right">(<a href="#top">back to top</a>)</p>


<!----------------- EXAMPLES of CUSTOMIZATIONS ----------------->
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

<p align="left"><img width="80%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/leftannote-rightannote-table.png"></p>

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
<p align="left"><img width="35%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/vcoefplot.png"></p>

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
<p align="left"><img width="75%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/main.png"></p>

<details><summary><i>Annotations arguments allowed include:</i></summary>
  
  * `ci_range`: Confidence interval range (e.g. (-0.39 to -0.25)).
  * `est_ci`: Estimate and CI (e.g. -0.32(-0.39 to -0.25)).
  * `formatted_pval`: Formatted p-values (e.g. 0.01**).
  
  To confirm what columns are available, you can do:
  
  ```python
  processed_df, ax = fp.forestplot(df, 
                                   ...
                                   return_df=True # return processed dataframe with processed columns
                                  )
  processed_df.head(3)
  ```
  
  |    | label                | group         |   n |          r | CI95%         |       p-val |      BF10 |   power | var    |    hl |    ll |   moerror |   formatted_r |   formatted_ll |   formatted_hl | ci_range         | est_ci                | formatted_pval   |   formatted_n |   formatted_power | formatted_est_ci      | yticklabel                                                        | formatted_formatted_pval   | formatted_group   | yticklabel2            |
|---:|:---------------------|:--------------|----:|-----------:|:--------------|------------:|----------:|--------:|:-------|------:|------:|----------:|--------------:|---------------:|---------------:|:-----------------|:----------------------|:-----------------|--------------:|------------------:|:----------------------|:------------------------------------------------------------------|:---------------------------|:------------------|:-----------------------|
|  0 | Mins worked per week | Labor factors | 706 | -0.321384  | [-0.39 -0.25] | 1.99409e-18 | 1.961e+15 |    1    | totwrk | -0.25 | -0.39 | 0.0686165 |         -0.32 |          -0.39 |          -0.25 | (-0.39 to -0.25) | -0.32(-0.39 to -0.25) | 0.0***           |           706 |              1    | -0.32(-0.39 to -0.25) | Mins worked per week            706  1.0    -0.32(-0.39 to -0.25) | 0.0***                     | Labor factors     | 0.0***   Labor factors |
|  1 | Years of schooling   | Labor factors | 706 | -0.0950039 | [-0.17 -0.02] | 0.0115515   | 1.137     |    0.72 | educ   | -0.02 | -0.17 | 0.0749961 |         -0.1  |          -0.17 |          -0.02 | (-0.17 to -0.02) | -0.10(-0.17 to -0.02) | 0.01**           |           706 |              0.72 | -0.10(-0.17 to -0.02) | Years of schooling              706  0.72   -0.10(-0.17 to -0.02) | 0.01**                     | Labor factors     | 0.01**   Labor factors |
  
</details>
