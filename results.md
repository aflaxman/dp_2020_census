Results
=======

We found error in total count varied as a function of total privacy loss
budget. For
$\epsilon = 0.25$ produced mean TC error of {tc_error_enum_dist_0_25}
at the enumeration district level and {tc_error_county_0_25} at the
county level;
$\epsilon = 1.0$ produced mean TC error of {tc_error_enum_dist_1_00}
at the enumeration district level and {tc_error_county_1_00} at the
county level;
and $\epsilon = 4.0$ produced mean TC error of {tc_error_enum_dist_4_00}
at the enumeration district level and {tc_error_county_4_00} at the
county level (Full table in Supplementary Appendix 1).
At the state level, there was TC error of $0.0$, as expected from the
state TC invariant. (Figure 1)

Error in stratified count varied similarly.  
When $\epsilon = 0.25$, the mean SC error 
at the enumeration district level was {sc_error_enum_dist_0_25} people,
at the county level was {sc_error_county_0_25} people, and
at the state level was {sc_error_state_0_25} people;
for $\epsilon = 1.0$, the mean SC error 
at the enumeration district level was {sc_error_enum_dist_1_00} people,
at the county level was {sc_error_county_1_00} people, and
at the state level was {sc_error_state_1_00} people; and
for $\epsilon = 4.00$, the mean SC error 
at the enumeration district level was {sc_error_enum_dist_4_00} people,
at the county level was {sc_error_county_4_00} people, and
at the state level was {sc_error_state_4_00} people.

We found that the empirical privacy loss was often substantially
smaller than the privacy loss budget.
For $\epsilon = 0.25$, the empirical privacy loss for TC
at the enumeration district level was {tc_privacy_loss_enum_dist_0_25},
at the county level was {tc_privacy_loss_county_0_25}, and
at the state level was {tc_privacy_loss_state_0_25};
for $\epsilon = 1.0$, the empirical privacy loss for TC
at the enumeration district level was {tc_privacy_loss_enum_dist_1_00},
at the county level was {tc_privacy_loss_county_1_00}, and
at the state level was {tc_privacy_loss_state_1_00}; and
for $\epsilon = 4.0$, the empirical privacy loss for  TC
at the enumeration district level was {tc_privacy_loss_enum_dist_4_00},
at the county level was {tc_privacy_loss_county_4_00}, and
at the state level was {tc_privacy_loss_state_4_00}.

This relationship between privacy loss budget and empirical privacy
loss was similar for stratified counts (SC) at the enumeration
district and county level. At the state level, the empirical privacy
loss for SC was substantially smaller than the empirical privacy loss
for TC (Census Bureau used state-level TC as an invariant, which makes
the formal privacy loss infinite for this quantity).
For $\epsilon = 0.25$, the empirical privacy loss for SC
at the enumeration district level was {sc_privacy_loss_enum_dist_0_25},
at the county level was {sc_privacy_loss_county_0_25}, and
at the state level was {sc_privacy_loss_state_0_25};
for $\epsilon = 1.0$, the empirical privacy loss for SC
at the enumeration district level was {sc_privacy_loss_enum_dist_1_00},
at the county level was {sc_privacy_loss_county_1_00}, and
at the state level was {sc_privacy_loss_state_1_00}; and
for $\epsilon = 4.0$, the empirical privacy loss for SC
at the enumeration district level was {sc_privacy_loss_enum_dist_4_00},
at the county level was {sc_privacy_loss_county_4_00}, and
at the state level was {sc_privacy_loss_state_4_00}.

FIGURE 1 AROUND HERE

Compared to 50% sample, ... (Figure 2)

FIGURE 2 AROUND HERE

The bias introduced by TopDown varied with diversity index, as
hypothesized.
Enumeration districts with only X empty strata had TC
and SC systematically lower than ground truth, while enumeration
districts with X empty strata had TC and SC systematically higher.
The size of this bias decreased as a function of $\epsilon$, from
{tc_bias_enum_dist_X_0_25} for $\epsilon = 0.25$ to 
{tc_bias_enum_dist_X_4_00} for $\epsilon = 4.0$.

Counties displayed the same general pattern, but there are fewer
counties and they typically have less empty strata, so it was not as
pronounced.
The size of this bias again decreased as a function of $\epsilon$, from
{tc_bias_county_X_0_25} for $\epsilon = 0.25$ to 
{tc_bias_county_X_4_00} for $\epsilon = 4.0$.
(Figure 3)

FIGURE 3 AROUND HERE

