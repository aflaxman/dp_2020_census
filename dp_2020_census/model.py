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
    error = t.count_new - t.count_orig

    return error

    
def empirical_privacy_loss(error, bandwidth=0.1, est_range_percentile=99, est_range_multiplier=1.5):
    """Calculate the empirical privacy loss based on observed measurement errors

    Parameters
    ----------

    error : pd.Series of measurement errors
    bandwidth : float, optional, passed as bw_method parameter in
                scipy.stats.gaussian_kde
    est_range_percentile : float, optional, used as upperbound and 
                           100-lowerbound percentile for estimation range
    est_range_multiplier : float, optional, used to scale percentile 
                           bound for estimation range
    
    Results
    -------

    returns pd.DataFrame of EPL and histogram, as well as smoothed versions

    """
    if len(error) == 0:
        return pd.DataFrame(columns=['hist', 'epl_hist', 'epl_cusum', 'smooth_hist', 'smooth_epl'])

    lb = np.percentile(error, 100-est_range_percentile)
    ub = np.percentile(error, est_range_percentile)
    bnd = est_range_multiplier*max(abs(lb), abs(ub))

    est_range = [-bnd, bnd]
    all_errors = error.values
    N = len(all_errors)

    f_empirical, bin_edges = np.histogram(all_errors, bins=np.arange(*est_range, 1))
    ratio = f_empirical[:-1] / f_empirical[1:]

    df = pd.DataFrame(index=.5*(bin_edges[:-2] + bin_edges[1:-1]))
    df['hist'] = f_empirical[:-1]
    df['epl_hist'] = np.log(ratio)

    ccusum = f_empirical.sum() - np.cumsum(f_empirical)
    df['epl_cusum'] = np.log(ccusum[1:] / ccusum[:-1])

    if np.allclose(all_errors.std(), 0):
        # can't do kde of all same thing
        df['smooth_hist'] = np.nan
        df['smooth_epl'] = np.inf
    else:
        kernel = scipy.stats.gaussian_kde(all_errors, bw_method=bandwidth)
        f_smoothed = N*kernel(.5 * (bin_edges[:-1] + bin_edges[1:]))
        ratio = f_smoothed[:-1] / f_smoothed[1:]
        df['smooth_hist'] = f_smoothed[:-1]
        df['smooth_epl'] = np.log(ratio)
    return df

def GDPC(epsilon, exact_counts):
    """ add Geometric noise, to make counts differentially private
    Parameters
    ----------
    epsilon : float-able
    exact_counts : pd.Series
    
    Results
    -------
    returns dp_counts, a pd.Series with index matching exact_counts
    """
    
    z = float(epsilon)

    all_errors = (np.random.geometric(z, size=len(exact_counts))
                    - np.random.geometric(z, size=len(exact_counts)))
    dp_counts = exact_counts + all_errors
    return dp_counts
