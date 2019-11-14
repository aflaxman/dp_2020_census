Differential privacy in the 2020 US census, what will it do? Quantifying the accuracy/privacy tradeoff
======================================================================================================

Samantha Petti and Abraham D. Flaxman, {formatted_date}


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
each State," and in 2020 this effort is likely to cost over fifteen
billion dollars.[@garfinkel2019understanding][@gao2018census] The
results will be used for apportioning representation in the US House
of Representatives, for dividing federal tax dollars between states,
as well as for a multitude of other governmental activities at the
national, state, and local levels.  Data from the decennial census will
also be used extensively by sociologists, economists, demographers,
and other researchers, and it will also inform strategic decisions in
the private and non-profit sectors, and facilitate the accurate
weighting of subsequent population surveys for the next
decade.[@ruggles2019differential]

The confidentiality of information in the decennial census is also
required by law, and the 2020 US Census will use a novel approach to
"disclosure avoidance" to protect respondents'
data.[@abowd2019disclosure] This approach builds on Differential
Privacy, a mathematical definition of privacy that has been developed
over the last decade and a half in the theoretical computer science
and cryptography communities.[@dwork2014algorithmic] Although the new
approach allows a more precise accounting of the variation introduced
by the process, it also risks reducing the utility of census data---it
may produce counts that are substantially less accurate than the
previous disclosure avoidance system, which was based on redacting the
values of table cells below a certain size (cell suppression) and a
technique called swapping, where pairs of households with similar
structures but different locations had their location information
exchanged in a way that required that the details of the swapping
procedure be kept secret.[@mckenna2018disclosure]

To date, there is a lack of empirical examination of the new
disclosure avoidance system but the approach was applied to the 2018
end-to-end (E2E) test of the decennial census, and computer code used
for this test as well as accompanying exposition has recently been
released publicly by the Census
Bureau.[@abowd2019disclosure][@boyd2019differential]

We used the recently released code, preprints, and data files to
understand and quantify the error introduced by the E2E disclosure
avoidance system when Census Bureau applied it to 1940 census data
(for which the individual-level data has previously been released
[@ruggles2018ipums]) for a range of privacy loss budgets.  We also
developed an empirical measure of privacy loss and used it to compare
the error and privacy of the new approach to that of a
simple-random-sampling approach to protecting privacy.


