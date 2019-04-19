---
title: boost
---

## Model Averaging: from CT to Boosting

In generally, Boosting > Random Forest > Bagging > Single Tree

### Classification Trees

![image-20190419114603181](Untitled/image-20190419114603181.png)

The decision boundaries are along the axes.

### Bagging

Suppose $C(S, x)$ is a classifier for dataset $S$ and input point $x$.

To bag $C$, draw bootstrap samples $S_1, S_2, ..., S_B$ from $S$ with size $N$

$C_{\text{bag}}(x)=\text{Majority Vote}(C(S_i, x), i \in [1, B])$

### Random Forest

refine bagging

At each tree split ,randomly sample $m$ features and only consider these samples. Typically $m=\sqrt p$ or $m=\log p$, where $p$ is the total number of features.

RF tries to improve bagging by de-corelating the trees.s

### Boosting

Average many trees, but each grown from reweighed samples.
$$
C(x)=\text{sign}\sum_{n}\alpha_nC_n(x)
$$

## Additive Model

