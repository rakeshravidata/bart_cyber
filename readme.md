## Applications of Bayesian Additive Regression Trees in Cybersecurity

With the rise of internet usage, the advent of internet of things and the amount of data being transferred on a
daily basis, our lives are becoming increasingly digitized. Most of our personal data is held inside digital devices and
their connection to the internet makes them vulnerable to malicious attacks. As a result, Cybersecurity is one of
the prime focus areas from a security standpoint for all developed and developing nations in the world. It is
estimated that over $6 Billion Dollars will be spent on arming the United States with cybersecurity ammunition to
counter malicious actors by 2021 [1]. Machine learning is being applied in cybersecurity to build robust systems in
order to prevent hackers from attacking institutions and organizations. Several government institutions and
research institutions are releasing data on malicious attacks that machine learning practitioners can use to build
novel intrusion detection systems. Tree ensembles like gradient boosting and random forest have been used with a
lot of success due to the ability of tree ensembles to handle high cardinality categorical variables efficiently. The
only drawback of using such models is that the final prediction is a point estimate which prevents the practitioner
from fully understanding the response variable. Bayesian additive regression trees (BART) has emerged as an
alternative to gradient boosting and in many cases, delivers much better performs while providing distribution of
probabilities instead of point estimates [2]. In this paper, I have implemented BART and compared its performance
on the CTU-13 Stratosphere Project data set with other classification models.
