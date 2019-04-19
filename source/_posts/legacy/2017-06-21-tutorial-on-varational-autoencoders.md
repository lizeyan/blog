---
title: Tutorial on varational autoencoders
date: 2017-06-21 19:16:26
tags: ["machine learning", "neural network", "generative model"]
---

变分自动编码机 variational autoencoders

<!--more-->

## Introduction

生成式模型用来处理数据点$X​$的概率分布$P(X)​$。一个最简单直接的应用就是计算$P(X)​$的值，比如对于图像， 一个生成式模型可以给真实的照片很高的概率，给无意义的图片比较低的概率。

而另一个更重要的应用是根据数据库中已有的数据，从模型生成和已知数据很相近的数据。

### latent variable model

以生成手写数字$[0,9]$的图片为例，我们的模型如果在生成像素之前首先猜测这个数字$z$是多少，那么这个过程逻辑就会更加清晰，更加直接。这个$z$就是latent variable。

我们需要保证对于已知数据中任何一个数据点$X$，都有至少一组latent variable可以使得模型生成$X$,才能说模型已经能够表示已知数据集. 形式化地讲,我们从空间$\mathbb{Z}$根据概率密度函数$P(z)$采样得到$z$,然后有一组确定性(deterministic)的映射$f:\mathbb{Z}\times\Theta\to\mathbb{X}$,也就是说有函数族$f(z,\theta)$,$\theta$是属于空间$\Theta$的参数. 如果$z$是随机变量而$\theta$是固定的,那么$f$就是空间$\mathbb{X}$中的一个随机变量. 我们的目标就是优化$\theta$,使得我们可以根据$P(z)$采样$z$,然后$f$以很大的概率逼近原始数据$X$. 用条件概率$P(X|z,\theta)$代替映射$f$,那么我们的目标就是最大化下面的概率:
$$
P(X)=\int_{\mathbb{Z}}{P(X|z,\theta)P(z)dz}
$$
在VAE中,输出概率分布经常认为是高斯分布,即$P(X|z,\theta)=N(X|f(z, \theta), \sigma^2 I)$.

为了简洁,常常省略$\theta$.我们对$P(X|z)$的唯一要求仅仅是简单的数值运算复杂度以及对$\theta$的连续性.

![figure1](/images/vae/standard.png)

## Variational AutoEncoder

VAE的数学基础和传统的AutoEncoder(比如Denoising AutoEncoder)很不同. .......

为了处理式(1),我们需要处理两个问题:

- 如何确定$z$
- 如何计算$z$的积分

![figure2](/images/vae/output_prob.png)

对于第一个问题,我们知道$z$表示了问题的内在信息.对于手写数字问题,$z$可以包括数字,笔迹的粗细,转弯处的角度等,这样的信息有很多,而且是互相关联的, 因此人工确认一个问题的latent variable是不可行的.在VAE中,我们仅仅是简单地假设$Z$服从简单的分布比如$N(0, I)$.这样做的理论依据是一个复杂的分布可以通过足够复杂的映射,从每一维分量都服从高斯分布的变量来生成.如figure2所示. 比如说,如果$P(X|z,\theta)=N(X|f(z,\theta), \sigma^2 I)$中的$f(z, \theta)$是一个神经网络表达的复杂映射,那么网络的前几层可能就是$z$到latent variable的分布的映射,后几层才是从latent variable到X的映射.

### 设定目标

现在我们的问题是如何计算式(1).一般来说,对于大多数的$z$,$P(X|z)$都接近0,对计算P(X)的贡献很小.VAE的关键思路就是只采样那些很可能会产生$X$的$z$来计算$P(X)$.这意味着我们需要一个新的分布函数$Q(z|X )$,它表示给定$X$情况下的$z$的分布.这时计算$E_{z\sim Q}{P(X|z)}$就比较简单了.

