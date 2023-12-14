"""Main functions for coefficient plots (coefplots) of multiple regression models."""
from typing import Any, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

np.seterr(all="ignore")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.pyplot import Axes

from forestplot.arg_validators import check_data
from forestplot.dataframe_utils import reverse_dataframe, sort_groups
from forestplot.graph_utils import (  # draw_ci,; draw_est_markers,; draw_pval_right,; draw_ref_xline,; draw_ylabel1,; draw_yticklabel2,; right_flush_yticklabels,
    despineplot,
    draw_alt_row_colors,
    draw_tablelines,
    format_grouplabels,
    format_tableheader,
    format_xlabel,
    format_xticks,
    remove_ticks,
)
from forestplot.mplot_dataframe_utils import insert_group_model, make_multimodel_tableheaders
from forestplot.mplot_graph_utils import (
    mdraw_ci,
    mdraw_est_markers,
    mdraw_legend,
    mdraw_ref_xline,
    mdraw_yticklabel2,
    mdraw_yticklabels,
)
from forestplot.text_utils import (  # form_est_ci,; make_tableheaders,; star_pval,
    format_varlabels,
    indent_nongroupvar,
    normalize_varlabels,
    prep_annote,
    prep_rightannnote,
)

rcParams["font.monospace"] = [
    "Lucida Sans Typewriter",
    "DejaVu Sans Mono",
    "Courier New",
    "Lucida Console",
]


def mforestplot(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]] = None,
    modellabels: Optional[Union[Sequence[str], None]] = None,
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    groupvar: Optional[str] = None,
    group_order: Optional[Union[list, tuple]] = None,
    logscale: bool = False,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    pval: Optional[str] = None,
    capitalize: Optional[str] = None,
    starpval: bool = True,
    sort: bool = False,
    sortby: Optional[str] = None,
    flush: bool = True,
    decimal_precision: int = 2,
    figsize: Union[Tuple, List] = (4, 8),
    xticks: Optional[Union[list, range]] = None,
    ylabel: Optional[str] = None,
    xlabel: Optional[str] = None,
    yticker2: Optional[str] = None,
    color_alt_rows: bool = False,
    return_df: bool = False,
    preprocess: bool = True,
    table: bool = False,
    **kwargs: Any,
) -> Axes:
    _local_df = dataframe.copy(deep=True)
    _local_df = check_data(
        dataframe=_local_df,
        estimate=estimate,
        varlabel=varlabel,
        pval=None,
        ll=ll,
        hl=hl,
        groupvar=groupvar,
        group_order=group_order,
        annote=annote,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
    )
    if (ll is None) or (hl is None):
        ll, hl = "ll", "hl"
    if preprocess:
        _local_df = _mpreprocess_dataframe(
            dataframe=_local_df,
            estimate=estimate,
            varlabel=varlabel,
            ll=ll,
            hl=hl,
            model_col=model_col,
            models=models,
            capitalize=capitalize,
            groupvar=groupvar,
            group_order=group_order,
            annote=annote,
            annoteheaders=annoteheaders,
            rightannote=rightannote,
            right_annoteheaders=right_annoteheaders,
            pval=pval,
            starpval=starpval,
            sort=sort,
            sortby=sortby,
            flush=flush,
            decimal_precision=decimal_precision,
            **kwargs,
        )
    ax = _make_mforestplot(
        dataframe=_local_df,
        yticklabel="yticklabel",
        estimate=estimate,
        model_col=model_col,
        models=models,
        modellabels=modellabels,
        groupvar=groupvar,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
        figsize=figsize,
        xticks=xticks,
        ll=ll,
        hl=hl,
        logscale=logscale,
        flush=flush,
        ylabel=ylabel,
        xlabel=xlabel,
        yticker2=yticker2,
        color_alt_rows=color_alt_rows,
        table=table,
        **kwargs,
    )
    return _local_df, ax


