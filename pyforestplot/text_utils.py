import pandas as pd
import numpy as np
from typing import Union


def star_pval(
	dataframe: pd.core.frame.DataFrame,
	pval: str,
	starpval: bool,
	decimal_precision: int,
	thresholds: Union[list, tuple] = (0.01, 0.05, 0.1),
	symbols: Union[list, tuple] = ("***", "**", "*"),
	**kwargs,
) -> pd.core.frame.DataFrame:
	"""
	"Star" the p-values according to the thresholds and symbols.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	pval (str)
		Name of column containing the p-values.
	starpval (bool)
		If True, use 'thresholds' and 'symbols' to "star" the p-values.
	decimal_precision (int)
		Precision of 2 means we go from '0.1234' -> '0.12'.
	thresholds (list-like)
		List of thresholds to star p-values. Default, which is pretty conventional, is
		0.01, 0.05, 0.1.
	symbols (list-like)
		List of symbols corresponding to the stated thresholds. Can be stars (e.g. ***
		or can be letters, e.g. 'c', 'b', 'a'

	Returns
	-------
		pd.core.frame.DataFrame with additional column for 'formatted_pval'.
	"""
	if pval is not None:
		try:
			assert len(thresholds) == len(symbols)
		except Exception:
			print("Error: P-value thresholds and symbols list must be of same length.")
			sys.exit(1)

		for ix, row in dataframe.iterrows():
			val = row[pval]

			if (np.isnan(val)) or (val == "nan"):
				dataframe.loc[ix, "formatted_pval"] = ""
				continue

			if val >= 1:
				val = 1.00000000000000000

			dec_formatted_pval = round(val, decimal_precision)
			dataframe.loc[ix, "formatted_pval"] = str(dec_formatted_pval)

			if starpval:
				for iy, threshold in enumerate(thresholds):
					if val <= threshold:
						_pval = "".join([str(dec_formatted_pval), symbols[iy]])
						dataframe.loc[ix, "formatted_pval"] = _pval
						break

	return dataframe


def indent_nongroupvar(
	dataframe, varlabel, groupvar, varindent: int = 2, **kwargs
) -> pd.core.frame.DataFrame:
	"""
	Indent the non-group variable labels when the 'form_ci_report' option is switched off.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	varlabel (str)
		Name of column containing the variable label to be printed out.
	groupvar (str)
		Name of column containing group of variables.
	varindent (int)
		Amount of whitespace to indent the variables when grouping of variables is used.

	Returns
	-------
		pd.core.frame.DataFrame with nongroup variables in 'varlabel' indented by stated amount.
	"""
	if varindent > 0:
		if groupvar is not None:
			groups = [gr.lower() for gr in dataframe[groupvar].unique()]

			for ix, row in dataframe.iterrows():
				label = row[varlabel]
				if label.lower() not in groups:
					label = label.rjust(varindent + len(label))
					dataframe.loc[ix, varlabel] = label
		else:
			for ix, row in dataframe.iterrows():
				label = row[varlabel]
				label = label.rjust(len(label))
				dataframe.loc[ix, varlabel] = label

	return dataframe


def normalize_varlabels(
	dataframe: pd.core.frame.DataFrame,
	varlabel: str,
	capitalize: str = "capitalize",
	**kwargs,
) -> pd.core.frame.DataFrame:
	"""
	Normalize variable labels to capitalize or title form.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	varlabel (str)
		Name of column containing the variable label to be printed out.	
	capitalize (str)
		'capitalize' or 'title'
		See https://pandas.pydata.org/docs/reference/api/pandas.Series.str.capitalize.html

	Returns
	-------
		pd.core.frame.DataFrame with the varlabel column normalized.
	"""
	if capitalize:
		if capitalize == "title":
			dataframe[varlabel] = dataframe[varlabel].str.title()
		elif capitalize == "capitalize":
			dataframe[varlabel] = dataframe[varlabel].str.capitalize()
		elif capitalize == "lower":
			dataframe[varlabel] = dataframe[varlabel].str.lower()
		elif capitalize == "upper":
			dataframe[varlabel] = dataframe[varlabel].str.upper()
		elif capitalize == "swapcase":
			dataframe[varlabel] = dataframe[varlabel].str.swapcase()

	return dataframe


