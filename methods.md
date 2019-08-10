Methods
=======

_Differential privacy definition and history._  A randomized algorithm for
analyzing a database is _differentially private_ if withholding or changing one
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
people stratified by census block, age, sex, race, and ethnicity,
differential privacy is often implemented by adding noise to the
counts.  It follows logically from the definition that achieving
$\epsilon$-differential privacy in this manner requires adding noise
with variance of at least that of a symmetric geometric distribution
with parameter $\epsilon$. [Additional details here? in Appendix?]

The new disclosure avoidance system for the 2020 US Census is designed
to be differentially private and to mantain the accuracy of census
counts. To complicate things beyond the typical challenge faced in
differentially private algorithm design, there are certain counts in
the census that will be published exactly as enumerated, without any
variance from adding noise.  These _invariants_ have not been selected
for the 2020 decennial census yet, but in the E2E test, the total
count for each state and the number of households in each enumeration
district where invariants.  There are also inequalities that will be
enforced, such as requiring the total count of people in an
enumeration district to be greater or equal to the number of occupied
households in that district.

_TopDown algorithm goal and high-level description._ At a high level,
the census approach to this challenge repeats two steps for multiple
levels of a geographic hierarchy (from the top down, hence the name
`TopDown`). The first step adds randomness to the data counts in a way
that satisfies $\epsilon$-differential privacy. This produces a set of
counts, $N$. The noisy counts in $N$ might have negative counts and
violate the invariants and inequalities.  The second step finds the
argument that minimizes a quadratic objective function, subject to
constraints from a system of linear equations and inequalities that
represent the invariants, inequalities, consistency with the DP counts
from one level higher, and non-negativity. The values that optimize
this constrained optimization are as close to the noisy data as
possible while also satisfying the public properties and requiring
that all counts are positive integers and other internal consistency
constraints. The final output of the TopDown algorithm is a synthetic
data set $S$ that has data counts matching the values that minimize
the constrained optimization.  This satisfies $\epsilon$-differential
privacy and the invariants and inequalities and affords detailed
control of how the privacy budget is spent between and within levels
of the hierarchy.

The census data has six different geographic levels: national, state,
county, census tracts, block groups, and blocks. The census's
differentially private algorithm uses a top-down approach to create
the synthetic data; steps one and two are performed six times in order
from the coarsest to the finest level. Each level is assigned a
privacy budget $\epsilon_i$ and the entire algorithm will satisfy
$\epsilon$-differential privacy where $\epsilon=\sum_{i=1}^6
\epsilon_i.$

At a specific geographic level (say census tracts) the true data has
the form of a histogram; a set of boxes each labeled with a geographic
unit (e.g. census tract one), a race combination (e.g. Black), one sex
(e.g. Female), and one age (e.g. 46). Although the 2020 census will
include more variables, the 1940 data run with E2E test code only
included race (6 mutually exclusive categories), ethnicity
(non-Hispanic and Hispanic), and age group (under-18 and 18-plus).
The number in the box, which we call a histogram count, is the number
of people in the geographic unit with the features of the label
(e.g. the number of 18-plus-year-old non-Hispanic White women in
enumeration district 107). Step one adds geometrically distributed
random noise to numbers in each box according to the privacy budget at
the level $\epsilon_i.$ This noisy data is unsatisfactory because the
noisy counts (i) are sometimes negative, (ii) do not satisfy the
public properties, and (iii) are inconsistent with the synthetic data
produced at the coarser level (e.g. the sum of the noisy counts in all
the boxes corresponding to a census tracts within Cook county may not
equal the number of people in Cook county reported in the synthetic
data produced in the previous step.) Step two solves an
optimization problem which adjusts the counts in boxes so that they
are positive, satisfy the invariants and inequalities, are consistent with the
synthetic data produced at the coarser level, and are as close as
possible to the noisy counts (and are integers).

### Step One: Adding random noise.

