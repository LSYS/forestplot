import pandas as pd
from typing import Optional


def insert_groups(
	dataframe: pd.core.frame.DataFrame,
	groupvar: str,
	varlabel: str
) -> pd.core.frame.DataFrame:
	"""
	Insert the name of variable groups as a psuedo variable in the dataframe.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	groupvar (str)
		Name of column containing group of variables.
	varlabel (str)
		Name of column containing the variable label to be printed out.

	Returns
	-------
		pd.core.frame.DataFrame with group variable labels inserted as psuedo variables.
	"""
	
	df_groupsasvar = pd.DataFrame()

	for group in dataframe[groupvar].unique():
		_df = dataframe.query(f'{groupvar}==@group')
		addgroupvar = pd.DataFrame({varlabel: [group], groupvar: [group]})
		df_groupsasvar = pd.concat([df_groupsasvar, addgroupvar, _df], ignore_index=True)


	return df_groupsasvar


def sort_data(
	dataframe: pd.core.frame.DataFrame,
	estimate: str,
	groupvar: str,
	sort: bool = False,
	sortby: Optional[str] = None,
	sortascend: bool = True,
	**kwargs
) -> pd.core.frame.DataFrame:
	"""
	Sort the dataframe according to the stated options.

	Parameters
	----------

	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	estimate (str)
		Name of column containing the estimates (e.g. pearson correlation coefficient,
		OR, regression estimates, etc.).
	groupvar (str)
		Name of column containing group of variables.
	sort (bool)
		If True, sort rows by estimate size
	sortby (str)
		Name of column to sort the dataframe by. Default is 'estimate'.
	sortascend (bool)
		Sort in ascending order.

	Returns
	-------
		pd.core.frame.DataFrame that is sorted by the stated options.
	"""
	
	if sort or (sortby is not None):
		if sortby is None:
			sortby = estimate

		if groupvar is not None:
			dataframe.sort_values([groupvar, sortby], ascending=sortascend, inplace=True)
		else:
			dataframe.sort_values(sortby, ascending=sortascend, inplace=True)

		dataframe.reset_index(drop=True, inplace=True)

	return dataframe


def reverse_dataframe(
	dataframe: pd.core.frame.DataFrame
) -> pd.core.frame.DataFrame:
	"""Flip the dataframe so that last row is now first and so on."""
	dataframe = dataframe[::-1]
	return dataframe.reset_index(drop=True)	


def load_data(name: str, **param_dict) -> pd.core.frame.DataFrame:
    """
	Load example dataset for quickstart.

	Example data available now:
		- mortality
	
	The source of these data will be from: https://github.com/LSYS/pyforestplot/tree/main/examples/data.
		
	Parameters
	----------
	name (str)
		Name of the example data set.

	Returns
	-------
	pd.core.frame.DataFrame.
	"""

    available_data = ["mortality"]

    name = name.lower().strip()

    if name in available_data:
        url = f"https://raw.githubusercontent.com/lsys/pyforestplot/main/examples/data/{name}.csv"
        df = pd.read_csv(url, **param_dict)
        return df
    else:
        available_data_str = ", ".join(available_data)
        raise AssertionError(
            f"{name} not found. Should be one of '{available_data_str}'"
        )
