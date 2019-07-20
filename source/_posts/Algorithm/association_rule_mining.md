---
title: Association Rule Mining
categories: [Algorithm]
---

# Association Rule Mining

Association rule mining can be viewed as a two-step process:

1.  Mining all frequent itemsets.
2.  Generate strong association rules from the frequent itemsets.



A itemset X is closed if there is no proper super-set Y such that Y has the same support count as X.

A itemset X is a closed frequent itemset if X is frequent and closed.

A itemset X is a maximal frequent if X is frequent and there is no proper super-set Y such that Y is frequent.



## Frequent Itemset Mining Methods

### Apriori

Generate candidates and test if they are frequent. 

The key is pruning the search space.

The Apriori property: If a itemset is not frequent, then any superset of it is not frequent.

The procedure of Apriori algorithm:

1.  generate length-k candidates based on length-(k-1) frequent itemsets.
2.  Scan the database once and prune the infrequent length-k candidates.







### Frequent-Pattern Grouwth

