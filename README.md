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
## Installation[![](./examples/images/pin.svg)](#installation)
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
## Quick start[![](./examples/images/pin.svg)](#quick-start)

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
