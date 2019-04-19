---
title: Dimension Reduction
categories:
  - StatisticalMachineLearning
---

## PCA

### Algorithm

$$
\newcommand{\vv}[1]{\boldsymbol{#1}}
$$



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

$$


