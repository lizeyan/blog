---
title: Network Diffusion
---

# Network Diffusion

[TOC]

## Invariant Network

假设有N条时间序列，这N条时间序列之间的相关关系称为invariant link。这样的有invariant link的graph就称为invariant network。

具体的做法是用ARX模型[^tkde2007]。给定两个时间序列$x(t), y(t)$。若将$x$作为输入，那么记
$$
\phi(t)=[-y(t-1),...,-y(t-n),x(t-k),...,x(t-k-m)]^\top\\
\theta = [a_1,...,a_n,b_0,...,b_m]^\top
$$
模型定义为$\hat{y}(t)=\phi(t)^\top\theta$。

通过最小化MSE得，$\theta$的解为
$$
\hat{\theta}_N=[\sum_{t=1}^{N}\phi(t)\phi(t)^\top]^{-1}\sum_{t=1}^{N}\phi(t)y(t)
$$
定义fitness score为
$$
F(\theta)=1 - \sqrt{\frac{\sum_{t=1}^{N}|y(t)-\hat{y}(t)|^2}{\sum_{t=1}^{N}|y(t)-\bar{y}|^2}}
$$
如果$F(\theta)$超过一个给定的阈值，那么就认为两个模型之间有相关关系。

但是给定一组$x, y$，我们无法事先确定哪个是输入哪个是输出。[^tkde2007]中的方法是选择$F(\theta)$较高的那一个，但是同时要求两个模型的fitness score都比较高。

## Broken Links

当系统发生异常时，组件之间的invariant link常常会发生变化。









[^tkde2007]: Guofei Jiang, Haifeng Chen, K. Yoshihira. Efficient and Scalable Algorithms for Inferring Likely Invariants in Distributed Systems
[^icdm2014]: Changxia Tao, Yang Ge, Qinbao Song, Yuan Ge, Olufemi A. Omitaomu. Metric Ranking of Invariant Networks with Belief Propagation.