The E2E DAS added random
noise in a flexible way that allowed the user to choose what
statistics are the most important to keep accurate. The noise was
added to the histogram counts for the level and also to a preselected
set of aggregate statistics.
Aggregate statistics are sets of histogram count sums specified by
some characteristics. For example, the ``ethnicity-sex" aggregate
statistic contains set of four counts: Hispanic men, Hispanic women,
non-Hispanic men, and non-Hispanic women. The census bureau plans to
include each value that will appear in a tabular summary in the set of
aggregate statistics. [Which DPQueries were used in E2E?]

The epsilon budget of the level governs how much total random noise to
add. A further parameterization of the epsilon budget dictates how the
noise will be allocated between the histogram counts and each type of
aggregate statistic. We write $\epsilon_i = h + s_1 + s_2 + \ldots +
s_k$, where $\epsilon_i$ is the budget for the geographic level, $h$
is the budget for the histogram counts, and $s_1, \dots s_k$ are the
budges for each of the $k$ types of aggregate statistics. Then noise
is added independently to each histogram count and aggregate statistic
as follows:


$$\text{noisy histogram count} = \text{true histogram count} + G(h/2)
$$
$$\text{noisy aggregate stat $j$} = \text{ true aggregate stat $j$} + G(s_j/2)
$$

where $G(z)$ denotes the geometric distribution,

$$\Pr[G(z)=k] = \frac{(1 - \exp(-z))\exp(-z|k|)}{1 + \exp(-z)}.$$

Note the noisy counts and noisy aggregate statistics are unbiased
estimates with variance $(1-\exp(-z))^2/ (2 \exp(-z))$, where $z$ is
the parameter for the geometric noise added. A higher privacy budget
means the noise added is more concentrated around zero, and therefore
the corresponding statistic is more accurate. Therefore, adjusting the
privacy budgets of the various aggregate statistics gives control over
which statistics are the most private/least accurate (low fraction of
the budget) and the most accurate/least private (high fraction of the
budget).

Note that the noise added to each histogram count comes from the same
distribution; the noise does not scale with the magnitude of count,
e.g. adding one hundred people to the count of 18 year-old
non-Hispanic White Men is just as likely as adding one hundred people
to the count of 78 year-old Hispanic Native Men, even though the
population of the latter is smaller. [This example doesn't exist
in the 1940s because we have fewer variables. I am not sure if I
should restrict to their variables for the examples. I think it makes
sense for the examples to be more like the 2020 census.]

### Step Two: Optimization.

In this step, the synthetic data is created from the noisy data by
optimizing a quadratic objective subject to a system of linear
equations and inequalities. The algorithm creates a variable for each
histogram count and each aggregate statistic. It adds equations and inequalities
to encode the requirements that (i) each count and
aggregate statistic is non-negative, (ii) the invariants and inequalities are
satisfied, (iii) the aggregate statistics are the sum of the
corresponding histogram counts, and (iv) the statistics are consistent
with the higher level synthetic data counts (i.e. the total number of men
summed across the counties in a state is equal to the number of men in
the State as reported by synthetic data set constructed in the
previous phase). The optimization step finds a solution that satisfies
these equations and has the property that the value of each variable
is as close as possible to the corresponding noisy histogram count or
noisy aggregate statistic. This is done in a way that favors closeness
for the noisy values constructed by adding noise from a lower variance
geometric distribution. [Integers! How?]

`TopDown` options still to be selected
--------------------------------------

The 7 key policy choices, and how they were set in the 2018 end-to-end
test:

1. Overall privacy 
2. How to split this budget between national, state, county, tract, block group, and block
3. At each level, how to split level-budget detailed  DP 
4. What DP Queries to include
5. What invariants to include
6. What constraints to include
7. What to publish


Our Evaluation Approach
-----------------------

1. Calculate errors and their variance (for total count and
age/race/ethnicity stratified count for state, county, and
enum_district)

2. Calculate "empirical privacy loss" (which we have just invented for
the purposes of this paper; need to describe it here) (for same groupings)

3. Search for bias, with our hypothesis that it appears differentially
with respect to diversity of spatial units.)

We compare the bias, variance, and privacy to a simpler, but
not-differentially-private approach to protecting privacy: simple
random sample of X% total for a range of X.

