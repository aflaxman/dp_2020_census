Acronyms
========

* DP - differentially private
* E2E - end-to-end
* TC - total count
* SC - stratified count
* MAE - median absolute error
* EPL - empirical privacy loss

Introduction
============

In the United States, the Decennial Census is an important part of
democratic governance.  Every ten years, the US Census Bureau is
constitutionally required to count the "whole number of persons in
each State", and in 2020 this effort is likely to cost over fifteen
billion dollars.[@garfinkel2019understanding][@gao2018census] The results will be used for apportioning representation
in the US House of Representatives, for dividing federal tax dollars
between states, as well as for a multitude of other governmental
activities at the national, state, and local level.  Data from the
decennial census will also be used extensively by sociologists,
economists, demographers, and other researchers, and it will also
inform strategic decisions in the private and non-profit sectors, and
facilitate the accurate weighting of subsequent population surveys for
the next decade.[@ruggles2019differential]

The confidentiality of information in the decennial census is also
constitutionally mandated, and the 2020 US Census will use a novel
approach to "disclosure avoidance" to protect respondents' data.[@abowd2018disclosure] This
approach builds on Differential Privacy, a mathematical
definition of privacy and privacy loss that has been developed over
the last decade and a half in the theoretical computer science and
cryptography communities.[@dwork2014algorithmic] Although the new approach allows a more
precise accounting of the noise introduced by the process, it also
risks reducing the utility of census data---it may produce counts that
are substantially noisier than the previous disclosure avoidance
system, which was based on a technique called swapping, and relied on
the detailed of the swapping procedure being secret.[@mckenna2018disclosure]

To date, there is a lack of empirical examination of the new disclosure avoidance system
but the approach was applied to the 2018 end-to-end (E2E) test of the
decennial census, and computer code used for this test as well as
accompanying exposition has recently been released publicly by the
Census Bureau.[@abowd2018disclosure][@boyd2019differential]

We used the recently released code, preprints, and data files to understand and
quantify the error introduced by the E2E disclosure avoidance system
when Census Bureau applied it to 1940 census data
(for which the full data has previously been released)
for a range of privacy loss budgets.  We also developed an empirical
measure of privacy loss and used it to compare the error and privacy
of the new approach to that of a simple-random-sampling approach to
protecting privacy.


Methods
=======

_Differential privacy definition and history._  A randomized algorithm for
analyzing a database is _differentially private_ (DP) if withholding or changing one
person's data does not substantially change the algorithm's
output. If the results of the computation are roughly the same whether
or not my data are included in the database, then the computation must
be protecting my privacy. DP algorithms come with a parameter $\epsilon$,
which quantifies how much privacy loss is allowed, meaning how much
can one person's data to affect the analysis.

