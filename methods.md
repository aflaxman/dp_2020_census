Methods
=======

_Differential privacy definition and history._ A randomized algorithm
for analyzing a database is _differentially private_ (DP) if
withholding or changing one person's data does not substantially
change the algorithm's output. If the results of the computation are
roughly the same whether or not my data are included in the database,
then the computation must be protecting my privacy. DP algorithms come
with a parameter $\epsilon$, which quantifies how much privacy loss is
allowed, meaning how much can one person's data to affect the
analysis.

To be precise, a randomized algorithm $\mathcal{A}$ is $\epsilon$-DP if,
for each possible output $\mathcal{P}$, for any pair of datasets $D$
and $D'$ that are the same everywhere except for on one person's data,
$$
\Pr\left[\mathcal{A}(D) = \mathcal{P}\right]
\leq \exp\left(\epsilon\right)
\Pr\left[\mathcal{A}(D') = \mathcal{P}\right].
$$

Differential privacy is a characteristic of an algorithm; it is not a
specific algorithm. Algorithms often achieve differential privacy by
adding random variation.[@dwork2014algorithmic]

The new disclosure avoidance system for the 2020 US Census is designed
to be DP and to maintain the accuracy of census counts. To complicate
things beyond the typical challenge faced in DP algorithm design,
there are certain counts in the census that will be published precisely
as enumerated, without any variation added.  These
_invariants_ have not been selected for the 2020 decennial census yet,
but in the 2018 end-to-end (E2E) test, the total count for each state
and the number of households in each enumeration district were
invariants.  There are also inequalities that will be enforced. The E2E test 
required the total count of people in an enumeration district to
be greater or equal to the number of occupied households in that
district.[@garfinkel2019end]

_TopDown algorithm._ At a high level, the census approach to this
challenge repeats two steps for multiple levels of a geographic
hierarchy (from the top down, hence their name "TopDown"). The first
step (Imprecise Histogram) adds variation from a carefully chosen
distribution to the stratified counts of individuals.  This produces a
set of counts with illogical inconsistencies. For example, the
imprecise histogram counts might be negative, violate
invariants or other inequalities, or be inconsistent with the counts
one level up in the geographic hierarchy.  The second step (Optimize)
adjusts the histogram to be close as possible to the imprecise counts,
subject to the constraints that all counts be non-negative,
consistent with each other and the higher levels of the hierarchy, and
satisfy the invariants and inequalities.  These two steps are
performed for each geographic level, from the coarsest to the finest.
Each level is assigned a privacy budget $\epsilon_i$ (which governs
how much variation to add in the Imprecise Histogram step), and the entire
algorithm achieves $\epsilon$-DP for $\epsilon=\sum_{i=1}^6
\epsilon_i$.  The 2020 US Census data will have six geographic levels,
nested hierarchically: national, state, county, census tracts, block
groups, and blocks; but in the 1940 E2E test, only national, state,
county, and district levels were included.

### Step One: Imprecise Histogram

In the E2E algorithm applied to the 1940s microdata, TopDown added
random variation in a flexible way that allowed the user to choose
what statistics are the most important to keep accurate. The variation
was added to the detailed histogram counts for the level and also to a
preselected set of aggregate statistics. The detailed histogram counts
stratified the population of each geographic by age (two values:
under-18-year-olds and 18-plus), race (six values), ethnicity (two
values: hispanic and non-hispanic), and household/group-quarters type
(6 values).  The aggregate statistics are sets of histogram count sums
specified by some characteristics. For example, the "ethnicity-age"
aggregate statistic contains set of four counts: people of Hispanic
ethnicity under age 18, of Hispanic ethnicity age 18 and over, of
non-Hispanic ethnicity under age 18, and of non-Hispanic ethnicity age
18 and over.

The aggregate statistics (internally called "DP queries") afford a way
to choose specific statistics that are more important to keep
accurate, and the E2E test included two such aggregates: a
household/group-quarters query, which increases the accuracy of the count of
each household type at each level of the hierarchy, and a
race/ethnicity/age query, which increases the accuracy of the
stratified counts of people by race, ethnicity, and voting age across
all household/group quarters types (again for each level of the
spatial hierarchy). It also included "detailed queries" corresponding
to boxes in the histogram.  The detailed queries were afforded 10% of
the privacy budget at each level, while the DP queries split the
remaining 90% of the privacy budget, with 22.5% spent on the
group-quarters queries and 67.5% spend on the race/ethnicity/age
queries.

The epsilon budget of the level governed how much total random variation
to add. A further parameterization of the epsilon budget determined
how the variance was allocated between the histogram counts and each type
of aggregate statistic. We write $\epsilon_i = h + s_1 + s_2 + \ldots
+ s_k$, where $\epsilon_i$ was the budget for the geographic level,
$h$ was the budget for the detailed queries, and $s_1, \dots s_k$ were
the budgets for each of the $k$ types of aggregate statistics. Then
variance was added independently to each count according to the follow
distribution:
$$
\text{imprecise detailed histogram count}
 = \text{precise detailed histogram count} + G(h/2)
$$
$$\text{imprecise aggregate stat $j$}
 = \text{ precise aggregate stat $j$} + G(s_j/2)
$$
where $G(z)$ denotes the two-tailed geometric distribution,
$$
\Pr[G(z)=k] = \frac{(1 - \exp(-z))\exp(-z|k|)}{1 + \exp(-z)}.
$$

The imprecise counts and imprecise aggregate statistics are unbiased estimates
with variance $(1-\exp(-z))^2/ (2 \exp(-z))$, where $z$ is the
parameter for the geometric random variable added. A higher privacy budget means
the variance added is more concentrated around zero, and therefore the
corresponding statistic is more accurate. Therefore, adjusting the
privacy budgets of the various aggregate statistics gives control over
which statistics are the most private/least accurate (low fraction of
the budget) and the most accurate/least private (high fraction of the
budget).

The variation added to each histogram count comes from the same
distribution, and is independent of all other added variation; the variance
does not scale with the magnitude of count, e.g. adding 23 people to
the count of age 18 and older non-Hispanic Whites is just as likely as
adding 23 people to the count of age under 18 Hispanic Native
Americans, even though the population of the latter is smaller.

### Step Two: Optimize

In this step, the synthetic data is created from the imprecise
detailed histogram counts and aggregate statistics by optimizing a
quadratic objective function subject to a system of linear equations
and inequalities. The algorithm creates a variable for each detailed
histogram count and each aggregate statistic. It adds equations and
inequalities to encode the requirements that (i) each count and
aggregate statistic is non-negative, (ii) the invariants and
inequalities are satisfied, (iii) the aggregate statistics are the sum
of the corresponding detailed histogram counts, and (iv) the
statistics are consistent with the higher level synthetic data counts
(i.e. the total number of people aged 18 and over summed across the
counties in a state is equal to the number of people aged 18 and over
in that state as reported by synthetic data set constructed in the
previous phase). The optimization step finds a solution that satisfies
these equations and has the property that the value of each variable
is as close as possible to the corresponding imprecise detailed
histogram count or imprecise aggregate statistic. The solution
minimizes a weighted sum of the squared differences between each precise
and imprecise count, where each weight is proportional to the
magnitude of the variation added in step one to create the imprecise
count. The solution to this optimization is not necessarily integral,
however, and TopDown uses a second optimization step to round
fractional counts to integers.


Empirical Privacy Loss for quantifying impact of optimize steps
---------------------------------------------------------------

As described above, the privacy loss of a DP algorithm is quantified
by a unitless number, $\epsilon$, that bounds the maximum log of the
relative change in the probability of an output when one person's data is
changed.  This bound is typically proven by logical deduction , and
for complex DP algorithms, the proof often relies on the Sequential
Composition Theorem,[@dwork2014algorithmic] which states that
information derived by combining the output of an $\epsilon_1$-DP
algorithm and an $\epsilon_2$-DP algorithm is at most
$(\epsilon_1+\epsilon_2)$-DP. This theorem is an inequality however, and
the inequality might have room for improvement.

It is possible to empirically quantify privacy loss, which has the
potential to show that the inequality of the sequential composition
theorem is not tight. The brute force approach quantify privacy loss
empirically is to search over databases $D$ and $D'$ that differ on one row
to find the event $E$ with the largest ratio of probabilities; this too
computationally intensive to be feasible for all but the simplest DP
algorithms.

For algorithms that produce DP counts of multiple
subpopulations, such as TopDown, it is possible to use the
distribution of the residual difference between the precise count
and the DP count to derive a proxy of the distribution produced by the
brute force approach.[@flaxman2019empirical]
The special structure of count queries affords a way to
avoid re-running the algorithm repeatedly, which is
essential for TopDown, since it takes several hours to complete a
single run of the algorithm.  Assuming that the residual difference of
the DP count minus the precise count is identically distributed for
queries across similar areas (such as voting-age population across all
enumeration districts), and then instead of focusing on only the histogram
counts containing the individual who has changed, we used the
residuals for all areal units to estimate the probability of the event
we are after:
$$
\Pr\left[\mathrm{error}_{j_1, j_2, \ldots, j_{J}}^D =k\right]
 \approx \bigg(\sum_{j_1'=1}^C\sum_{j_2'=1}^C\cdots\sum_{j_J'= 1}^C
   \mathbf{1}\left[\left\{\mathrm{error}_{j_1', j_2', \ldots, j_{J}'}^D
 = k\right\}\right]\bigg)\bigg/C^J =: \hat{p}_k,
$$
and
$$
\mathrm{error}_{j_1, j_2, \ldots, j_{J}}^D
$$
is the residual difference of DP counts returned by TopDown minus the
exact count for that same quantity in the 1940 census.

We can make this estimate with more precision than the direct
estimate, using substantially less computation.

It is also possible to make an estimate of the probability $D'$ yields
error of $k$ without repeatedly running the DP algorithm.  This relies
on the observation that, for count queries, a change to a single row
of data can change the exact count by at most one for any areal unit.
Therefore
$$
\Pr\left[\mathrm{error}_{j_1, j_2, \ldots, j_{J}}^{D'}
= k\right]
\gtrapprox
\begin{cases}
\Pr\left[\mathrm{error}_{j_1, j_2, \ldots, j_{J}}^{D}
= k+1\right], \qquad \text{ if } k \geq 0;\\[.1in]
\Pr\left[\mathrm{error}_{j_1, j_2, \ldots, j_{J}}^{D}
= k-1\right], \qquad \text{ if } k \leq 0;
\end{cases}
$$
which we can also approximate by examining the residuals for all areal units:
$$
\Pr\left[\mathrm{error}_{j_1, j_2, \ldots, j_{J}}^{D'}
= k\right]
\gtrapprox
\bigg(\sum_{j_1'=1}^C\sum_{j_2'=1}^C\cdots\sum_{j_J' = 1}^C \mathbf{1}\left[\left\{\mathrm{error}_{j_1', j_2', \ldots, j_{J}'}^D
= k\pm 1\right\}\right]\bigg)\bigg/C^J.
$$


TopDown options still to be selected
------------------------------------

There are 7 key choices in implementing TopDown, that balance accuracy
and privacy. We list them here, and state how they were set in the
2018 end-to-end test when run on the 1940s Census data:

1. Overall privacy. A range of $\epsilon$ values, with $\{0.25, 0.50,
   0.75, 1.0, 2.0, 4.0, 8.0\}$ used in the E2E test run on the 1940
   Census Data.

2. How to split this budget between national, state, county, tract,
   block group, and block. In the test run, $\epsilon$ was split
   evenly between national, state, county, and enumeration district.

3. What DP Queries to include. In the test, two DP Queries were
   included: (i) counts stratified by age-group/race/ethnicity (in
   other words, aggregating over "group quarters" type); and (ii) the
   group-quarters counts, which tally the number of people free-living
   as well as in five types of institutional and non-institutional
   facilities.

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
   and synthetic household file for a range of $\epsilon$ values, for
   4 different seeds to the pseudorandom number generator.


Our Evaluation Approach
-----------------------

1. We calculated residuals (DP count minus exact count) and summarized
   their distribution by its median absolute error (MAE) for total
   count (TC) and age/race/ethnicity stratified count (SC) at the
   state, county, and enumeration-district level.  We also summarized
   the size of these counts to understand relative error as well as
   the absolute error introduced by TopDown.

2. We calculated a measure of empirical privacy loss (EPL), inspired
   by the definition of differential privacy.  To measure EPL, we
   approximated the probability distribution of the residuals
   $\hat{p}(x)$ using Gaussian kernel density estimation with a
   bandwidth of 0.1, and compare the log-ratio inspired by the
   definition of $\epsilon$-DP algorithms:

   $$\text{EPL}(x) = \log\left(\hat{p}(x) / \hat{p}(x+1)\right).$$

   We hypothesized that the EPL of TopDown will be substantially
   smaller than the theoretical guarantee of $\epsilon$, which was
   proven using the Sequential Composition Theorem, which provides an
   inequality that is usually _not_ a tight
   bound.[@flaxman2019empirical] However, it is possible that it will
   be _much larger_ than $\epsilon$, due to the difficult-to-predict
   impact of including certain invariants.

3. We searched for bias in the residuals from (1), with our hypothesis
   that the DP counts are positively biased for areas with low
   diversity. We based this hypothesis on the expected impact of the
   non-negativity constraints included in the optimization steps of
   the TopDown algorithm.  For each detailed query with a negative
   value for its noisy count, the optimization step will increase the
   value to make the results logical, and this reduction in variance
   must tradeoff some increase in bias. To quantify the scale of the
   bias introduced by optimization, for each geographic area, we
   constructed a "homogeneity index" by counting the cells of the
   detailed histogram that contained a true count of zero, and we
   examined the bias (mean residual) of the corresponding counts from
   TopDown stratified by homogeneity index.

We also compared the median absolute error and empirical privacy loss
of TopDown to a simpler, but not-differentially-private approach to
protecting privacy, Simple Random Sampling (i.e. sampling without
replacement) for a range of sized samples.  To do this, we generated
samples without replacement of the 1940 Census Data for a range of
sizes, and applied the same calculations from (1) and (2) to this
alternatively perturbed data.


