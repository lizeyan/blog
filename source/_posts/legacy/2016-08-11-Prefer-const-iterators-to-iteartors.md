---
title: Prefer const_iterators to iteartors
date: 2016-08-11 21:12:57
tags: ["c++", "c++11", "const", "iterator"]
categories:
- 读Effective Modern C++后有感
---
多使用`const_itrrator`.

<!-- more -->

(这篇其实没什么内容)

在任何能使用`const`的地方，你都应该使用它。
所以如果你不需要修改一个迭代器指向的对象时，就应该使用`const_iterator`而不是`iterator`。
在c++98中其实就有`const_itearator`，但是绝大多数配套的函数比如`std::vector::insert`都只接受`itearator`为参数。因为非常量是不能直接转换为常量的，所以使用`const_itearator`变得很麻烦。
在c++11中改变了这一切，你可以放心地到处使用`const_itearator`。

另一方面，c++11提供了非成员函数的`begin(Container)`,`end(Container)`函数。使用这样的函数而不是成员函数版本的，可以让你的代码更加有普适性。
比如说当你在写一个函数模板的时候，你就不能确定对方传入的容器是有`begin`成员函数的,传入的还可能是原生数组.
STL针对原生数组特化了`iterator`相关函数.对于第三方库中的容器,你也可以在添加`begin`，`end`的同时避免修改对方的实现。

``` c++
template <typename C, typename V>
void findAndInsert (C& container, const V& targetVal, const V& insertVal)
{
	auto it = std::find (std::cbegin(container), std::cend (container), targetVal);
	container.insert (it, insertVal);
}
```

