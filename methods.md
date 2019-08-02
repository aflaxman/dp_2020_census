Methods
=======

Differential privacy definition and history.

TopDown algorithm goal and high-level description.

The 7 key policy choices, and how they were set in the 2018 end-to-end
test.

Our Evaluation Approach
-----------------------

1. Calculate errors and their variance (for total count and
age/race/ethnicity stratified count for state, county, and
enum_district)

2. Calculate "empirical privacy loss" (which we have just invented for
the purposes of this paper) (for same groupings)

3. Search for bias, with our hypothesis that it appears differentially
with respect to diversity of spatial units.)

We compare the bias, variance, and privacy to a simpler, but
not-differentially-private approach to protecting privacy: simple
random sample of 1% total.


