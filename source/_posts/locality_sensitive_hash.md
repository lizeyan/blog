---
title: Locality Sensitive Hashing
---

## Definition and Instances

LSH is a randomized hasing framework for efficient approximate neasrest negibot search in high dimensional space.

It is based on the definition of LSH family $\mathcal{H}$, a family of hash functions mapping similar input items into the same hash code with higher probability than dissimilar items.

### The Family

A family $\mathcal{H}$ is $(R, cR, P_1, P_2)$-sensitive if for any two items $p$ and $q$

If $d(p, q)\le R$, then $P(h(p)=h(q))\ge P_1​$

If $d(p, q)\ge cR$, then $P(h(p)=h(q))\le P_2$

Here $c>1$, $P_1>P_2$, $h\in\mathcal{H}$

Define $\rho=\frac{\log P_1}{\log P_2}$, then there exists an algorithm for (R, C)-near neighbor problem which uses $O(dn+n^{1+\rho})$ space, with query time dominated by $O(n^{\rho})$

