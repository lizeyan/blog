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
模型定义为$\hat{y}(t)=\phi(t)^\top\theta$

[^tkde2007]: Guofei Jiang, Haifeng Chen, K. Yoshihira. Efficient and Scalable Algorithms for Inferring Likely Invariants in Distributed Systems
[^icdm2014]: Changxia Tao, Yang Ge, Qinbao Song, Yuan Ge, Olufemi A. Omitaomu. Metric Ranking of Invariant Networks with Belief Propagation.