---
title: 'Use std::unique_ptr for exclusive-ownership resource management'
date: 2016-08-17 10:21:20
tags: ["c++", "c++11", "unique_ptr"]
categories:
- 读Effective Modern C++后有感
---
使用`std::unique_ptr`管理独占的资源。

<!-- more -->

`std::unique_ptr`可能是最简单最方便的智能指针。一般情况下，`std::unique_ptr`的大小和原生指针是相同的，同时它们的操作执行的指令也几乎完全相同。所以使用`std::unique_ptr`相比原生指针没有什么性能损耗，即使在时间空间非常紧张的环境下也可以使用。

`std::unique_ptr`表达的语义是对指针指向对象的独占性所有权。一个非空的`std::unique_ptr`总是拥有它所指向对象的所有权。移动`std::unique_ptr`会转移所有权，而拷贝`std::unique_ptr`是被禁止的。通过这种方式，`std::unique_ptr`保持了对资源的独占性。在`std::unique_ptr`的析构函数中，`std::unique_ptr`会释放对资源的控制，默认情况下的处理方式是直接`delete`内含的原生指针。相比原生指针，最大的好处是可以保证资源总是会被释放，并且只会释放一次。即使是程序中遇到异常等打断运行流的情况，依然能够正确释放资源。如果你需要特化释放资源的方式，也是可以的。
``` c++
class Object
{
public:
	int a = 0;
	double b = 0.0;
	static std::function<void(Object*)> delInvmt;
	virtual ~ Object () = default;
};
std::function<void(Object*)> Object::delInvmt = [] (Object* object)
{
	std::cout << "delete" << std::endl;
	delete object;
};
class O1: public Object
{
public:
	char c = '0';
};
class O2: public Object
{
public:
	long d = 0L;
};
template <typename... Ts>
std::unique_ptr<Object, decltype(Object::delInvmt)> makeObject (Ts&&... params)// ignore ... now if you don't understand
{
	std::unique_ptr<Object, decltype(Object::delInvmt) > rslt (nullptr, Object::delInvmt);
	if (/* O1 */ true)
	{
		rslt.reset (new O1(std::forward<Ts>(params)...));// ignore std::forward now if you don't understand
	}
	else /* O2 */
	{
		rslt.reset (new O2(std::forward<Ts>(params)...));// ignore std::forward now if you don't understand
	}
	return rslt;
}
int main ()
{
	auto x = makeObject ();
	std::cout << sizeof (x) << std::endl; // 20
}
```
- Object::delInvmt是一个lambda函数。使用lambda函数作为`std::unique_ptr`的释放器既方便又高效（为什么高效？后面解释）。
- 当我们指定`std::unique_ptr`的释放器的时候，我们需要在模板参数中添加释放器的类型，同时在构造函数中传入释放器。关于`decltype`参考[decltype](https://lizeyan.github.io/2016/07/24/c-%E7%B1%BB%E5%9E%8B%E6%8E%A8%E5%AF%BC/)
- 我们不能直接用原生指针给`std::unique_ptr`赋值，需要使用`std::unique_ptr::reset`函数设置。
- 使用`std::forward`是为了完美转发，以后再学习。
- 使用`std::unique_ptr`可以像使用原生指针一样使用多态。为此`Object`需要虚析构函数。
- 在c++14，`makeObject`的返回值其实可以写成`auto`：
```
class Object
{
public:
	int a = 0;
	double b = 0.0;
	virtual ~ Object () = default;
};
class O1: public Object
{
public:
	char c = '0';
};
class O2: public Object
{
public:
	long d = 0L;
};
template <typename... Ts>
auto makeObject (Ts&&... params)// ignore ... now if you don't understand
{
	static auto delInvmt = [] (Object* object)
	{
		std::cout << "delete" << std::endl;
		delete object;
	};
	std::unique_ptr<Object, decltype(delInvmt) > rslt (nullptr, delInvmt);
	if (/* O1 */ true)
	{
		rslt.reset (new O1(std::forward<Ts>(params)...));// ignore std::forward now if you don't understand
	}
	else /* O2 */
	{
		rslt.reset (new O2(std::forward<Ts>(params)...));// ignore std::forward now if you don't understand
	}
	return rslt;
}
int main ()
{
	auto x = makeObject ();
	std::cout << sizeof (x) << std::endl; // 4
}
```

使用`std::unique_ptr`最大的好处在于一旦创建之后你完全不需要关心关于释放资源的种种麻烦的事情。`std::unique_ptr`自然会在最合适的地方释放且只释放一次资源。从调用`std::unique_ptr`者的角度来看，它实在是非常*sweet*:)

之前说我们可以认为`std::unique_ptr`的大小和原生指针是相同的。但是当我们使用自定义的删除器时，还要加上传出的删除器函数对象的大小。
- 使用lambda函数时最适合的，它的大小仅仅是所有capture到的变量的大小之和
- 使用`std::function`的话，大小会稍微大一些。可以参考上面的两个例子，大小差别很大。
- 使用一般函数，你不得不转换为函数对象`std::function`。

`std::unique_ptr`还可以支持数组
``` c++
std::unique_ptr<Object[]> os (new Object[10]);
for (int i = 0; i < 10; ++i)
	std::cout << os[i].a << std::endl;
```
因为模板参数不同，所以不用想原生指针那样担心分不清是指向一个对象还是指向数组。
不过使用STL容器是比使用数组更好的方案，强烈*不推荐*使用这种写法。