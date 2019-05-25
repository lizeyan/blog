---
title: Locality Sensitive Hashing
categories:
- Algorithm
---

## Definition and Instances

LSH is a randomized hasing framework for efficient approximate neasrest negibot search in high dimensional space.

It is based on the definition of LSH family $\mathcal{H}$, a family of hash functions mapping similar input items into the same hash code with higher probability than dissimilar items.

LSH aims to maximize the probability of collision of similar items, while tradition hash always avoid collisions.

### The Family

A family $\mathcal{H}$ is $(R, cR, P_1, P_2)$-sensitive if for any two items $p$ and $q$

If $d(p, q)\le R$, then $P(h(p)=h(q))\ge P_1​$

If $d(p, q)\ge cR$, then $P(h(p)=h(q))\le P_2$

Here $c>1$, $P_1>P_2$, $h\in\mathcal{H}$

Define $\rho=\frac{\log P_1}{\log P_2}$, then there exists an algorithm for (R, C)-near neighbor problem which uses $O(dn+n^{1+\rho})$ space, with query time dominated by $O(n^{\rho})$ distance computations and $O(n^{\rho}\log_{1/P_2}n)$ evaluations of hash functions. [^fn1]

[^fn1]: Localitysensitive hashing scheme based on p-stable distributions.

Define $g(x)=(h_1(x), ...., h_K(x))$, the output of $g$ identifies a hash bucket id.

However, the compound hash function also reduce the probability of collsion of smiliar items.

To improve the recall, $L$ such compund hash function are sampled independently, each of which corresponds to a hash table.



To improve precision, K should be large.

To improve recall, L should be large.

The items lying in the L hash buckets are retrieved as near item candidates.

### $l_p$ Distance

### Angle-Based Distance

### Hamming Distance

### Jaccard Coefficient

### $\mathcal{X}^2$ Distance

### Rank Similarity

### Shift Invariant Kernels

### Non-Metric Distance

### Arbitrary Distance Measures

## Search, Modeling and Analyzing

### Search

#### Entropy-based search

#### LSH forest

#### Adaptative LSH

#### Multi-Probe LSH [^multi-probe-lsh]

Given a query $q$, the basic LSH query $g(q)=(h_1(q), ..., h_M(q))$, while multi-probe LSH probes $g(q)+\Delta$. $\Delta=(\delta_1, ..., \delta_M), \delta_i\in\{-1, 0, 1\}$, since similar objects should hash to the same or adjacent buckets with high probability. A approriate pertubation sequence will make multi-probe LSH achieves similar recall with less hash tables and similar time complexity.

##### Step-Wise Probing

Firstly probe the 1-step buckets, then all the 2-step buckets, and so on.

The total number of all $n$-step buckets is $L\times {M\choose n}\times2^n$.

![image-20190525212643536](locality_sensitive_hash/image-20190525212643536.png)

Using the step-wise probing method, all coordinates in the hash values are treated indentically.







[^multi-probe-lsh]: Q. Lv, W. Josephson, Z. Wang, M. Charikar, and K. Li. Multiprobe lsh: Efﬁcient indexing for high-dimensional similarity search. In VLDB, pages 950–961, 2007. 3, 8

#### Dynamic Collision Counting for Search

#### Bayesian LSH

#### Fast LSH

#### Bi-Level LSH

### SortingKeys-LSH

### Analysis and Modeling

