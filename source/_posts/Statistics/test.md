---
title: Statistical Test
categories:
  - Statistics
---

[TOC]

## Two-Sample Kolmogorov–Smirnov Test

Two-sample Kolmogorov–Smirnov (KS) test may be used to test whether two underlying one-dimentional probability distributions differ.

In this case, the KS statistic is 
$$
D_{m,n}=\sup{x} |F_{1,n}(x)-F_{2,m}(x)|,
$$
where $F_{1,n}$ and $F_{2,m}$ are the empirical distribution functions of the first and second sample respectively, and $n$ and $m$ are the size of them.

Empirical distribution function is defined as follows:
$$
F_{n}(x)=\frac{1}{n}\sum_{i=1}^{n}I_{(-\infty, x]}(X_i)
$$
Null hypothesis is a statement of 'no effect' or 'no difference'.

For large samples, the null hypothesis is rejected at level $\alpha$ if 
$$
D_{n,m}>c(\alpha)\sqrt{\frac{n+m}{nm}}
$$

| $\alpha$    | 0.10  | 0.05  | 0.025 | 0.01  | 0.005 | 0.001 |
| ----------- | ----- | ----- | ----- | ----- | ----- | ----- |
| $c(\alpha)$ | 1.073 | 1.224 | 1.358 | 1.517 | 1.628 | 1.858 |

In general, 
$$
c(\alpha)=\sqrt{-\frac{1}{2}\alpha}
$$

## T-Test

## Chi-Squared Test

Suppose $n$ observations are classified into $k$ mutually exclusive classes with respectiive observed numbers $x_i$, and a null hypothesis gives the probablity $p_i$ the an observation falls into the $i$-th class.