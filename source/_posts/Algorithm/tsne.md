---
title: t-SNE
---

## Intro

## SNE

**Input**: 
$$
\{\mathbf{x}_i, \mathbf{x}_i\in \mathbb{R}^D\}_{i=1}^{N}
$$
**Output**:
$$
\{\mathbf{y}_i, \mathbf{y}_i\in \mathbb{R}^d\}_{i=1}^{N}, d<D 
$$
**Objective**

SNE uses a conditional likelihood to measure the distance between two points,  $p_{i|j}$, which represents the probability to pick $j$ when $i$ is chosen.
$$
p_{j|i}=\frac{\exp(-||\mathbf{x}_i-\mathbf{x}_j||^2)}{\sum_{k\neq i}\exp(-||\mathbf{x}_i-\mathbf{x}_k||^2)}
$$
Similarly, in the low dimension space, SNE uses $q_{j|i}$ to measure the distance between two mapping points.
$$
q_{j|i}=\frac{\exp(-||\mathbf{y}_i-\mathbf{y}_j||^2)}{\sum_{k\neq i}\exp(-||\mathbf{y}_i-\mathbf{y}_k||^2)}
$$
The objective function is to minimize the KL divergence between  

## t-SNE