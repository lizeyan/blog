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

当系统发生异常时，组件之间的invariant link常常会发生变化。消失的invariant link就被称为broken link。

通过检测哪些组件导致了broken link可以引导运维人员找到故障的根因。

## MRF Model

### Algorithm

MRF（Markov random field）模型可以用来建模invariant network和borken network[^icdm2014]。

MRF包含若干个变量，每个变量有隐状态和显状态，隐状态之间有互相的连接。

每个包含至少一条broken link的节点是MRF中的一个变量，broken link是变量之间的连接。其observed state是我们对每个节点的根因程度的直接观察。具体的定义可以为
$$
RB_{v_i}=\frac{number\>of\>borken\>links\>of\>v_i}{number\>of\>all\>links\>of\>v_i}\\
RUB_{v_i}=1-\frac{number\>of\>broken\>links\>related\>to\>BINN}{number\>of\>all\>links\>related\>to\>BINN}
$$
BINN指的是节点的通过broken link连接起来的邻居

RB被用来作为隐状态的初始值，RUB作为显状态[^icdm2014]。

node compatibility function定义为
$$
\Phi(\lambda, \omega)=\begin{cases}\omega & \lambda=abnormal\\1-\omega & \lambda =normal\end{cases}
$$
每个节点是根因的belief，$b(\lambda)$为：
$$
b_i(\lambda)=k\Phi(\lambda, \omega_i)\prod_{j\in N(i)}m_{ji}(\lambda)
$$
$m_{ji}(\lambda)$表示邻居$j$认为$i$处于状态$\lambda$的belief
$$
m_{ij}(\lambda)=\sum_{\lambda'}\Phi(\lambda,\omega_i)\Psi(\lambda,\lambda')\prod_{n\in N(i)/j}m_{ni}(\lambda')
$$
其中$\Psi(\lambda,\lambda')$表示edge compatibility function。

|          | normal                 | abnormal       |
| -------- | ---------------------- | -------------- |
| normal   | $\epsilon_0$ (很小)    | $1-\epsilon_0$ |
| abnormal | $\epsilon$ （小于0.5） | $1-\epsilon$   |

这样的message passing的方法被称为loopy BP[^icdm2014]。

### Evaluation

~[^icdm2014]中只把MRF model和直接用RB给节点排序的方法进行了对比。评价指标是top-k precision，top-k recall，和nDCG。

- Top-k precision and recall. k一般选择ground truth set大小的两倍 [^dcg]。
- nDCG （cumulated gain vector with discount, [^dcg]）：表征top-p的排序结果。p一半比ground truth set略小。
$$
nDCG=\frac{DCG}{IDDCG}
$$
$$
DCG_p=\sum_{i=1}^{p}\frac{2^{rel_i-1}}{\log_2{1+i}}
$$
​	$rel_i$是第i名在ground truth中的名次。IDCG是ground truth的DCG

但是从结果看来，LBP比直接用RB并不好太多。

![image-20190625151638557](network_diffusion/image-20190625151638557.png)

![image-20190625151846712](network_diffusion/image-20190625151846712.png)

![image-20190625151900114](network_diffusion/image-20190625151900114.png)

## Label Propagation and Network Diffusion[^kdd2016]





[^tkde2007]: Guofei Jiang, Haifeng Chen, K. Yoshihira. Efficient and Scalable Algorithms for Inferring Likely Invariants in Distributed Systems
[^icdm2014]: Changxia Tao, Yang Ge, Qinbao Song, Yuan Ge, Olufemi A. Omitaomu. Metric Ranking of Invariant Networks with Belief Propagation.
[^kdd2016]: Wei Cheng, Kai Zhang, Haifeng Chen, Guofei Jiang, Zhengzhang Chen, Wei Wang. Ranking Causal Anomalies via Temporal and Dynamical Analysis on Vanishing Correlations