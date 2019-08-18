
Results
=======

We found error in total count varied as a function of total privacy loss
budget. For
$\epsilon = 0.25$ produced median absolute error in TC of {tc_enum_dist_0_25_mae}
at the enumeration district level and {tc_county_0_25_mae} at the
county level;
$\epsilon = 1.0$ produced median absolute error in TC of {tc_enum_dist_1_0_mae}
at the enumeration district level and {tc_county_1_0_mae} at the
county level;
and $\epsilon = 4.0$ produced median absolute error in TC of {tc_enum_dist_4_0_mae}
at the enumeration district level and {tc_county_4_0_mae} at the
county level (Full table in Supplementary Appendix 1).
At the state level, there was TC error of $0.0$, as expected from the
state TC invariant. (Figure 1)

Error in stratified count varied similarly; When
$\epsilon = 0.25$, the median absolute error in SC
at the enumeration district level was {sc_enum_dist_0_25_mae} people,
at the county level was {sc_county_0_25_mae} people, and
at the state level was {sc_state_0_25_mae} people;
for $\epsilon = 1.0$, the median absolute error in SC
at the enumeration district level was {sc_enum_dist_1_0_mae} people,
at the county level was {sc_county_1_0_mae} people, and
at the state level was {sc_state_1_0_mae} people; and
for $\epsilon = 4.00$, the median absolute error in SC
at the enumeration district level was {sc_enum_dist_4_0_mae} people,
at the county level was {sc_county_4_0_mae} people, and
at the state level was {sc_state_4_0_mae} people.

We found that the empirical privacy loss was often substantially
smaller than the privacy loss budget.
For $\epsilon = 0.25$, the empirical privacy loss for TC
at the enumeration district level was {tc_privacy_loss_enum_dist_0_25_max_abs}
and at the county level was {tc_privacy_loss_county_0_25_max_abs}
(at the state level empirical privacy loss is undefined, since the invariant makes all error zero);
for $\epsilon = 1.0$, the empirical privacy loss for TC
at the enumeration district level was {tc_privacy_loss_enum_dist_1_0_max_abs}
and at the county level was {tc_privacy_loss_county_1_0_max_abs}; and
for $\epsilon = 4.0$, the empirical privacy loss for TC
at the enumeration district level was {tc_privacy_loss_enum_dist_4_0_max_abs}
and at the county level was {tc_privacy_loss_county_4_0_max_abs}.

This relationship between privacy loss budget and empirical privacy
loss was similar for stratified counts (SC) at the enumeration
district and county level, but for privacy loss budgets of 1.0 and less, the empirical privacy
at the enumeration district level was loss for SC was not as responsive to $\epsilon$.
For $\epsilon = 0.25$, the empirical privacy loss for SC
at the enumeration district level was {sc_privacy_loss_enum_dist_0_25_max_abs},
at the county level was {sc_privacy_loss_county_0_25_max_abs}, and
at the state level was {sc_privacy_loss_state_0_25_max_abs};
for $\epsilon = 1.0$, the empirical privacy loss for SC
at the enumeration district level was {sc_privacy_loss_enum_dist_1_0_max_abs},
at the county level was {sc_privacy_loss_county_1_0_max_abs}, and
at the state level was {sc_privacy_loss_state_1_0_max_abs}; and
for $\epsilon = 4.0$, the empirical privacy loss for SC
at the enumeration district level was {sc_privacy_loss_enum_dist_4_0_max_abs},
at the county level was {sc_privacy_loss_county_4_0_max_abs}, and
at the state level was {sc_privacy_loss_state_4_0_max_abs}.

![](fig_1_hist_epl.png "Figure 1 Error Histogram and Empirical Privacy Loss Function")

*Figure 1*: Panel (a) shows the distribution of error (DP - True) for
stratified counts at the enumeration district level, stratified by
age, race, and ethnicity; and panel (b) shows the empirical privacy
loss, $EPL(x) = \log\left(p(x) / p(x+1)\right),$
where $p(x)$ is the probability density corresponding to the
histogram in (a), after smoothing with a Gaussian kernel of bandwidth
$0.1$.

We found that the MAE and EPL of TopDown were similar to that
introduced by simple random sampling for $\epsilon \geq 1.0$.

To describe in words:

Total count
County
Enum Dist
Stratified Count
State
County
Enum Dist
(Figure 2)

![](fig_2_td_vs_srs.png "Figure 2 TopDown and Simple Random Sample")
*Figure 2*: The curve with circular markers shows that in TopDown, the
choice of $\epsilon$ controls the tradeoff between MAE and EPL,
although for $\epsilon < 1$ there is not much difference in EPL.  The
curve with square markers shows the MAE and EPL of Simple Random
Sampling for a range of sample sizes, for comparison.  For example,
TopDown with $\epsilon = 1.0$ provides privacy loss and estimation
error similar to a sample of 50% of the 1940 census data, while
$\epsilon = 2.0$ is comparable to a 75% sample (for counts stratified
by age, race, and ethnicity at the county level; different aggregate
statistics produce different curves).

The bias introduced by TopDown varied with diversity index, as
hypothesized.
Enumeration districts with only X empty strata had TC
and SC systematically lower than ground truth, while enumeration
districts with X empty strata had TC and SC systematically higher.
The size of this bias decreased as a function of $\epsilon$, from
tc_bias_enum_dist_X_0_25 for $\epsilon = 0.25$ to 
tc_bias_enum_dist_X_4_00 for $\epsilon = 4.0$.

Counties displayed the same general pattern, but there are fewer
counties and they typically have less empty strata, so it was not as
pronounced.
The size of this bias again decreased as a function of $\epsilon$, from
tc_bias_county_X_0_25 for $\epsilon = 0.25$ to 
tc_bias_county_X_4_00 for $\epsilon = 4.0$.

County diversity is correlated with county size [measure of correlation here], and we found a relationship between bias as county size as well.  (Or should figure be simply diversity?  or percent White?)
(Figure 3)

FIGURE 3 AROUND HERE -- error or absolute error on y-axis, diversity or size or whiteness on x



