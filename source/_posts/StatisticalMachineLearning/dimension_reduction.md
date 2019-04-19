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