def _mpreprocess_dataframe(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    ll: Optional[str],
    hl: Optional[str],
    groupvar: Optional[str] = None,
    group_order: Optional[Union[list, tuple]] = None,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    capitalize: Optional[str] = None,
    flush: bool = True,
    decimal_precision: int = 2,
    **kwargs: Any,
) -> pd.core.frame.DataFrame:
    """
    Preprocess the dataframe to be ready for plotting.

    Returns
    -------
    pd.core.frame.DataFrame
        Dataframe with additional columns for plotting.
    """
    if groupvar is not None:
        dataframe = sort_groups(dataframe, groupvar=groupvar, group_order=group_order)
        dataframe = insert_group_model(
            dataframe=dataframe, groupvar=groupvar, varlabel=varlabel, model_col=model_col
        )

    dataframe = normalize_varlabels(
        dataframe=dataframe, varlabel=varlabel, capitalize=capitalize
    )

    dataframe = indent_nongroupvar(dataframe=dataframe, varlabel=varlabel, groupvar=groupvar)

    if annote is None:  # Form ytickers = formatted variable labels
        dataframe = format_varlabels(
            dataframe=dataframe,
            varlabel=varlabel,
            form_ci_report=False,
            ci_report=False,
            groupvar=groupvar,
        )
    else:
        dataframe = prep_annote(
            dataframe=dataframe,
            groupvar=groupvar,
            varlabel=varlabel,
            annote=annote,
            annoteheaders=annoteheaders,
            **kwargs,
        )

    if rightannote is not None:
        dataframe = prep_rightannnote(
            dataframe=dataframe,
            groupvar=groupvar,
            varlabel=varlabel,
            rightannote=rightannote,
            right_annoteheaders=right_annoteheaders,
        )

    dataframe = make_multimodel_tableheaders(
        dataframe=dataframe,
        varlabel=varlabel,
        model_col=model_col,
        models=models,
        annote=annote,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
        flush=flush,
        **kwargs,
    )
    return reverse_dataframe(dataframe)  # since plotting starts from bottom


def _make_mforestplot(
    dataframe: pd.core.frame.DataFrame,
    yticklabel: str,
    estimate: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]],
    modellabels: Optional[Union[Sequence[str], None]],
    groupvar: str,
    xticks: Optional[Union[list, range]],
    ll: str,
    hl: str,
    logscale: bool,
    flush: bool,
    annoteheaders: Optional[Union[Sequence[str], None]],
    rightannote: Optional[Union[Sequence[str], None]],
    right_annoteheaders: Optional[Union[Sequence[str], None]],
    ylabel: str,
    xlabel: str,
    yticker2: Optional[str],
    figsize: Union[Tuple, List],
    despine: bool = True,
    color_alt_rows: bool = False,
    table: bool = False,
    **kwargs: Any,
) -> Axes:
    if models is None:
        models = dataframe[model_col].dropna().unique()
    if modellabels is None:
        modellabels = models

    _, ax = plt.subplots(figsize=figsize, facecolor="white")

    ax = mdraw_est_markers(
        dataframe,
        estimate=estimate,
        yticklabel=yticklabel,
        model_col=model_col,
        models=models,
        ax=ax,
        **kwargs,
    )
    ax = mdraw_ci(
        dataframe,
        estimate=estimate,
        yticklabel=yticklabel,
        ll=ll,
        hl=hl,
        model_col=model_col,
        models=models,
        logscale=logscale,
        ax=ax,
        **kwargs,
    )
    ax = mdraw_legend(models=models, modellabels=modellabels, ax=ax, xlabel=xlabel, **kwargs)

    format_xticks(
        dataframe=dataframe, estimate=estimate, ll=ll, hl=hl, xticks=xticks, ax=ax, **kwargs
    )
    mdraw_ref_xline(
        ax=ax,
        dataframe=dataframe,
        model_col=model_col,
        annoteheaders=annoteheaders,
        right_annoteheaders=right_annoteheaders,
        **kwargs,
    )
    df_subset = dataframe.query(f'{model_col}=="{models[-1]}"').reset_index(drop=True)
    mdraw_yticklabels(
        df_subset,
        yticklabel=yticklabel,
        model_col=model_col,
        models=models,
        flush=flush,
        ax=ax,
        **kwargs,
    )
    if rightannote is not None:
        ax, righttext_width = mdraw_yticklabel2(
            df_subset,
            annoteheaders=annoteheaders,
            right_annoteheaders=right_annoteheaders,
            ax=ax,
            **kwargs,
        )
    else:
        righttext_width = 0
    remove_ticks(ax)
    format_grouplabels(dataframe=dataframe, groupvar=groupvar, ax=ax, **kwargs)
    format_tableheader(
        annoteheaders=annoteheaders, right_annoteheaders=right_annoteheaders, ax=ax, **kwargs
    )

    format_xlabel(xlabel=xlabel, ax=ax, **kwargs)
    if color_alt_rows:
        draw_alt_row_colors(
            dataframe,
            groupvar=groupvar,
            annoteheaders=annoteheaders,
            right_annoteheaders=right_annoteheaders,
            ax=ax,
        )
    if (annoteheaders is not None) or (right_annoteheaders is not None):
        if table:
            draw_tablelines(
                dataframe=df_subset,
                righttext_width=righttext_width,
                pval=None,
                right_annoteheaders=right_annoteheaders,
                ax=ax,
                extrapad=0.03,  # To tune where the right tablelines start
                **kwargs,
            )
    if annoteheaders or right_annoteheaders:
        negative_padding = 1.0
    else:
        negative_padding = 0.5
    ax.set_ylim(-0.5, ax.get_ylim()[1] - negative_padding)
    despineplot(despine=despine, ax=ax)
    return ax
