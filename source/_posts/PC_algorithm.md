---
title: PC Algorithm
categories: ['PaperNotes']
---

# PC Algorithm

## Find the Equivalence Class of a DAG

### Concepts and Notations

#### Faithfulness[^jmlr2005]

A probability distribution $P$ is said to be faithful with respect to a graph $G$, if conditional independencies of the distribution can be inferred from **d-seperation** in the graph $G$ and vice-visa. More precisely, consider a random vector $\mathbf{X}\sim P$. Faithfulness of $P$ with respect to $G$ means, for any $i\ne j\in V$ and any set $\mathbf{s}\in V$,

$$
\mathbf{X}^{(i)}\bot \mathbf{X}^{(j)}\ \text{given} \ \mathbf{s}
\\\leftrightarrow\\
i\ \text{and}\ j \text{are d-seperated by the set}\ s
$$

 

#### D-Seperation[^mit6.034]

The Bayes net assumption says, "each variable is conditionally independent of its non-descendants, given its parents".

D-seperation is a formal procedure using this statement.

1.  Draw the ancestral graph.
2.  For each pair of variables with a common child, draw a undirected edge between them.
3.  Replace directed edges with undirected edges.
4.  Delete the givens and their edges.
5.  If the variables are disconnected, or one or more are missing, they are guaranteed to be independent. 'Connected' means there is a path between them, even though they are not directly connected.

![image-20190715161555478](Einstein-Summation-Convention/image-20190715161555478.png)



[^jmlr2005]: Kalisch, Markus, and Peter Bühlmann. "Estimating high-dimensional directed acyclic graphs with the PC-algorithm." *Journal of Machine Learning Research* 8.Mar (2007): 613-636.
[^mit6.034]: http://web.mit.edu/jmn/www/6.034/d-separation.pdf