def format_varlabels(
	dataframe: pd.core.frame.DataFrame,
	varlabel: str,
	form_ci_report: bool,
	column2: str,
	groupvar: str,
	extrapad: int = 2,
	varindent: int = 2,
	**kwargs,
) -> pd.core.frame.DataFrame:
	"""
	Format the yticklabels as normalized variable labels + estimate + confidence interval if 
	form_ci_report = True. If form_ci_report = False, then just use the variable label.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	varlabel (str)
		Name of column containing the variable label to be printed out.
	form_ci_report (bool)
		If True, form the formatted confidence interval as a string.
	column2 (str)
		Name of column containing the second column of annotation to be printed.
	groupvar (str)
		Name of column containing group of variables.
	extrapad (int)
		Amount of padding between variable label and the estimate + confidence interval formatted string.
	varindent (int)
		Amount of whitespace to indent the variables when grouping of variables is used.

	Helpers
	-------
		_get_max_varlen
		_format_secondcolumn
		_remove_est_ci

	Returns
	-------
		pd.core.frame.DataFrame with an additional 'yticklabel' column.
	"""
	if form_ci_report | (column2 is not None):
		pad = _get_max_varlen(dataframe=dataframe, varlabel=varlabel, extrapad=extrapad)

	if form_ci_report & (column2 is None):
		for ix, row in dataframe.iterrows():
			var = row[varlabel]
			est_ci = row["est_ci"]

			if groupvar is not None:
				groups = [gr.lower() for gr in dataframe[groupvar].unique()]

				if var.lower() in groups:  # If row is a group header
					yticklabel = var.ljust(pad)
				else:  # indent variable labels
					# indent = ''.rjust(varindent)
					# yticklabel = ''.join([indent, var.ljust(pad),est_ci])
					yticklabel = "".join([var.ljust(pad), est_ci])
			else:
				yticklabel = "".join([var.ljust(pad), est_ci])

			dataframe.loc[ix, "yticklabel"] = yticklabel

	elif column2 is not None:
		dataframe = _format_secondcolumn(dataframe=dataframe, column2=column2)

		for ix, row in dataframe.iterrows():
			var = row[varlabel]
			annote = row[f"formatted_{column2}"]

			if groupvar is not None:
				groups = [gr.lower() for gr in dataframe[groupvar].unique()]

				if var.lower() in groups:  # If row is a group header
					yticklabel = var.ljust(pad)
				else:  # indent variable labels
					# already indented from indent_nongroupvar
					yticklabel = "".join([var.ljust(pad), annote])

			dataframe.loc[ix, "yticklabel"] = yticklabel

	else:
		dataframe["yticklabel"] = dataframe[varlabel]

	dataframe = _remove_est_ci(
		dataframe=dataframe, varlabel=varlabel, groupvar=groupvar
	)

	return dataframe


def _remove_est_ci(
	dataframe: pd.core.frame.DataFrame, varlabel: str, groupvar: str,
) -> pd.core.frame.DataFrame:
	"""
	Make rows for 'est_ci' and 'ci_range' empty string '' if row is a group variable label.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	varlabel (str)
		Name of column containing the variable label to be printed out.
	groupvar (str)
		Name of column containing group of variables.

	Returns
	-------
		pd.core.frame.DataFrame.
	"""
	if groupvar is not None:
		for ix, row in dataframe.iterrows():
			var = row[varlabel]
			grouplabel = row[groupvar]
			if (
				var.lower().strip() == grouplabel.lower().strip()
			):  # If row is a group header
				dataframe.loc[ix, "ci_range"] = ""
				dataframe.loc[ix, "est_ci"] = ""

	return dataframe


def _format_secondcolumn(
	dataframe: pd.core.frame.DataFrame, column2: str, ha: str = "right", **kwargs
) -> pd.core.frame.DataFrame:
	"""
	Format the non-CI column as an annotation. Right-align this column using the max length in the column.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	column2 (str)
		Name of column containing the second column of annotation to be printed.

	Helpers
	-------
		_get_max_varlen
	Returns
	-------
		pd.core.frame.DataFrame with an additional 'formatted_column2' column.	
	"""

	pad = _get_max_varlen(dataframe=dataframe, varlabel=column2, extrapad=0)

	for ix, row in dataframe.iterrows():
		annote = row[column2]
		if ha == "right":
			annote = str(annote).rjust(pad)
		else:
			annote = str(annote).ljust(pad)

		dataframe.loc[ix, f"formatted_{column2}"] = annote

	return dataframe


