"""dp_2020_census.model

Code to calculate error from perturbations, simulation simple random
sampling and other non-DP methods of DAS, and summarize results
suitably for publication

"""

import numpy as np, matplotlib.pyplot as plt, pandas as pd
import scipy.stats

def perturbation_error(df_orig, df_new, stratification_cols=['state', 'county']):
    """Calculate the error for the counts in df_new with respect to the
    counts in df_orig, when stratified by stratification cols

    Parameters
    ----------

    df_orig : pd.DataFrame, the original count data, including a column called "count"
    df_new : pd.DataFrame, the perturbed count data, with columns matching df_orig
    stratification_cols : list, the columns on which to stratify when calculating the errors

    Results
    -------

    returns pd.Series with multi-index of stratification columns, and
    values quantifying the error for each noisy measurement

    """

    assert len(stratification_cols) > 0, 'at least one stratification columns is required'

    cnt_orig = df_orig.groupby(stratification_cols)['count'].sum()
    cnt_new = df_new.groupby(stratification_cols)['count'].sum()

    t = pd.merge(cnt_orig, cnt_new,
                 left_index=True, right_index=True,
                 how='outer', suffixes=('_orig', '_new')
             )
    t = t.fillna(0)
    error = t.count_orig - t.count_new

    return error

    
def empirical_privacy_loss(error):
    """Calculate the empirical privacy loss based on observed measurement errors

    Parameters
    ----------

    error : pd.Series of measurement errors
    
    Results
    -------

    returns pd.DataFrame of EPL and histogram, as well as smoothed versions

    """

    lb = np.percentile(error, 2.5)
    ub = np.percentile(error, 97.5)
    bnd = 1.5*max(abs(lb), abs(ub))

    est_range = [-bnd, bnd]
    all_errors = error.values
    N = len(all_errors)

    f_empirical, bin_edges = np.histogram(all_errors, bins=np.arange(*est_range, 1))
    ratio = f_empirical[:-1] / f_empirical[1:]

    df = pd.DataFrame(index=.5*(bin_edges[:-2] + bin_edges[1:-1]))
    df['hist'] = f_empirical[:-1]
    df['epl'] = np.log(ratio)

    kernel = scipy.stats.gaussian_kde(all_errors)
    f_smoothed = N*kernel(.5 * (bin_edges[:-1] + bin_edges[1:]))
    ratio = f_smoothed[:-1] / f_smoothed[1:]
    df['smooth_hist'] = f_smoothed[:-1]
    df['smooth_epl'] = np.log(ratio)
    return df

