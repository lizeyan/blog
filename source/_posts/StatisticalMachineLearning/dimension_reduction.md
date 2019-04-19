---
title: Dimension Reduction
categories:
  - StatisticalMachineLearning
---

## PCA

### Algorithm

{% raw %}
$$
\newcommand{\vv}[1]{\boldsymbol{#1}}
$$


{% endraw %}

Given data matrix $\mathbf{X}$, get the $d$-largest eigenvalues $\lambda_1, ..., \lambda_d$ and correbounding egivenvectors $\vv{u}_1, \vv{u}_2, ..., \vv{u}_d$

let $\mathbf{U}=\begin{bmatrix}\vv u_1, \vv u_2,..., \vv u_d\end{bmatrix}$

Encode: $\mathbf{U}^\top \mathbf X$

Decode: $ \mathbf{U} \mathbf Z$

​	

### Maximum Variance Formulation

#### 1-d case

The projection direction $\vv{u}$ satisfies $||\vv{u}||=1$
$$
y=\vv{u}^\top\vv{x}\\
\bar{\vv{y}}=\vv{u}^\top\bar{\vv{x}}\\
var(\vv{y})=\frac{1}{N}\sum_{i=1}^{N}(\vv u^\top\vv{x}_n-\vv{u}^\top\bar{\vv{x}})^2\\
=\vv{u}^\top \mathbf{S} \vv{u}, \mathbf{S}=\frac{1}{N}(\vv{x}_n-\bar{\vv{x}})(\vv{x}_n-\bar{\vv{x}})^\top
$$

$$
\hat{\vv{u}}=\text{argmax}_\vv{u}\vv{u}^\top \mathbf{S} \vv{u}\\
s.t.\>\> \vv{u}^\top\vv{u}=1
$$

Solve it, we get
$$
\mathbf{S}\vv{u}=\lambda\vv{u}\\
\lambda=\vv{u}^\top \mathbf{S} \vv{u}
$$
Therefore $\lambda$ is the largest eigen-value.

#### add more component

$$
\hat{\vv{u}}_2=\text{argmax}_\vv{u}\vv{u}^\top \mathbf{S} \vv{u}\\
s.t.\>\> \vv{u}^\top\vv{u}=1 \\
\>\> \vv{u}_1^\top\vv{u}=0
$$


$$
\mathbf{S} \vv u_2 - \lambda \vv u_2 - \gamma \vv u_1=0\\
\vv u_1^\top \mathbf{S} \vv u_2 - 0 - \gamma = 0\\
\mathbf{S} \vv u_2 - \lambda \vv u_2=0\\
\lambda=\vv u_2^\top \mathbf{S} \vv u_2
$$

### Minimum Error Formulation

A set of complete orthonormal basis
$$
\{\vv u_1,\vv  u_2, ..., \vv u_n\}
$$
Then $\vv x$ can be represented by $\vv{x}=\sum_i \alpha_i \vv u_i, \alpha_i=\vv{x}^\top\vv u_i$

Consider a low-dimension representation:
$$
\vv{x}_n=\sum_{i=1}^{d}z_{ni}\vv u_i + \sum_{i=d+1}^{D}b_i\vv u_i
$$

$$
J=\frac{1}{N}\sum_{n=1}^{N}||x_n-\hat x_n||^2
$$

$$
\frac{dJ}{dz_{ni}}=2(x_n-\sum_{i=1}^dz_{ni}u_i-\sum_{i=d+1}^Db_iu_i)u_i=0\\
x_n
$$

