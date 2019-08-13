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

Error in stratified count varied similarly.  
When $\epsilon = 0.25$, the median absolute error in SC
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
district and county level. The empirical privacy
loss for SC was roughly twice the empirical privacy loss
for TC and the county and enumeration district level.
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

FIGURE 1 AROUND HERE

Compared to 50% sample, ... (Figure 2)

FIGURE 2 AROUND HERE

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
(Figure 3)

FIGURE 3 AROUND HERE

