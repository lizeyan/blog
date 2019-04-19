---
title: Basic Neural Network--Introduction to MLP and CNN
date: 2017-03-8 09:07:11
tags: ["Neural Network", "MLP", "CNN"]
---

本文通过介绍多层感知器(Multilayer Perceptron, MLP)和卷积神经网络(Convolution Neural Network, CNN)来引导大家认识神经网络,它们都是最基本的深度神经网络.

<!--more-->

{% raw %}

<div class="graphical-notebook readonly" gid="5933d1a40f5b83c0fe7001d1" style="height:800px;"></div><script src="https://gn-web.somefive.com/graphical-notebook.js"></script>

{% endraw %}

## 感知器 Perceptron

感知器是我们的神经元的简单抽象,由Frank Rosenblatt在1957年提出,是一种最简单形式的神经网络.我们看一下感知器的样子:

![perceptron](/images/NN/perceptron.png)

感知器的输入是 $x_1,x_2,....,x_n$ ,输出是一个值 $y$ .

$$
y=f(\sum_{i=1}^{N}w_i\cdot x_i+\theta)
$$

用向量化的数学表达式可以将其表示为

$$
y=f(\vec{W}\cdot\vec{X}+\theta)
$$

其中$f()$是激活函数,用来将线性运算的结果进行映射.最简单的激活函数莫过于

$$
f(x)=\begin{cases}1 & x \ge 0 \\ 0 & x < 0\end{cases}
$$

感知器通过对输入进行线性运算来进行分类,可以解决相当复杂的问题.但是感知器的一个本质缺陷在于它不能处理线性不可分的问题.比如下面这一组数据(也就是著名的XOR问题):

| $x_1$ | $x_2$ | label |
| ----- | ----- | ----- |
| 0     | 0     | 0     |
| 1     | 1     | 0     |
| 0     | 1     | 1     |
| 1     | 0     | 1     |

对于点(0,0)和(1,1),他们属于类别0;对于点(0,1)和(1,0)他们属于类别1. 这个问题是线性不可分的,看起来很简单,却超出了感知器的处理能力. 感知器的这一缺点导致人工神经网络从1960年代到1980年代长期停止,在1974年反向传播算法被应用于神经网络,产生了下面会讲到的多层感知器,神经网络领域才开始复兴.

那么我们怎么去训练这个神经网络呢?

感知器的表达式中的$\vec{W},\theta$都是可训练的参数,为了表达的简单,我们规定$\vec{X}'=[1,\vec{x}^T]^T, \vec{W}'=[\theta,\vec{W}]$

那么$\vec{W}\cdot\vec{X}+\theta=\vec{W}'\cdot\vec{X}'$,现在我们要训练的就只有$\vec{W}'$了.

我们的训练数据需要包括输入和类别,然后用训练数据的类别和训练过程中感知器输出的类别比较来调整参数.这种学习方式就是监督学习(Supervised Learning)

一个简单的学习策略是这样的

$$
w_i(n+1)=w_i(n)+\eta(T(n)-y(n))x_i(n)
$$

其中$T(n),y(n)$分别表示第n次训练是的训练数据的类别和感知器输出的类别.$\eta$是一个训练参数,我们称其为学习速率

## 多层感知器(MLP)

我们之前提到过,感知器只能处理线性可分的问题.多层感知器对这一点做出了重要的改进.多层感知器的结构其实很简单,就是很多个感知器组合在一起:

![mlp](/images/NN/mlp.png)

多层感知器和感知器的使用方法是一样的,只是处理能力有的本质的改变,多层感知器遇到的最大问题其实是如何训练.

多层MLP的每一层可以用这样的形式来统一地描述,这种矩阵化的形式也更方便实现:

$$
\vec{y}_{n\times1}=f(W_{n\times m}\cdot \vec{x_{m\times1}}+\vec{b_{n\times 1}})
$$

## 多层感知器的训练--反向传播算法(Back Propagation, BP)

反向传播算法的第一阶段是将输入从输入层输入,进行前馈计算,得到激励响应.然后将激励响应和训练目标求差,得到误差

$$
\epsilon_j(n)=T_j(n)-y_j(n)
$$

其中$j$表示输出神经元所处的位置,n表示迭代的次数

我们用二次误差来表示前馈的损失(Loss):

$$
e(n)=\sum_je_j(n) \\
e_j(n)=\frac{1}{2}{\epsilon_j(n)}^2
$$

反向传播算法的第二阶段是将误差进行反向传播,更新权值$\vec{W}$