接下来假设$z$服从一个任意的分布$Q(z)$,而不是简单的标准正态分布.我们首先要把 $E_{z\sim Q}{P(X|z)}$ 和$P(X)$联系起来. 下面先给出Kullback-Leibler divergence(KL divergence, 记作 $\mathbb{D}$ ),它描述了两个分布之间的差异:
$$
D[Q(z)||P(z|X)]=E_{z\sim Q}[logQ(z)-logP(z|X)]
$$
使用贝叶斯公式展开:
$$
D[Q(z)||P(z|X)]=E_{z\sim Q}[logQ(z)-log\frac{P(X|z)P(z)}{P(X)}]\\
=E_{z\sim Q}[logQ(z)-logP(X|z)-P(z)] + logP(X)
$$
再做整理:
$$
logP(X)-D[Q(z)||P(z|X)]=E_{z\sim Q}[logP(X|z)]-D[Q(z)||P(z)]
$$
这里$X$是固定的,而$Q(z)$是任意的分布(而不是那个能够产生最佳的可以重建$X$的$z$的分布).由于我们的目标是最大化$P(X)$,所以应该让$Q$依赖$X$:
$$
logP(X)-D[Q(z|X)||P(z|X)]=E_{z\sim Q}[logP(X|z)]-D[Q(z|X)||P(z)]
$$
这个式子是VAE的核心.它的左边是我们想最大化的量.右边是我们可以计算并通过SGD来最优化的量.右边也具有一个Autoencoder的"形式",Q把$X$encode到$z$,P把$z$decode到$X$

$P(z|X)$描述了给定$X$,什么样的$z$更可能产生和$X$相近的数据.我们没有办法直接计算$P(z|X)$,但是如果我们对模型做了足够多的优化,那么$D[Q(z|X)||P(z|X)]$就足够小,我们可以直接使用$Q(z|X)$来计算$P(z|X)$.

### 优化目标

接下来我们讨论如何使用梯度下降法来优化式(5)的右端项.首先我们令$Q(z|X)=N(z|\mu(X,\theta),\Sigma(X,\theta))$,其中$\theta$代表从数据中学习到的参数,我们再之后的推导中常常省略它.在实际中,$\mu$和$\Sigma$往往是用神经网络来拟合,而且$\Sigma$限制为对角矩阵,这样更易于计算.

两个高斯分布的KL divergence为:
$$
D[N(\mu_0, \Sigma_0)||N(\mu_1,\Sigma_1)]=\frac{1}{2}(tr(\Sigma_1^{-1}\Sigma_0)+(\mu_1-\mu_0)^T\Sigma_1^{-1}(\mu_1-\mu_0)-k+log\frac{|\Sigma_1|}{|\Sigma_0|})
$$
所以:
$$
D[N(\mu,\Sigma)||N(0, I)]=\frac{1}{2}(tr(\Sigma)+\mu^T\mu-k-log|\Sigma|)
$$
我们可以通过采样的方式来逼近$E_{z\sim Q}[logP(X|z)]$,但是这样需要很多个$z$的采样,很多次$f(z,\theta)$的计算.因此,我们只选取一个$z$并且把对应的$logP(X|z)$作为$E_{z\sim Q}[logP(X|z)]$的估计.这样做是因为我们还会对数据集中所有的数据点做梯度下降.实际上我们要优化的式子为:
$$
E_{X\sim D}[logP(X)-D[Q(z|X)||P(z|X)]]=E_{X\sim D}[E_{z\sim Q}[logP(X|z)]-D[Q(z|X)||P(z)]]
$$
对这个式子求梯度,算符会从期望外移到期望内.所以我们可以采样一个$X$和一个$z$,然后计算下式的梯度:
$$
logP(X|z)-D[Q(z|X)||P(z)]
$$
![figure4](/images/vae/vae.png)

然后将许多次采样的结果平均起来,就是式8的梯度了.然而式9有一个严重的问题,就是$E_{z\sim Q}[logP(X|z)]$本来是依赖$Q$的,但是在式9中这种依赖消失了.用更形象的方式解释,那就是式9对应的网络是figure4中左边所示的网络. 随机梯度下降并不能处理网络中出现的随机采样操作. 所以我们需要将这个随机采样操作移到输入层,这种技巧被称为重参数化方法(reparameterization trick):
$$
E_{X\sim D}[E_{z\sim Q}[logP(X|z)]-D[Q(z|X)||P(z)]]\\=E_{X\sim D}[E_{\epsilon\sim N(0,I)}[logP(X|z=\epsilon*\Sigma^{\frac{1}{2}}(X)+\mu(X))]-D(Q(z|X)||P(z))]
$$
这些期望都和模型参数无关,所以我们只需要对期望内部的部分求梯度即可.

### 使用模型

![figure5](/images/vae/test.png)

当我们需要生成新的样本,只需要将$z\sim N(0,I)$输入到decoder中即可.

而如果需要知道一个数据点$X$的概率就不那么简单了,因为式5的右端项只是$P(X)$的下界而已.

### interpretation

#### 误差项$D[Q(z|X)||P(z|X)]$

.......

#### 信息论的解释

.......

#### 正则化

.......

