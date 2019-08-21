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


