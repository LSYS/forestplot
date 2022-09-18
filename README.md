<div id="top"></div> 
<h1 align="center" >
  <strong>Forestplot</strong>
</h1>
<h4 align="center">Easy API for forest plots.</h3>
<p align="center">A python package to make publication-ready but customizable forest plots.</p>

<!----------------- PROJECT SHIELDS ----------------->
<p align="center">
  <a href="https://pypi.org/project/forestplot">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/forestplot?label=Python&logo=python&logoColor=white">
  </a>
  <br>
</p>

-----------------------------------------------------------

<p align="center"><img width="85%" src="https://raw.githubusercontent.com/LSYS/forestplot/main/docs/images/main.png"></p>


<!----------------- TABLE OF CONTENT ----------------->
<details open><summary><b>Table of Contents</b></summary><p>

> - [Installation](#installation)
> - [Quick start](#quick-start)
> - [Examples with Customizations](#examples-with-customizations)
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