def _get_max_varlen(
	dataframe: pd.core.frame.DataFrame, varlabel: str, extrapad: int,
) -> int:
	"""
	Get max variable length in dataframe.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	varlabel (str)
		Name of column containing the variable label to be printed out.
	extrapad (int)
		Amount of padding between variable label and the estimate + confidence interval formatted string.

	Returns
	-------
		int
	"""
	max_varlen = 0
	for var in dataframe[varlabel]:
		try:
			varlen = len(var)
		except TypeError:
			continue
		if varlen > max_varlen:
			max_varlen = varlen
	pad = max_varlen + extrapad

	return pad


def prep_annote(
	dataframe: pd.core.frame.DataFrame,
	annote: Union[tuple, list],
	annoteheaders: Union[tuple, list],
	varlabel: str,
	groupvar: str,
	**kwargs,
) -> pd.core.frame.DataFrame:
	"""
	Prepare the additional columns to be printed as annotations. 

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	annote (list-like)
		List of columns to add as additional annotation in the plot.
	annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations.
	varlabel (str)
		Name of column containing the variable label to be printed out.
	groupvar (str)
		Name of column containing group of variables.

	Helpers
	-------
		_get_max_varlen

	Returns
	-------
		pd.core.frame.DataFrame with an additional formatted 'yticklabel' column.	
	"""
	lookup_annote_len = {}
	for ix, annotation in enumerate(annote):
		# Get max len for padding
		_pad = _get_max_varlen(dataframe=dataframe, varlabel=annotation, extrapad=0)
		if annoteheaders is not None:
			# Check that max len exceeds header length
			_header = annoteheaders[ix]
			if len(_header) > _pad:
				_pad = len(_header)

		lookup_annote_len[ix] = _pad

		for iy, row in dataframe.iterrows():
			_annotation = row[annotation]
			_annotation = str(_annotation).ljust(_pad)

			dataframe.loc[iy, f"formatted_{annotation}"] = _annotation

	# get max length for variables
	pad = _get_max_varlen(dataframe=dataframe, varlabel=varlabel, extrapad=0)

	if groupvar is not None:
		groups = [gr.lower() for gr in dataframe[groupvar].unique()]
	else:
		groups = []

	for ix, row in dataframe.iterrows():
		yticklabel = row[varlabel]
		if yticklabel.lower().strip() in groups:
			dataframe.loc[ix, "yticklabel"] = yticklabel
		else:
			yticklabel = yticklabel.ljust(pad)
			yticklabel = f"{yticklabel:}"
			for annotation in annote:
				_annotation = row[f"formatted_{annotation}"]
				yticklabel = " ".join([yticklabel, _annotation])

			dataframe.loc[ix, "yticklabel"] = yticklabel

	return dataframe


def prep_rightannnote(
	dataframe: pd.core.frame.DataFrame,
	rightannote: Union[tuple, list],
	right_annoteheaders: Union[tuple, list],
	varlabel: str,
	groupvar: str,
	**kwargs,
) -> pd.core.frame.DataFrame:
	"""
	Prepare the additional columns to be printed as annotations on the right. 

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	rightannote (list-like)
		List of columns to add as additional annotation on the right-hand side of the plot.
	right_annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations.
	varlabel (str)
		Name of column containing the variable label to be printed out.
	groupvar (str)
		Name of column containing group of variables.

	Helpers
	-------
		_get_max_varlen

	Returns
	-------
		pd.core.frame.DataFrame with an additional formatted 'yticklabel2' column.
	"""
	lookup_annote_len = {}
	for ix, annotation in enumerate(rightannote):
		# Get max len for padding
		_pad = _get_max_varlen(dataframe=dataframe, varlabel=annotation, extrapad=0)
		if right_annoteheaders is not None:
			# Check that max len exceeds header length
			_header = right_annoteheaders[ix]
			if len(_header) > _pad:
				_pad = len(_header)

		lookup_annote_len[ix] = _pad

		for iy, row in dataframe.iterrows():
			_annotation = row[annotation]
			_annotation = str(_annotation).ljust(_pad)

			dataframe.loc[iy, f"formatted_{annotation}"] = _annotation

	if groupvar is not None:
		groups = [gr.lower() for gr in dataframe[groupvar].unique()]
	else:
		groups = []

	for ix, row in dataframe.iterrows():
		yticklabel = row[varlabel]
		yticklabel2 = ""
		if yticklabel.lower().strip() in groups:
			dataframe.loc[ix, "yticklabel2"] = ""
		else:
			for annotation in rightannote:
				_annotation = row[f"formatted_{annotation}"]
				yticklabel2 = " ".join([yticklabel2, _annotation])

			dataframe.loc[ix, "yticklabel2"] = yticklabel2

	return dataframe

