Discussion
==========

For $\epsilon \geq 1.0$, TopDown introduced near minimal noise and
attained empirical privacy loss almost 10 times less than $\epsilon$,
but created a quantifiable amount of bias.  The bias increased the
reported counts in homogeneous districts while decreasing the counts
in racially and ethnically mixed districts; since the errors are
similar in *absolute* scale, cities of sufficient size will likely not
notice who they have lost, but rural districts likely *will* notice or
at least benefit from the population count (and appropriations) that
they have gained.  The TopDown algorithm will likely drive some
redistribution of resources from diverse urban communities to
segregated rural communities.

The small communities that are likely to have upward bias in their
TopDown counts will be the ones small enough to benefit from the
quality Assurance processes that have been implemented in past
censuses, such as the Count Question Resolution program, and the
results in this paper can help anticipate and plan for this process.

Accurate counts in small communities are important for emergency
preparedness and other routine planning tasks performed by state and
local goverment demographers, and this work may help to understand how
such work will be affected by the shift to a DP disclosure avoidance
system.

This work has not investigated more detailed research uses of
decennial census data in social research tasks, such as segregation
research, and how this may be affected by TopDown.  On the other hand,
human subject research requires informed consent (Belmont Principles);
de-identified data is not HSR, but if it is re-identifiable, it should
not be considered de-identified, should it?

Another important use of decennial census data is in constructing
control populations and survey weights for survey sampling of the US
population for health, political, and public opinion polling.  This
work provides some evidence on how TopDown may affect this work, but
further work is warranted.

This work still fits into the beginning of a discussion on how to best
balance privacy and accuracy in decennial census data collection, and
there is a need for continued discussion.  This need must be balanced
against a risky sort of observer bias---attitude surveys have found
that calling attention to the privacy and confidentiality of census
responses, even if done in a positive manner, reduce willingness to
answer census questions.[ref]

Limitations
-----------

There are many differences between the 1940 census data and the 2020
data to be collected next year. Number of geographic levels, number of
strata to be included in detailed queries.

Additional changes are being planned, HDMM instead of geometric
mechanism, for example.

Our approach to quantifying error focused on the median absolute
error, and there are important tails to this distribution as well.

Our empirical privacy loss is not comprehensive, and there is the
possibility that some other perturbation or some other test statistic
would reveal a larger privacy loss than we have found with our
approach.  Our approach also assumes that the residuals for different
locations is generalizable to the residuals from the same location
when run with different data.  Although these are certainly different,
it is likely that the difference is sufficiently small as to not
affect our estimates substantially.




