---
title: Statistical Test
categories: [statistics]
---

[TOC]

## Two-Sample Kolmogorov–Smirnov Test

Two-sample Kolmogorov–Smirnov (KS) test may be used to test whether two underlying one-dimentional probability distributions differ.

In this case, the KS statistic is 
$$
D_{m,n}=\sup{x} |F_{1,n}(x)-F_{2,m}|,
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


In general, 
$$
c(\alpha)=\sqrt{-\frac{1}{2}\alpha}
$$


