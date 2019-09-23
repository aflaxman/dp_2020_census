Discussion
==========

We anticipate some readers of this will be social researchers who rely
on Census Bureau data for quantitative work, and who have concerns that
the Census Bureau is going to add noise to this data.  Such a reader may be open
to the possibility that privacy is a valid reason for adding this
noise, yet still be concerned about how this noise will affect their
next decade of research. Our results visually summarized in Figure 2
can help to understand what this noise will mean: if $\epsilon=1.0$, for
county-level stratified counts, TopDown will be like the noise
introduced by working with a 50% sample of the full dataset; if
$\epsilon=2.0$, it will like working with a 75% sample; and if $\epsilon=6.0$,
it will have accuracy matching a 95% sample, which is pretty close
to having the full data without noise.  Such a reader may still want
to see an analysis like this run on the 2010 decennial census data, but we hope
this will help them rest a little easier about the quality of the data
they are relying on for their work.

We also expect that some readers will be more drawn to the lower end
of the epsilon curve.  Just how private is TopDown with $\epsilon=0.25$, especially
when total count at the state-level is invariant? Our results show
that all $\epsilon$ less than 1.0 have empirical privacy loss around
0.15, independent of $\epsilon$.  You can add more and more noise, but,
perhaps due to the invariants, that noise is not translating into more
and more privacy.

For $\epsilon \geq 1.0$, we found that TopDown introduced near minimal noise and
attained empirical privacy loss almost 10 times less than $\epsilon$.  
We also found that this created a quantifiable amount of bias.  The bias increased the
reported counts in homogeneous districts while decreasing the counts
in racially and ethnically mixed districts.  The TopDown algorithm may
therefore drive some redistribution of resources from diverse urban
communities to segregated rural communities.  [More about the
hypothesis that bias is due to homogeneity, vs the theory that bias is
due to unit size.]

Accurate counts in small communities are important for emergency
preparedness and other routine planning tasks performed by state and
local government demographers, and this work may help to understand how
such work will be affected by the shift to a DP disclosure avoidance
system.

This work has not investigated more detailed research uses of
decennial census data in social research tasks, such as segregation
research, and how this may be affected by TopDown.

Another important use of decennial census data is in constructing
control populations and survey weights for survey sampling of the US
population for health, political, and public opinion polling.  Our
work provides some evidence on how TopDown may affect this
application, but further work is warranted.

This work still fits into the beginning of a discussion on how to best
balance privacy and accuracy in decennial census data collection, and
there is a need for continued discussion.  This need must be balanced
against a risky sort of observer bias---attitude surveys have found
that calling attention to the privacy and confidentiality of census
responses, even if done in a positive manner, reduces the willingness
of respondents to answer census questions.[ref]

Limitations
-----------

There are many differences between the 1940 census data and the 2020
data to be collected next year. In addition to the US population being
three times larger now, the analysis will have six geographic levels
instead of four, ten times more race groups and over 60 times more
age groups. We expect that this will yield detailed queries with
typical exact count sizes even smaller than the stratified counts for
enumeration districts we have examined here.  We suspect that impact
of this will likely be to slightly decrease accuracy and increase
privacy loss, but the accuracy of our hypothesis remains to be seen.

In addition to the changes in the data, additional changes are planned
for TopDown, such as a switch from independent geometric noise to the
High Dimensional Matrix Mechanism. We expect this to increase the
accuracy a small amount without changing the empirical privacy loss.

In this work, we have focused on the median of the absolute error, but
the spread of this distribution is important as well, and in future
work, researchers may wish to investigate the tails of this
distribution. We have also focused on the empirical privacy loss for
specific queries at specific geographic aggregations, and our
exploration was not comprehensive. Therefore, it is possible that some
other test statistic would demonstrate a larger empirical privacy loss
than we have found with our approach. Our approach also assumes that
the residuals for different locations is generalizable to the
residuals from the same location when run with different
data. Although these are certainly different, we suspect that the
difference is sufficiently small as to not affect our estimates
substantially.

Conclusion
==========

The TopDown algorithm will provide a provably $\epsilon$-DP disclosure
avoidance system for the 2020 US Census, and it provides affordances
to balances privacy and accuracy.  This is an opportunity, but it is
not without risks. Taking advantage of the opportunity and mitigating
the risks will require that we understand what the approach is doing,
and we hope that this analysis of the 2018 E2E test can help build
such understanding.






