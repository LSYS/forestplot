VERSION = (0, 2, 1)

__version__ = '.'.join(map(str, VERSION))

from forestplot.plot import forestplot
from forestplot.dataframe_utils import load_data