我们首先要知道,权值的更新通过误差对权值的梯度进行:

$$
w_{kij}(n+1)=w_{kij}(n)+\Delta_{w_{kij}}=w_{kij}(n)-\eta\frac{\partial e(n)}{\partial w_{kij}}
$$

那么问题的关键就在于求解$\frac{\partial e(n)}{\partial w_{kij}}$

($k$表示权值所在的层数,i表示神经元在该层的位置)

(以下是一大段数学推导)

$$
\frac{\partial e(n)}{\partial w_{kij}}={\frac{\partial e(n)}{\partial y_{ki}(n)}}\cdot{\frac{\partial y_{ki}(n)}{\partial u_{ki}(n)}}\cdot{\frac{\partial u_{ki}(n)}{\partial w_{kij}}}\\
\text{where  }  y_{ki}(n)=f_{ki}(u_{ki}), u_{ki}=\sum_j{w_{kij}\cdot y_{(k-1)j}}
$$

$$
\frac{\partial u_{ki}}{\partial w_{kij}}=y_{(k-1)j}
$$

$$
\frac{\partial y_{ki}(n)}{\partial u_{ki}(n)}=f'_{ki}(u_{ki})
$$

若第k层是输出层,那么:

$$
\frac{\partial e(n)}{\partial y_{ki}(n)}=-(T_{ki}(n)-y_{ki}(n))
$$

如果是隐含层(即不是输出层的其它层)

