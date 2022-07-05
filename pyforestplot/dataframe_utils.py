import pandas as pd


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
