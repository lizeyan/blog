---
title: Classify rows in ndarray by specific column
date: 2017-02-23 09:07:11
tags: ["numpy", "python"]
---

如何在一个`ndarray`中以某一列的值将其分类?

<!--more-->

问题本身用一个例子来说明:
$$
A=\begin{bmatrix}
1 &  1& 3\\ 
2 &  2& 4\\ 
1 &  3& 5\\ 
2 &  4& 6\\ 
3 &  5& 7
\end{bmatrix}
$$
其中第一列是数值的`id`，后面是某种属性，我们希望按`id`将A变成下面这样
$$
A=[\begin{bmatrix}
1 &  1& 3\\ 
1 &  3& 5\\ 
\end{bmatrix},
\begin{bmatrix}
2 &  2& 4\\ 
2 &  4& 6\\ 
\end{bmatrix},
\begin{bmatrix}
3 &  5& 7
\end{bmatrix}]
$$

``` python
import numpy as np
a = np.asarray([[1, 1, 3], [2, 2, 4], [1, 3, 5], [2, 4, 6], [3, 5, 7]])
indices = np.argsort(a[:, 0])
arr_tmp = a[indices]
c = np.array_split(arr_tmp, np.where(np.diff(arr_tmp[:, 0])!=0)[0] + 1)
```

则

``` python
c == [array([[1, 1, 3],
       [1, 3, 5]]), array([[2, 2, 4],
       [2, 4, 6]]), array([[3, 5, 7]])]
```

如果我们还想再每一个`id`的属性中取最大值，则可以

``` python
d = np.asarray([np.max(k, axis=0) for k in c])
d == array([[1, 3, 5],
       [2, 4, 6],
       [3, 5, 7]])
```

