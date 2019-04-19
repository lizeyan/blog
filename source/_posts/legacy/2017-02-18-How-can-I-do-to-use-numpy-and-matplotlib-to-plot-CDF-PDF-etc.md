---
title: 'How can I do to use numpy and matplotlib to plot CDF and PDF?'
date: 2017-02-18 23:56:12
tags: ["python", "numpy", "matplotlib", "pyplot", "cdf", "pdf"]

---

如何在python3中使用numpy和matplotlib库处理数据并绘制累积分布函数(*Cumulative Distribution Function*, CDF),概率密度函数(*Probability Distribution Function*, PDF)

<!--more-->

1. 概率密度函数

   概率密度函数描述的是随机变量在一定范围内取值可能性的函数.该随机变量取值在[a,b]的概率为该函数在[a,b]的积分.

   首先,我们的数据是$n\cdot 1$维的

   ``` python
   import numpy as np
   from matplotlib import pyplot as plt
   data = np.random.normal(size=100000)
   ```

   然后使用numpy得到概率密度函数

   ``` python
   hist, bin_edges = np.histogram(data, bins='auto', normed=True)
   plt.plot(bin_edges[1:], hist)
   ```

   结果如图示

   ![pdf_1](/images/plot_cdf_pdf/pdf_1.png)

   PDF实际上就是数据的直方图分布的包络线.我们在上图的基础上再加上直方图分布,只需要再加一行即可

   ``` python
   plt.hist(data, 50, normed=1, alpha=0.9)
   ```

   结果如图示:

   ![pdf_2](/images/plot_cdf_pdf/pdf_2.png)

2. 累积分布函数

   CDF是PDF的积分,所以cdf总是从0开始,单调非减,最终到达1.

   基本的思路是得到数据的直方图分布,然后累积求和就得到CDF的近似取样

   ```python
   hist, bin_edges = np.histogram(data, bins='auto', normed=True)
   cdf = np.cumsum(hist * np.diff(bin_edges))
   plt.plot(bin_edges[1:], cdf)
   ```

   结果如图示

   ![cdf_1](/images/plot_cdf_pdf/cdf_1.png)
