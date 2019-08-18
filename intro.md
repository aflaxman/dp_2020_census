Introduction
============

In the United States, the Decennial Census is an important part of
democratic governance.  Every ten years, the US Census Bureau is
consititutionally required to count the "whole number of persons in
each State", and in 2020 this effort is likely to cost over fifteen
billion dollars.[@garfinkel2019understanding, @gao2018census] The results will be used for apportioning representation
in the US House of Representatives, for dividing federal tax dollars
between states, as well as for a multitude of other governmental
activities at the national, state, and local level.  Data from the
decennial census will also be used extensively by sociologists,
economists, demographers, and other researchers, and it will also
inform strategic decisions in the private and non-profit sectors, and
facilitate the accurate weighting of subsequent population surveys for
the next decade.[@ruggles2019differential]

The confidentiality of information in the decenial census is also
constitutionally mandated, and the 2020 US Census will use a novel
approach to "disclosure avoidance" to protect respondents' data.[@abowd2018disclosure] This
approach builds on Differential Privacy (DP), a mathematical
definition of privacy and privacy loss that has been developed over
the last decade and a half in the theoretical computer science and
cryptography communities.[@dwork2014algorithmic] Although the new approach allows a more
precise accounting of the noise introduced by the process, it also
risks reducing the utility of census data---it may produce counts that
are substantially noisier than the previous discloure avoidance
system, which was based on a technique called swapping, and relied on
the detailed of the swapping procedure being secret.[@mckenna2018disclosure]

To date, there is a lack of empirical examination of DP in census DAS,
but the approach was applied to the 2018 end-to-end test of the
decennial census, and computer code used for this test as well as
accompaning exposition has recently been released publicly by the
Census Bureau.[@abowd2018disclosure, @boyd2019differential]

We used the recently released code, preprints, and data files to
quantify the error introduced by the E2E disclosure avoidance system
when Census Bureau used it to guarantee differential privacy for the
1940 US Census (for which the full data has previously been released)
at a range of privacy loss budgets.  We also developed an empirical
measure of privacy loss and used it to compare the error and privacy
of the DP approach to that of a simple-random-sampling approach to
protecting privacy.


