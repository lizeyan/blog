---
title: NB and LR
---

## NB

settings:
$$
p(y|\pi)=\begin{cases}\pi & y=1 \\ 1-\pi & y=0\end{cases} \\
p(x|y, q)=\begin{cases}q_y & x=1 \\ 1-q_y & x=0\end{cases}
$$
Log likelihood:
$$
\mathcal{L} = \log \prod_{i=1}^{N}p(x_i, y_i)\\
=\sum_{i=1}^{N}\log p(x_i|y_i)+\log p(y_i) \\
=\sum_{i=1}^{N}x_i\log q_{y_i} + (1-x_i)\log (1 - q_{y_i}) + y_i\log \pi_i + (1-y_i)\log (1 - \pi_i)
$$
MLE:
$$
\frac{\partial \mathcal{L}}{\partial \pi}=
$$
