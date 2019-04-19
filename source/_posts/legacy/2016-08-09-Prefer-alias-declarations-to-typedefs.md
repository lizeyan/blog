---
title: Prefer alias declarations to typedefs
date: 2016-08-09 20:19:55
tags: ["c++11", "alias", "typedef"]
categories:
- 读Effective Modern C++后有感
---

使用alias declatration代替`typedef`。

<!-- more -->
使用STL是令人愉快的，但是我们肯定不想每次输入下面这个类型:
``` c++
	std::unique_ptr<std::unordered_map<std::string, std::pair<int, std::vector<std::string> > > >;       
```
为此我们可以使用typedef或者alias declatration来简化代码:
``` c++
typedef std::unique_ptr<std::unordered_map<std::string, std::pair<int, std::vector<std::string> > > > UPtrMSIV;
```
``` c++
using UPtrMSIV = std::unique_ptr<std::unordered_map<std::string, std::pair<int, std::vector<std::string> > > >;
```
`typedef`和alias declaration的功能是完全一样的，都是定义一个类型的别名，那么我们为什么要抛弃`typedef`呢？

我们先想想如何定义函数指针的别名:
``` c++
typedef void (*FP) (int, std::string);
```
``` c++
using FP = void (*) (int, std::string);
```
可以看出alias declaration比`typedef`更加简洁而且容易理解.不过这个对于绝大多数熟悉C Language的都不是问题,alias declaration还有其他更加技术上的优点.
当我们的视野从一般的代码拓展到模板时,就很容易发现问题:alias declaration是支持模板的.
eg1:
``` c++
template <typename T>
using MyList = std::list <T, MyAlloc<T> >;

MyList<std::string> ls;
```
而同样的功能用typedef实现起来就很麻烦。
eg2:
``` c++
template <typename T>
struct MyList
{
	typedef std::list<T, MyAlloc<T> > type;
}

MyList<T>::type ls;
```
而当我们在另一个模板中使用`MyList`时，又会有新的问题
eg3:
``` c++
template <typename T>
struct Widget
{
private:
	MyList<T>::type ls; // error
}
```
上面这段代码看起来意义明确，但是无法通过编译。原因在于`MyList<T`>的定义到底是什么是需要编译时特化之后才能知道的，那么此时`MyList<T>::type`我们没有办法确认它是一个类型还是一个变量。
此时我们必须通过`typename`关键字显式地声明`MyList<T>::type`是一个类型名:
``` c++
template <typename T>
struct Widget
{
private:
	typename MyList<T>::type ls; // error
}
```
但是使用alias declaration的话，`MyList`本身就是一个alias模板，所以`MyList<T>`一定是一个类型别名而不会是别的什么。因此下面的代码是正确的:
``` c++
template <typename T>
struct Widget
{
private:
	MyList<T> ls; // error
}
```

在c++11的标准库中，有一些使用了类似`eg2`的技术，比如`<type_traits>`中的`std::remove_const<T>::type`, `std::remove_reference<T>::type`。使用它们的时候务必注意`typename`;
c++标准委员会当然是清楚alias declaration的好的，在c++11中，为之前的使用`typedef`的库都添加了alias declaration的版本。
eg:
``` c++
template< class T >
using remove_cv_t = typename remove_cv<T>::type; //since c++14
```