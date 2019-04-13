---
title: Kernel Density Estimation
mathjax: true
categories: []
---

## KDE

Kernel density estimation (KDE) is a non-parametric way to estimate the probability distribution function (PDF) of a random variable.

若 $\{x_n, n=1,2,...n\}$ 为一列$iid$的样本，那么它的KDE是 
$$
\hat f_h(x)=\frac{1}{nh}\sum_{i=1}^{n}K(\frac{x-x_i}{h})
$$
$h$是bandwith，对KDE的结果有很大影响

[KDE示例](https://github.com/lizeyan/lizeyan.github.io/blob/master/jupyter-notebooks/kernel-density-estimation.ipynb)

## Bandwidth的选择

