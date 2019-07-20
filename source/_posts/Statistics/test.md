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

Then we have the expeccted numbers $m_i=np_i$

As $n\to \infty$, the following quantity follows  $\chi^2$ distribution with $k-1$ freedom:
$$
X^2=\sum_{i=1}^{k}\frac{(x_i-m_i)^2}{m_i}
$$
The CDF of $\chi^2$ distribution is as follows:

![{\displaystyle {\frac {1}{\Gamma (k/2)}}\;\gamma \left({\frac {k}{2}},\,{\frac {x}{2}}\right)\;}](https://wikimedia.org/api/rest_v1/media/math/render/svg/11559ab9fa699c0a8af78095bad79c249480a4ec)

![CDF curve](https://upload.wikimedia.org/wikipedia/commons/0/01/Chi-square_cdf.svg)

The following table gives the $p$-values matching to $\chi^2$ for the first 10 degress of freedom.

| Degrees of freedom (df) | *χ*2 value |      |      |      |      |       |       |       |       |       |       |
| ----------------------- | ---------- | ---- | ---- | ---- | ---- | ----- | ----- | ----- | ----- | ----- | ----- |
| 1                       | 0.004      | 0.02 | 0.06 | 0.15 | 0.46 | 1.07  | 1.64  | 2.71  | 3.84  | 6.63  | 10.83 |
| 2                       | 0.10       | 0.21 | 0.45 | 0.71 | 1.39 | 2.41  | 3.22  | 4.61  | 5.99  | 9.21  | 13.82 |
| 3                       | 0.35       | 0.58 | 1.01 | 1.42 | 2.37 | 3.66  | 4.64  | 6.25  | 7.81  | 11.34 | 16.27 |
| 4                       | 0.71       | 1.06 | 1.65 | 2.20 | 3.36 | 4.88  | 5.99  | 7.78  | 9.49  | 13.28 | 18.47 |
| 5                       | 1.14       | 1.61 | 2.34 | 3.00 | 4.35 | 6.06  | 7.29  | 9.24  | 11.07 | 15.09 | 20.52 |
| 6                       | 1.63       | 2.20 | 3.07 | 3.83 | 5.35 | 7.23  | 8.56  | 10.64 | 12.59 | 16.81 | 22.46 |
| 7                       | 2.17       | 2.83 | 3.82 | 4.67 | 6.35 | 8.38  | 9.80  | 12.02 | 14.07 | 18.48 | 24.32 |
| 8                       | 2.73       | 3.49 | 4.59 | 5.53 | 7.34 | 9.52  | 11.03 | 13.36 | 15.51 | 20.09 | 26.12 |
| 9                       | 3.32       | 4.17 | 5.38 | 6.39 | 8.34 | 10.66 | 12.24 | 14.68 | 16.92 | 21.67 | 27.88 |
| 10                      | 3.94       | 4.87 | 6.18 | 7.27 | 9.34 | 11.78 | 13.44 | 15.99 | 18.31 | 23.21 | 29.59 |
| P value (Probability)   | 0.95       | 0.90 | 0.80 | 0.70 | 0.50 | 0.30  | 0.20  | 0.10  | 0.05  | 0.01  | 0.001 |