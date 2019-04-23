---
title: boost
categories:
  - StatisticalMachineLearning
---

## Model Averaging: from CT to Boosting

In generally, Boosting > Random Forest > Bagging > Single Tree

### Classification Trees

The decision boundaries are along the axes.

### Bagging

Suppose $C(S, x)$ is a classifier for dataset $S$ and input point $x$.

To bag $C$, draw bootstrap samples $S_1, S_2, ..., S_B$ from $S$ with size $N$

$C_{\text{bag}}(x)=\text{Majority Vote}(C(S_i, x), i \in [1, B])$

### Random Forest

refine bagging

At each tree split ,randomly sample $m$ features and only consider these samples. Typically $m=\sqrt p$ or $m=\log p$, where $p$ is the total number of features.

RF tries to improve bagging by de-corelating the trees.s

### Boosting

Average many trees, but each grown from reweighed samples.
$$
C(x)=\text{sign}\sum_{n}\alpha_nC_n(x)
$$

#### Adaboost

1.  initialize observations' weights $w_i=\frac{1}{N}, i = 1, 2, ..., N$

2.  For m from 1 to M:

    1.  fit $C_m$ with observations with weights $w_i$

    2.  Compute weighted error rate:
        $$
        err_m=\frac{\sum_i w_i1_{C_m(x_i)\neq y_i}}{\sum_i w_i}
        $$



    3.  Update ratio $\alpha_m=\log\frac{1-err_m}{err_m}$
    
    4.  Update weights
        $$
        w_i \leftarrow w_i \cdot \exp(\alpha_m1_{C_m(x_i)\neq y_i})
        $$


    5.  Renormalize sum of $w_i$ to 1s

3.  return $C(x)=\text{sign}(\sum_{i=1}^{M}\alpha_mC_m(x))$



#### Additive Model

Boosting build a additive model:
$$
f(x)=\sum_{k=1}^{M}\beta_kC(x;\gamma_k)
$$
Traditional methods fit the parameters jointly. But Adaboost do it stagewisely.

#### Adaboost: Stagewise Modeling

Adaboost fit a stagewise logistic regression model $f(x)$ by stagewisely fit the loss:
$$
\mathcal{L}=\exp(-yf(x))
$$


Given $f_{M-1}(x)$, the solution to $\beta_M, \gamma_M$ is 
$$
\text{argmin}_{\beta, \gamma}\sum_{i=1}^{N}\exp(-y_i(f_{M-1}(x_i)+\beta C(x_i;\gamma)))
$$

##### Why Exponential Loss

![image-20190419140355191](boost/image-20190419140355191.png)

exp loss is a upper bound of 0-1 loss.

It leads to simple reweighting scheme.

binomial deviance can be more robust

#### General Stagewise Algorithm

![image-20190419140524731](boost/image-20190419140524731.png)

## Learning from Crowds