To be precise, randomized algorithm $\mathcal{A}$ is
$\epsilon$-differentially private if, for each possible output
$\mathcal{P}$, for any pair of datasets $D$ and $D'$ that are the same
everywhere except for on one person's data,
$$
\Pr\left[\mathcal{A}(D) = \mathcal{P}\right]
\leq \exp\left(\epsilon\right)
\Pr\left[\mathcal{A}(D') = \mathcal{P}\right].
$$

Differential privacy is a characteristic of an algorithm; it is not a
specific algorithm. For census counting tasks such a producing
histograms of the total count of people in each state, or counts of
people stratified by census block, age-group, race, and ethnicity,
differential privacy is often implemented by adding noise to the
counts.

The new disclosure avoidance system for the 2020 US Census is designed
to be DP and to maintain the accuracy of census
counts. To complicate things beyond the typical challenge faced in
DP algorithm design, there are certain counts in
the census that will be published exactly as enumerated, without any
variation caused by adding noise.  These _invariants_ have not been selected
for the 2020 decennial census yet, but in the 2018 end-to-end (E2E) test, the total
count for each state and the number of households in each enumeration
district where invariants.  There are also inequalities that will be
enforced, such as requiring the total count of people in an
enumeration district to be greater or equal to the number of occupied
households in that district.

_TopDown algorithm._ At a high level,
the census approach to this challenge repeats two steps for multiple
levels of a geographic hierarchy (from the top down, hence their name
"TopDown"). The first step (Noisy Histogram) adds noise from a carefully chosen
distribution to the data counts.
This produces a set of
noisy counts. The noisy counts might have negative counts or
violate invariants or other inequalities.  The second step (Optimize) finds the
tuned-up histogram that minimizes a quadratic objective function, subject to
constraints from a system of linear equations and inequalities that
represent the invariants, inequalities, consistency with the DP counts
from one level higher, and non-negativity. The solution to
this constrained optimization is as close to the noisy counts as
possible while also satisfying internal consistency.
The final output of TopDown is a synthetic
data set that has data counts matching the values that minimize
the constrained optimization.  This is $\epsilon$-DP
and also satisfies the invariants and inequalities using an approach that affords detailed
control of how the privacy budget is distributed between and within levels
of the hierarchy.

The census data has six geographic levels, nested hierarchically: national, state,
county, census tracts, block groups, and blocks. The census's
DP algorithm uses a top-down approach to create
the synthetic data; steps one and two are performed six times,
from the coarsest to the finest level. Each level is assigned a
privacy budget $\epsilon_i$ and the entire algorithm achieves
$\epsilon$-DP for $\epsilon=\sum_{i=1}^6
\epsilon_i.$

At a specific geographic level (say census tracts) the true data has
the form of a histogram; a set of boxes each labeled with a geographic
unit (e.g. census tract one), a race combination (e.g. Black), one sex
(e.g. Female), and one age (e.g. 46). Although the 2020 census will
include more variables, the 1940 data run with E2E test code
included the following: race (6 mutually exclusive categories), ethnicity
(non-Hispanic and Hispanic), age group (under-18 and 18-and-over),
and group quarters (2 categories).
The number in the box, which we call a histogram count, is the number
of people in the geographic unit with the features of the label
(e.g. the number of 18-and-over non-Hispanic White women in
enumeration district 107). Step one adds geometrically distributed
random noise to numbers in each box according to the privacy budget at
the level $\epsilon_i$. This noisy data is unsatisfactory because the
noisy counts (i) are sometimes negative, (ii) do not satisfy the
invariants or inequalities, and (iii) are inconsistent with the synthetic data
produced at the coarser level (e.g. the sum of the noisy counts in all
the boxes corresponding to a census tract within Cook county may not
equal the number of people in Cook County reported in the synthetic
data produced in the previous level.) Step two solves an
optimization problem which adjusts the counts in boxes so that they
are non-negative integers, satisfy the invariants and inequalities, are consistent with the
synthetic data produced at the coarser level, and are as close as
possible to the noisy counts.

### Step One: Noisy Histogram

In the E2E algorithm applied to the 1940s microdata, TopDown added random
noise in a flexible way that allowed the user to choose what
statistics are the most important to keep accurate. The noise was
added to the histogram counts for the level and also to a preselected
set of aggregate statistics.
Aggregate statistics are sets of histogram count sums specified by
some characteristics. For example, the ``ethnicity-age" aggregate
statistic contains set of four counts: people of Hispanic ethnicity under age 18, of Hispanic ethnicity age 18 and over,
of non-Hispanic ethnicity under age 18, and of non-Hispanic ethnicity age 18 and over. Census Bureau researchers have discussed plans to
include each value that will appear in a tabular summary in the set of
aggregate statistics.  The E2E test included two such aggregate statistics (internally called "DP queries"): a group-quarters query, 
which increases the accuracy of the count of each household type at
each level of the hierarchy, and a race/ethnicity/age query, which
increases the accuracy of the stratified counts of people by race,
ethnicity, and voting age across all household/group quarters types (again
for each level of the spatial hierarchy). It also included "detailed queries" corresponding to boxes in the histogram.
The detailed queries were
afforded 10% of the privacy budget at each level, while the DP queries
split the remaining 90% of the privacy budget, with 22.5% spent on the
group-quarters queries and 67.5% spend on the race/ethnicity/age
queries.

The epsilon budget of the level governed how much total random noise to
add. A further parameterization of the epsilon budget determined how the
noise was allocated between the histogram counts and each type of
aggregate statistic. We write $\epsilon_i = h + s_1 + s_2 + \ldots +
s_k$, where $\epsilon_i$ was the budget for the geographic level, $h$
was the budget for the histogram counts, and $s_1, \dots s_k$ were the
budgets for each of the $k$ types of aggregate statistics. Then noise
was added independently to each histogram count and aggregate statistic
according to the follow distribution:


$$\text{noisy histogram count} = \text{true histogram count} + G(h/2)
$$
$$\text{noisy aggregate stat $j$} = \text{ true aggregate stat $j$} + G(s_j/2)
$$

where $G(z)$ denotes the geometric distribution,

$$\Pr[G(z)=k] = \frac{(1 - \exp(-z))\exp(-z|k|)}{1 + \exp(-z)}.$$

The noisy counts and noisy aggregate statistics are unbiased
estimates with variance $(1-\exp(-z))^2/ (2 \exp(-z))$, where $z$ is
the parameter for the geometric noise added. A higher privacy budget
means the noise added is more concentrated around zero, and therefore
the corresponding statistic is more accurate. Therefore, adjusting the
privacy budgets of the various aggregate statistics gives control over
which statistics are the most private/least accurate (low fraction of
the budget) and the most accurate/least private (high fraction of the
budget).

The noise added to each histogram count comes from the same
distribution, and is independent of all other added noise;
the noise does not scale with the magnitude of count,
e.g. adding 23 people to the count of age 18 and older
non-Hispanic Whites is just as likely as adding 23 people
to the count of age under 18 Hispanic Native Americans, even though the
population of the latter is smaller.

Although the E2E test used independent geometric noise for each
detailed query and DP query at each level, the version of TopDown for
the 2020 Census DAS will likely use the High Dimensional Matrix
Mechanism [@chen2015differentially], which may reduce the variance of the noise.

### Step Two: Optimize

In this step, the synthetic data is created from the noisy data by
optimizing a quadratic objective subject to a system of linear
equations and inequalities. The algorithm creates a variable for each
histogram count and each aggregate statistic. It adds equations and inequalities
to encode the requirements that (i) each count and
aggregate statistic is non-negative, (ii) the invariants and inequalities are
satisfied, (iii) the aggregate statistics are the sum of the
corresponding histogram counts, and (iv) the statistics are consistent
with the higher level synthetic data counts (i.e. the total number of people aged 18 and over
summed across the counties in a state is equal to the number of people aged 18 and over in
that state as reported by synthetic data set constructed in the
previous phase). The optimization step finds a solution that satisfies
these equations and has the property that the value of each variable
is as close as possible to the corresponding noisy histogram count or
noisy aggregate statistic. This is done in a way that favors closeness
for the noisy values constructed by adding noise from a lower variance
geometric distribution.

The solution to this optimization is not necessarily integral, however,
and TopDown uses a second optimization step to round
fractional counts to integers. In this optimization, the linear
equations and inequalities all correspond to those in the previous
optimization, and the objective function is changed to minimize $(1 -
2(x_i - \lfloor x_i \rfloor)) z_i$, where each $x_i$ corresponds to a
(potentially non-integer) detailed query count given in the synthetic
data and $z_i$ is required to take an integer value of 0 or 1, where $z_i
= 0$ implies $x_i$ should be rounded down and $z_i = 1$ implies that
$x_i$ should be rounded up.

TopDown options still to be selected
------------------------------------

There are 7 key choices in implementing TopDown, that balance accuracy
and privacy. We list them here, and state how they were set in the
2018 end-to-end test when run on the 1940s Census data:

1. Overall privacy. A range of $\epsilon$ values, with $\{0.25, 0.50,
   0.75, 1.0, 2.0, 4.0, 8.0\}$ used in the E2E test run on the 1940
   Census Data.

2. How to split this budget between national, state, county, tract,
   block group, and block. In the test run, $\epsilon$ was split evenly
   between national, state, county, and enumeration district.

3. What DP Queries to include. In the test, two DP Queries were
   included: (i) counts stratified by age-group/race/ethnicity (in
   other words, aggregating over "group quarters" type); and (ii) the
   group-quarters counts, which tally the number of people free-living and
   number in institutional and non-institutional facilities.

4. At each level, how to split level-budget between detailed queries
   and DP queries. The test run used 10% for detailed queries, 22.5%
   for group quarters; and 67.5% for
   age-group-/race-/ethnicity-stratified counts.

5. What invariants to include. The test run held the total count at
   the national and state level invariant.

6. What constraints to include.  The test run constrained the total
   count of people to be greater or equal to total count of occupied
   households at each geographic level.

7. What to publish.  The test run published a synthetic person file
   and synthetic household file for a range of $\epsilon$ values, for 4
   different seeds to the pseudorandom number generator.


Our Evaluation Approach
-----------------------

1. We calculated residuals (DP count minus exact count) and summarized
   their distribution by its median absolute error (MAE) for total
   count (TC) and age/race/ethnicity stratified count (SC) at the
   state, county, and enumeration-district level.  We also summarized
   the size of these counts to understand relative error as well as
   the absolute error introduced by TopDown.

2. We calculated a measure of "empirical privacy loss", inspired by the
   definition of differential privacy.  To measure empirical privacy
   loss, we approximate the probability distribution of the residuals
   $\hat{p}(x)$ using Gaussian kernel density estimation with a
   bandwidth of 0.1, and compare the log-ratio inspired by the
   definition of $\epsilon$-DP algorithms:

   $$\text{EPL}(x) = \log\left(\hat{p}(x) / \hat{p}(x+1)\right).$$

   We hypothesized that the EPL of TopDown will be substantially smaller
   than the theoretical guarantee of $\epsilon$.  However, it is possible
   that it will be _much larger_ than $\epsilon$, due to the
   difficult-to-predict impact of including certain invariants.

3. We searched for bias in the residuals from (1), with our hypothesis
   that the DP counts are positively biased for areas with low
   diversity. For each geographic area, we constructed a "homogeneity
   index" by counting the cells of the detailed query histogram that
   contained a true count of zero, and we examined the bias (mean
   residual) of the corresponding counts from TopDown stratified by
   homogeneity index.

We also compared the median absolute error and empirical privacy loss
of TopDown to a simpler, but not-differentially-private approach to
protecting privacy, simple random sampling without replacement for a
range of sized samples.  To do this, we generated samples without
replacement of the 1940 Census Data for a range of sizes, and applied
the same calculations from (1) and (2) to this alternatively perturbed
data.



Results
=======

Error and Privacy of TopDown
----------------------------

We found error in total count (TC) varied as a function of total
privacy loss budget. Running TopDown with $\epsilon = 0.25$ produced
median absolute error in TC of 56 at the
enumeration district level and 81 at the county
level; $\epsilon = 1.0$ produced median absolute error in TC of
15 at the enumeration district level and
24 at the county level; and $\epsilon = 4.0$ produced
median absolute error in TC of 4 at the
enumeration district level and 7 at the county level
(Full table in Supplementary Appendix 1).  At the state level, there
was TC error of $0.0$, as expected from the state TC invariant.  The
median TC was 865 for enumeration districts,
18679 for counties, and 1903133 for
states.

Error in stratified count (SC) varied similarly; When $\epsilon =
0.25$, the median absolute error in SC at the enumeration district
level was 17 people, at the county level was
16 people, and at the state level was
18 people; for $\epsilon = 1.0$, the median absolute
error in SC at the enumeration district level was
6 people, at the county level was
6 people, and at the state level was
7 people; and for $\epsilon = 4.00$, the median
absolute error in SC at the enumeration district level was
2 people, at the county level was
2 people, and at the state level was
2 people. The median SC was
88 for enumeration districts,
47 for counties, and 229 for
states.  (Figure 1)

We found that the empirical privacy loss was often substantially
smaller than the privacy loss budget.
For $\epsilon = 0.25$, the empirical privacy loss for TC
at the enumeration district level was 0.024
and at the county level was 0.031
(at the state level empirical privacy loss is undefined, since the invariant makes all residuals zero);
for $\epsilon = 1.0$, the empirical privacy loss for TC
at the enumeration district level was 0.085
and at the county level was 0.081; and
for $\epsilon = 4.0$, the empirical privacy loss for TC
at the enumeration district level was 0.304
and at the county level was 0.275.

This relationship between privacy loss budget and empirical privacy
loss was similar for stratified counts (SC) at the enumeration
district and county level, but for privacy loss budgets of 1.0 and less, the empirical privacy
at the enumeration district level was loss for SC was not as responsive to $\epsilon$.
For $\epsilon = 0.25$, the empirical privacy loss for SC
at the enumeration district level was 0.288,
at the county level was 0.129, and
at the state level was 0.067;
for $\epsilon = 1.0$, the empirical privacy loss for SC
at the enumeration district level was 0.488,
at the county level was 0.166, and
at the state level was 0.141; and
for $\epsilon = 4.0$, the empirical privacy loss for SC
at the enumeration district level was 0.450,
at the county level was 0.460, and
at the state level was 0.531.

![](fig_1_hist_epl.png "Figure 1 Error Histogram and Empirical Privacy Loss Function")

*Figure 1*: Panel (a) shows the distribution of residuals (DP - Exact) for
stratified counts at the enumeration district level, stratified by
age, race, and ethnicity; and panel (b) shows the empirical privacy
loss, $EPL(x) = \log\left(p(x) / p(x+1)\right),$
where $p(x)$ is the probability density corresponding to the
histogram in (a), after smoothing with a Gaussian kernel of bandwidth
$0.1$.


Comparison with Error and Privacy of Simple Random Sampling
-----------------------------------------------------------

We found that the MAE and EPL of Simple Random Sampling varied with larger sample size in a manner analogous to the total privacy budget in TopDown, for $\epsilon \geq 1$.  For a 5% sample of the 1940 Census data, we found 
median absolute error in TC of 74 at the enumeration district level,
 388 at the county level, and
3883 at the state level;
a 50% sample produced
median absolute error in TC of 17 at the enumeration district level,
 90 at the county level, and
932 at the state level;
and a 95% sample produced
median absolute error in TC of 4 at the enumeration district level,
 20 at the county level, and
130 at the state level;

Error in stratified county varied similarly; for a 5% sample, we found
median absolute error in SC of 18 at the enumeration district level,
 19 at the county level, and
41 at the state level;
a 50% sample produced
median absolute error in TC of 4 at the enumeration district level,
 5 at the county level, and
9 at the state level.

We found empirical privacy loss increased as sample size increased.
For a 5% sample,
at the enumeration district level, we found
EPL of 0.020 for TC and 0.098 for SC,
and at the county level, we found
0.035 for TC and 0.034 for SC;
a 50% sample produced
EPL of 0.079 for TC and 0.318 for SC
at the enumeration district level,
and 
0.082 for TC and 0.150 for SC
at the county level;
and a 95% sample produced
EPL of 0.314 for TC and 1.333 for SC
at the enumeration district level,
and 
0.429 for TC and 0.612 for SC
at the county level.
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
statistics produce different comparisons).

Bias in the noise introduced by TopDown
---------------------------------------

The bias introduced by TopDown varied with diversity index, as
hypothesized.
Enumeration districts with homogeneity index 0 (0 empty strata) had TC
systematically lower than ground truth, while enumeration
districts with 22 empty strata had TC systematically higher.
The size of this bias decreased as a function of $\epsilon$.  Homogeneity index 0
had bias of -52.6 people for $\epsilon = 0.25$,
-18.9 people for $\epsilon = 1.0$,
and -6.6 people for $\epsilon = 4.0$;
while homogeneity index 22
had bias of 8.7 people for $\epsilon = 0.25$,
3.6 people for $\epsilon = 1.0$,
and 1.5 people for $\epsilon = 4.0$.

Counties displayed the same general pattern, but there are fewer
counties and they typically have less empty strata, so it was not as
pronounced.
The size of this bias again decreased as a function of $\epsilon$.
homogeneity index 0
had bias of -103.7 people for $\epsilon = 0.25$,
-33.9 people for $\epsilon = 1.0$,
and -10.4 people for $\epsilon = 4.0$;
while homogeneity index 22
had bias of 23.4 people for $\epsilon = 0.25$,
14.5 people for $\epsilon = 1.0$,
and 6.0 people for $\epsilon = 4.0$.
(Figure 3)

![](fig_3_homogeneity_bias.png "Figure 3 Homogeneity Bias")

*Figure 3*: The homogeneity index is associated with the residual
 (difference between the count estimated by TopDown and the true
 count).  This plot shows the association for enumeration districts,
 and a similar relationship holds at the county level.  As $\epsilon$
 increases, the scale of the bias decreases; this plot shows $\epsilon
 = 1.0$.




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
local government demographers, and this work may help to understand how
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

Conclusion
==========

DP in census, what will it be?  Opportunity to have something that balances privacy and accuracy, but this opportunity is not without risks.





*Acknowledgements*: Thanks to Neil Marquez for suggesting comparing TopDown to simple random sampling.


References
==========


