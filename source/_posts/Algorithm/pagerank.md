---
title: Page Rank
categories: [algorithm]
---
# PageRank

记故障传播矩阵为$\mathbf{A}^{N\times N}$，每个节点的异常度$\mathbf{u}$作为 personalization vector。
则
$$
\mathbf{\pi}^\top=\mathbf{\pi}^\top(\alpha \mathbf{A}+(1-\alpha)\mathbf{e}\mathbf{u}^\top)
$$
因为$\mathbf{\pi}^\top\mathbf{e}=1$，
所以等价于
$$
\mathbf{\pi}^\top=\alpha\mathbf{\pi}^\top \mathbf{A}+(1-\alpha)\mathbf{u}^\top
$$

记$\mathbf{M}=(\alpha \mathbf{A}+(1-\alpha)\mathbf{e}\mathbf{u}^\top)$
则$\mathbf{\pi}$应为$\mathbf{M}^\top$的特征值为1 的特征向量。
因为$\mathbf{M}\mathbf{e}=\mathbf{e}$，所以$\mathbf{M}$有特征值 1，那么$\mathbf{M}^\top$也有

根据Gershgorin circle theorem，$\mathbf{M}^\top$的最大特征值不超过 1

所以只要找到$\mathbf{M}$最大特征值对应的特征向量即可

---

**Gershgorin circle theorem**
对于矩阵$\mathbf{M}=(m_{ij})$，记$R_i=\sum_{j\neq i}|m_{ij}|$，则$\mathbf{M}$的特征值至少在以下一个圆盘中：$D(m_{ii}, R_i), \forall i$
证明：
记$\lambda$是$\mathbf{M}$的任意一个特征值，$\mathbf{x}$是对应的特征向量，且使得模最大的元素的模正好是 1（这显然总是可以做到的），记为$x_i$。
那么$\sum_jm_{ij}x_j=\lambda x_i$
因为$x_i=1$，所以$\sum_{j\neq i}m_{ij}x_j+m_{ii}=\lambda$
所以
$$
|\lambda-m_{ii}|=|\sum_{j\neq i}m_{ij}x_{ij}|\le \sum_{j\neq i}|m_{ij}||x_j|\le R_i
$$