$$
\frac{\partial e(n)}{\partial y_{ki}(n)}=\sum_{i'}\frac{\partial e(n)}{\partial y_{(k+1)i'}}\frac{\partial y_{(k+1)i'}}{\partial y_{ki}(n)}
$$

现在推导已经结束了,我们再来整理一下:

$$
\text{define } \Delta_{w_{kij}}=\eta \delta_{ki}(n)y_{(k-1)j}
$$

那么有:

$$
\delta_{ki}(n)=
\begin{cases}
f'_{ki}(u_{ki})(T_{ki}(n)-y_{ki}(n)) & \text{k is output layer}\\
f'_{ki}(u_{ki})\sum_{i'}\delta_{(k+1)i'}w_{ki'i} & \text{k is hidden layer}
\end{cases}
$$

所以可以看出,$\frac{\partial e(n)}{\partial w_{kij}}$是递推计算的.它的计算过程恰好和前馈过程是相反的:

- 在输出层由损失函数计算局部梯度$\delta$
- 将$\delta$沿着网络向前传播

![mlp_bp](/images/NN/mlp_bp.png)

最后再以矩阵化的形式描述一下局部梯度$\delta$的计算:

$$
\vec{\delta_{k}(n)}=
\begin{cases}
f'_{k}(\vec{u_{k}})\boldsymbol{\cdot}(\vec{T_{k}(n)}-\vec{y_{k}(n)}) &\text{k is output layer} \\
f'_{k}(\vec{u_{k}})\boldsymbol{\cdot}(W_k^T\cdot \vec{\delta_{k+1}})& \text{k is hidden layer}
\end{cases}
$$

注意$\boldsymbol{\cdot}$表示逐元素相乘,$\cdot$表示矩阵乘法

因为在BP算法过程中,需要对激活函数求导,所以激活函数必须是可导的,因此我们不能再使用简单的阶跃函数作为激活函数.实际中常用的激活函数有Sigmoid,ReLU,PReLU,Tanh等.

Sigmoid
$$
sigmoid(x)=\frac{1}{1+e^{-x}}
$$
ReLU
$$
ReLU(x)=\begin{cases}x & x \ge 0 \\ 0 & x < 0\end{cases}
$$
PReLU
$$
PReLU(x)=\begin{cases}x & x \ge 0 \\ \alpha x & x < 0\end{cases}
$$
其中参数alpha是可训练的参数.

Tanh
$$
Tanh(x)=\frac{sinh(x)}{cosh(x)}=\frac{e^x-e^{-x}}{e^x+e^{-x}}
$$

## 卷积神经网络(CNN)

### 卷积(Convolution)和池化(Pooling)

卷积和池化是CNN引入的两种基本操作,我们先分别介绍一下它们

#### 卷积(Convolution)

卷积是两个函数之间的操作, 结果是一个新的函数.用$*$表示.一维卷积的数学定义如下:

$f(x)*g(x)=\int_{-\infty}^{+\infty}f(t)g(x-t)dt$

对离散序列来说,卷积可以写成下面的形式

$$
f[n]*g[n]=\sum_{m=-\infty}^{+\infty}f[m]\cdot g[n-m]
$$

我们可以看到,两个长度分别为$n,m$的序列做卷积,结果的长度应该是$n+m-1$.

上面讲到的数学上的卷积在实际处理中被称为full卷积.为什么要强调是full呢?

假设有一个序列`[1,2,3,4,5]`,需要和卷积核`[1,2,3]`做卷积

如果直接运算,会得到:

$$
[1*3+2*2+1*3, 2*3+3*2+4*1, 5*1+4*2+3*3]=[10, 16, 22]
$$

这和定义是不符的,但是这个计算机中最方便实现,称其为valid卷积

full卷积则需要在前一个序列左右补上一定数量的0,即形成[0,0,1,2,3,4,5,0,0],然后再做valid卷积.

#### 池化(Pooling)

池化是将一个序列进行简化.常见的方法包括平均值池化和最大值池化,通过几个例子就可以说明:

$$
average\text{_}pooling_2([1, 2, 3, 4, 5, 6, 7,8])=[1.5,3.5,5.5,7.5] \\
average\text{_}pooling_4([1, 2, 3, 4, 5, 6, 7,8])=[2.5, 6.5] \\
max\text{_pooling}_2([1, 2, 3, 4, 5, 6, 7,8])=[2,4,6,8]\\
max\text{_pooling}_2([2,5,1,3,6,8,4,7])=[5,3,8,7]
$$

$upsample$是池化的逆操作,比如我们之前做的是$average\text{_}pooling_2$, 那么:

$$
upsample([1, 2, 3])=[1, 1, 2, 2, 3, 3]
$$

### 1D卷积神经网络

我们通过一个最简单的CNN展示它一般的结构:

![cnn](/images/NN/cnn.png)

实线表示层是卷积层,虚线表示的层是池化层.

在卷积层,通过下式计算这一层的输出

$$
y_{l+1}=f(\vec{y_l}*_{valid}\vec{w_l}+{b_l})
$$

$f()$仍然表示激活函数.从图上可以看到,从输入层到第一层做了两次卷积操作.通过两个不同的卷积核对输入做卷积,从而将输入扩展到多个频道(Channel)可以提高对输入的特征的提取能力.

在池化层,我们简单地对每一个频道做一次池化操作即可

最后一层是全连接层,全连接层其实就是之前讲的MLP的一层的结构.

### CNN的训练

CNN可训练的参数是全连接层的权重,以及卷积层的卷积核$\vec{W}$,偏移$b$

我们还是通过反向传播算法来更新权值.

和多层感知器的BP类似,我们要求的是$\frac{\partial e(n)}{\partial w_{ij}^k}$和$\frac{\partial e(n)}{\partial b_{ij}^k}$

($k$代表层数,$i$代表频道)

同样,我们仍然定义局部梯度,这样就只需要求解出局部梯度的递推式就可以了.

$$
\delta_{i}^k=-\frac{\partial e(n)}{\partial u_{i}^k(n)}
$$

对于输出层:

$$
\delta_{i}^k=(T_{i}^k-y_{i}^k)f'_{k}(u_{i}^k)
$$

对于全连接层:

$$
\vec{\delta_k}=\vec{W_k}^T\cdot \vec{\delta_{k+1}} \boldsymbol{\cdot}\vec{f'_{k}(\vec{u_k})}\\
\frac{\partial e(n)}{\partial \vec{w_{i}^k}}=\vec{\delta_k}(\vec{f(u_{k-1})})^T\\
\frac{\partial e(n)}{\partial b_{k}}=\vec{\delta_k}
$$

其中$\boldsymbol{\cdot}$表示的是逐元素相乘,而不是矩阵乘法.

对于卷积层:

$$
\delta_{i}^k=\sum_{q\in M}(\delta_{q}^{k+1}*_{full}W_{qi}^{k})\boldsymbol{\cdot}f'(u_i^k) \\
\frac{\partial e(n)}{\partial w_{qp}^k}=y_p^k*_{valid}\delta_q^{k+1}\\
\frac{\partial e(n)}{\partial b_q^{k}}=\sum_i{\delta_{qi}^{(k+1)}}
$$

其中的$M$表示第k层的第i个频道在(k+1)层生成的所有频道

对于(平均)池化层:

$$
\delta_i^k=\frac{1}{poolingsize}upsample(\delta_i^{k+1})\boldsymbol\cdot f'(u_i^k)
$$

