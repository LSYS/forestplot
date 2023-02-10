"""State version and import user-facing functions."""
VERSION = (0, 2, 2)

__version__ = ".".join(map(str, VERSION))

from forestplot.dataframe_utils import load_data
from forestplot.plot import forestplot
