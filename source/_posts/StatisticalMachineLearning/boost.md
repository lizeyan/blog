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