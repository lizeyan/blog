---
title: Make const member functions thread safe
date: 2016-08-13 20:55:56
tags: ["c++", "c++11", "const", "thread safe"]
categories:
- 读Effective Modern C++后有感
---

保证`const`成员函数都是线程安全的。

<!-- more -->

假设我们有一个类用来处理多项式，其中有一个函数是用来求这个多项式的根的。因为求一个多项式的根并不会修改这个多项式本身，所以这个成员函数应该是`const`的
``` c++
class Polynomial
{
public:
	using RootsType = std::vector<double>; // --> https://lizeyan.github.io/2016/08/09/Prefer-alias-declarations-to-typedefs/
	RootsType roots () const;
};
```
考虑到计算根可能是个很费时个过程，我们希望计算过一次之后就缓存下来，之后可以直接返回这个缓存下来的值。
``` c++
class Polynomial
{
public:
	using RootsType = std::vector<double>; // --> https://lizeyan.github.io/2016/08/09/Prefer-alias-declarations-to-typedefs/
	RootsType roots () const
	{
		if (!rootsValid)
		{
			...
			rootsValid = true;
		}
		return rootsValue;
	}
}
private:
	mutable bool rootsValid {false}; // --> https://lizeyan.github.io/2016/07/28/Distinguish-between-and-when-initializing/
	mutable RootsType rootsValue {};
};
```
（插一句，`mutable`的语义是程序员确认这个变量的值对于对象的外在表现没有任何影响，因而编译器允许在`const`成员函数中修改其值）
但是，但用户使用这段代码的时候，用户会认为既然这个函数是`const`的，不会对`Polynomial`有任何影响，那么就可以这样使用:
``` c++
Polynomial p1, p2;
auto calcRoots = [] (const Polynomial& p) -> Polinomial::RootsType {return p.roots();};
std::thread t1 (calcRoots, std::ref(p1)), t2 (calcRoots, std::ref(p2));
```
如果有两个线程同时在运行同一个多项式的求根函数呢？按照用户所看到的声明来说，应当是安全的。但是实际上，两个线程可能同时对一块内存进行读写，这是不安全的(undefined behavior)。
为此我们需要加入同步控制：
``` c++
class Polynomial
{
public:
	using RootsType = std::vector<double>; // --> https://lizeyan.github.io/2016/08/09/Prefer-alias-declarations-to-typedefs/
	RootsType roots () const
	{
		std::lock_guard<std::mutex> g(m);
		if (!rootsValid)
		{
			...
			rootsValid = true;
		}
		return rootsValue;
	}
}
private:
	mutable std::mutex m;
	mutable bool rootsValid {false}; // --> https://lizeyan.github.io/2016/07/28/Distinguish-between-and-when-initializing/
	mutable RootsType rootsValue {};
};
```

在很多情况下，线程锁带来的开销过大了，我们可以用一种更简单的方法处理它:
``` c++
class Point
{
public:
	double distance () const noexcept
	{
		++callCount;
		return std::hypot (x, y);
	}
private:
	mutable std::actomic<std::size_t> callCount {0};
	double x, y;
};
```
这里，通过使用原子操作就能让对`callCount`的读写变成线程安全的，而不需要使用锁。
但是如果有两个或者更多的变量需要线程安全，那么原子操作就无能为力了:
``` c++
class Widget
{
public:
	int magicValue () const
	{
		if (cached)
			return cachedValue;
		else
		{
			cached = true;
			return cachedValue = expensiveComputation ();
		}
	}
private:
	mutable std::actomic<bool> cached{false};
	mutable std::actomic<double> cachedVlaue{0.0};
};
```
为什么呢？如果一个线程修改了`cached`之后但是还没有修改`cachedValue`，但是其他线程这时候使用`cached`判断然后返回`cachedValue`，那么就会出错。
如果我们调换`cached`和`cachedValue`赋值的顺序呢？
``` c++
class Widget
{
public:
	int magicValue () const
	{
		if (cached)
			return cachedValue;
		else
		{
			cachedValue = expensiveComputation ();
			cached = true;
			return cachedValue;
		}
	}
private:
	mutable std::actomic<bool> cached{false};
	mutable std::actomic<double> cachedVlaue{0.0};
};
```
那么`expensiveComputation ()`就可能被执行两次，这开销可能就非常大了。
因此下面的代码才是我们的标准答案:
``` c++
class Widget
{
public:
	int magicValue () const
	{
		std::lock_guard<std::mutex> g (m);
		if (cached)
			return cachedValue;
		else
		{
			cachedValue = expensiveComputation ();
			cached = true;
			return cachedValue;
		}
	}
private:
	mutable std::mutex m {};
	mutable bool cached{false};
	mutable double cachedVlaue{0.0};
};
```


最后强调，务必注意使你的库中的所有`const`函数都是线程安全的，除非你能够确认不会有人在多线程环境下调用它。
