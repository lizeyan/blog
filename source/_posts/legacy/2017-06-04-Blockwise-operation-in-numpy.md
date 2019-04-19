---
title: Blockwise operation in numpy
date: 2017-06-04 17:40:18
tags: ["numpy", "python"]
---

如何在numpy中让一个矩阵分块，对每个块进行操作。

<!--more-->

## Motivation

比如现在有n张图片，每张图片的尺寸为$w*h$。现在需要对图片中每个8*8的块做DCT变换，那么应该如何做？

最简单的是在后两个维度上使用for循环，但是这样效率比较低。我的做法是将原始$n * w * h$的ndarray进行分块，转换成一个$n * \frac{w}{8} * \frac{h}{8} * 8 * 8$的ndarray，然后再后两维调用dct,这样比直接for循环快得多。

这个问题在多媒体大作业第一次遇到，代码在https://github.com/lizeyan/Multimedia/blob/master/lab12/utility.py

## 滑动窗口

相比分块，更加通用的操作是用一个窗口在矩阵上移动（分块只是相当于步长等于窗口大小）

``` python
def sliding_window(matrix, block, step=(1, 1)):
    """
    用一个大小为block的滑动窗口在matrix上滑动，步长为step
    """
    shape = matrix.shape[:-2] + (int((matrix.shape[-2] - block[0]) / step[0] + 1), int((matrix.shape[-1] - block[1]) / step[1] + 1)) + block
    strides = matrix.strides[:-2] + (matrix.strides[-2] * step[0], matrix.strides[-1] * step[1]) + matrix.strides[-2:]
    return as_strided(matrix, shape=shape, strides=strides)
```



## 分块

``` python
def blockwise(matrix, block=(3, 3)):
    """
    将矩阵按照块大小变成分块矩阵，只处理最后两维。
    即步长等于块大小的滑动窗口
    """
    return sliding_window(matrix, block, block)
```



## 组合

如何将分块完的矩阵再组合起来？

``` python
def block_join(blocks):
    """
    将后四维作为分块矩阵，拼接起来
    """
    # 将后四维移到最前面
    blocks = np.rollaxis(_blocks, -1)
    for _ in range(3):
        blocks = np.rollaxis(blocks, -1)
    # 拼接
    joined = np.vstack(map(np.hstack, blocks))
    # 将前两维移到最后面
    for _ in range(2):
        joined = np.rollaxis(joined, 0, np.ndim(_blocks) - 2)
    return joined
```

## 测试

``` python
n = 25, 15
w = 1024
h = 512
a = np.random.randn(*n, w, h)
print("a.shape", a.shape)
b = blockwise(a, (8, 8))
print("b.shape", b.shape)
a1 = block_join(b)
print("a1.shape", a1.shape)
assert np.max(np.abs(a1 - a)) == 0
```

