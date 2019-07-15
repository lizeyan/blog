---
title: Einstein Summation Convention
categories:
  - NumPy
---

## Common operations in this notation

$$
\mathbf{u}\cdot\mathbf{v}=u_iv^i
$$

$$
\mathbf{C}=\mathbf{A}\mathbf{B}\\
\Rightarrow
C^i_k=A^i_{j}B^{j}_k
$$

$$
trace(\mathbf{A})=A^i_{i}
$$

## NumPy Convention

$trace(A)$: `ii`

$diag(A)$: `ii->i`

`sum(A, axis=1)`: `ij->i`

$A^\top$: `ij->ji`

$\mathbf{u}\cdot\mathbf{v}$: `i,i`

$\mathbf{A}\mathbf{u}$: `ij,j->i`



