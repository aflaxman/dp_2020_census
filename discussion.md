Discussion
==========

For $\epsilon \geq 1.0$, TopDown introduced near minimal noise and
attained empirical privacy loss almost 10 times less than $\epsilon$,
but created a quantifiable amount of bias.  The bias increased the
reported counts in homogeneous districts while decreasing the counts
in racially and ethnically mixed districts.  The TopDown algorithm may
therefore drive some redistribution of resources from diverse urban
communities to segregated rural communities.

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
of respondants to answer census questions.[ref]

Limitations
-----------

There are many differences between the 1940 census data and the 2020
data to be collected next year. In addition to the US population being
three times larger now, the analysis will have six geographic levels
instead of four, ten times more race groups and ove r 60 times more
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






