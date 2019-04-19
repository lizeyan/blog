---
title: Use constexpr whenever possible
date: 2016-08-12 22:58:23
tags: ["c++", "c++11", "constexpr"]
categories:
- 读Effective Modern C++后有感
---
再安利一个关键字`constexpr`。

<!-- more -->

`constexpr`是比较令人困惑的新特性，因为它很容易和`const`混淆。但是了解清楚`constexpr`的语义之后,你一定会想要使用它的。

首先说`constexpr objects`。当`constexpr`修饰一个变量的时候，它表明这个变量不仅是`const`的，而且还是在编译期（准确地说是编译和连接时）就能确定值的。
编译期就能确定值有很多好处：这些变量会被放到只读内存里，这对内存宝贵的嵌入式设备而言尤为宝贵；这些变量可以被用于代码中需要编译器常量的地方，比如数组的大小，模板参数，枚举值，alignment specifier(不知道该翻译成什么...)等等；编译期间初始化变量也可以减少运行时间。
`constexpr objects`满足下列条件:
- 属于文字类型([literal type](http://en.cppreference.com/w/cpp/concept/LiteralType)):
	- possibly cv-qualified void (since c++14,为了使`constexpr functions`的返回值能够是`void`)
	- 内建类型
	- 引用类型
	- 文字类型的数组
	- 满足下列所有条件的类
		- 使用trivial destructor。我理解是使用默认构造函数，并且所有成员变量和基类也都是这样
		- 是以下类型的一种：
			- 聚合(aggregate, 另一篇介绍过[Distinguish between {} and () when initializing](https://lizeyan.github.io/2016/07/28/Distinguish-between-and-when-initializing/))
			- 有至少一个`constexpr`构造函数
- 必须立即构造或者赋值。
- 构造函数的所有参数都必须是`constexpr`
- 调用的构造函数必须是`constexpr`的（下面介绍`constexpr`函数）。

`constexpr functions`表示的是一种能力。当`constexpr functions`接受的参数都是`constexpr`时，它的这个函数的返回值此时就是`constexpr`的，函数本身就可以在编译期运行。否则就和普通函数一样工作。它和`const`没有什么联系，`constexpr functions`可以不是`const`的。
`constexpr functions`有一些限制:
- 不能是虚函数
- 返回值必须是文字类型 （c++11中文字类型*不包括*`void`）
- 每一个参数必须是文字类型
- there exists at least one argument value such that an invocation of the function could be an evaluated subexpression of a core constant expression (for constexpr function templates, at least one specialization must satisfy this requirement , for constructors, use in a constant initializer is sufficient) (since C++14)) 实在没太理解具体的涵义:(
- 函数体要求
	- c++11: 只能包含下面的语句
		- static_assert
		- typedef 或者 alias declarations[参考](https://lizeyan.github.io/2016/08/09/Prefer-alias-declarations-to-typedefs/)
		- [using declarations](http://en.cppreference.com/w/cpp/language/namespace#Using-declarations)
		- [using directives](http://en.cppreference.com/w/cpp/language/namespace#Using-directives)
		- 恰好一个return语句
	- c++14: 不能包括下面的语句
		- 内联汇编
		- goto
		- 除了`case`和`default`之外的[标签](http://en.cppreference.com/w/cpp/language/statements#Labels)。
		- try block
		- 非文字类型变量的定义
		- static或者thread_local变量
		- 未初始化变量
		- if the function is a defaulted copy/move assignment, the class of which it is a member must not have a mutable variant member 懵逼....
eg:
``` c++
class Point
{
public:
	constexpr Point (double x = 0.0, double y = 0.0) noexcept : _x (x), _y(y) {}
	constexpr double x () const noexcept {return _x;}
	constexpr double y () const noexcept {return _y;}
	constexpr void setX (double x) noexcept {_x = x;}
	constexpr void setY (double y) noexcept {_y = y;}
private:
	double _x = 0.0, _y = 0.0;
};
constexpr Point reflection (const Point& p) noexcept
{
	Point result;
	result.setX (-p.x());
	result.setY (-p.y());
	return result;
}
int main ()
{
	constexpr Point p1 (1.5, 1.4);
	constexpr Point p2 = reflection (p1);
}
```

值得注意的是`constexpr`是你的函数接口的一部分，它可以尽可能放大你的函数的使用范围。如果你使用了`constexpr`但是之后决定放弃，那么可能导致大量调用它的代码无法编译。
