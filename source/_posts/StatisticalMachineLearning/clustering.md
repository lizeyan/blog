---
title: Clustering
categories:
  - StatisticalMachineLearning
tags:
  - unsupervised
---

## Clustering

cluster means group objects into classes of similar objects

-   Minimize inter-class similarity
-   Maximize intra-class similarity

### Metric Sapce

What is distance?

1.  $d(x, y) = d(y, x)$
2.  $d(x , y) \ge 0$ and $d(x, y)=0 \Leftrightarrow x = y$
3.  $d(x,y)\le d(x, z) + d(z, y)$

Examples:

-   (distance derived from) $p$-norm 
-   edit distance
-   hamming distance
-   Cosine distance
-   Non-metric distances,  e.g. DTW, perceptual loss

### K-Means

#### Algorithm

1.  Initialize $\mu_1, ..., \mu_K$
2.  Repeat until no change happens
    1.  Expectation: for each $k$, $C_k=\{i\>s.t.\> x_i\text{ is closest to }\mu_k\}$
    2.  Maximization: for each $k$, update $\mu_k=\frac{1}{|C_k|}\sum_{i\in C_k}x_i$

#### Optimization problem

$$
J=\sum_{i=1}^{N}\sum_{k=1}^{K}r_{nk}||x_n-\mu_k||^2 \\
s.t. \>\> \sum_{k=1}^{K}r_{nk}=1, r_{nk}\in\{0, 1\}\\
\mu_k=\frac{\sum_ix_i1_{r_{nk}=1}}{\sum_i1_{r_{nk}=1}}
$$

In each expection step, we keep $\mu_k$ fixed and optimize $J$ with respect to $r_{nk}$

It has closed form solution:	