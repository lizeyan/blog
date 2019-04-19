---
title: Prefer deleted functions to private undefiened ones
date: 2016-08-11 13:42:33
tags: ["c++", "c++11", "delete", "private"]
categories:
- 读Effective Modern C++后有感
---
`deleted function`比起将函数声明为`private`好在哪里?

<!-- more -->

当你在工程中有一些函数不希望他人调用的时候，你需要禁止这个函数的调用。在C++98中，标准的写法是将成员函数声明为`private`同时不定义.这样用户会由于访问控制而无法调用该函数,如果是在类内或者友元类类中,也会因为未定义而出现连接错误.
eg1:
``` c++
class Single
{
private:
	Single (const Single& s);
	Single& operator= (const Single& s);
}
```
在c++11中，为这种需求提供了一种更简单的写法:
eg2:
``` c++
class Single
{
public:
	Single (const Single& s) = delete;
	Single& operator= (const Single& s) = delete;
}
```
这不仅仅是写法的改变。
首先`deleted function`即使在类内或者友元类也不能调用，这样你可以将被删除函数声明为`public`.如此可以让用户总是在编译的时候能够得到错误信息,而不是可能延迟到连接时.同时错误信息也更加明确,不是访问权限错误而是访问被删除的函数.
```
'Single::Single(const Single&)' is private
undefined reference to `Single::Single(Single const&)'
use of deleted function 'Single::Single(const Single&)'
```

同时，更重要的是`deleted function`可以被用于任何函数，而不只是成员函数。
eg3:
``` c++
bool isLucky (int number) {return number & 1;}
bool isLucky (bool) = delete;
bool isLucky (char) = delete;
bool isLucky (double) = delete;
isLucky (1);
isLucky ('a'); //error: use of deleted function 'bool isLucky(char)'
isLucky (true); //error: use of deleted function 'bool isLucky(bool)'
isLucky (1.0); //error: use of deleted function 'bool isLucky(double)'
isLucky (1.0f); //error: use of deleted function 'bool isLucky(double)'
```
通过这种方式禁止了用户通过隐式类型转换传入不正确的参数。值得注意的是，如果将参数类型为`double`的函数禁止掉，那么传入`float`也是不可以的。因为c++编译器往往倾向于把`float`隐式转换为`double`而不是`int`。

除了普通函数，还有模板函数也可以使用`delete`.
eg4:
``` c++
template <typename T>
void process (T* ptr);
```
此时我们不希望有人传入`void*`或者`char*`(因为这都是特殊情况，char*一般会被当成字符串处理),那么可以这样
eg5:
``` c++
template <>
void process (void*) = delete;
template <>
void process (char*) = delete;
```
这里有一个潜在的危险：你还需要显式地禁止`const void*`, `const char*`, `const volatile void*`, `const volatile char*`, `char16_t*`, `char32_t*`, `const char16_t*`等等等等类型。这是一个严重的缺陷，基础类型太多，能做的隐式类型转换更是太多，你很难想到所有的隐患。

如果你在类中定义模板成员函数，你是不能给不同的特化函数以不同的访问权限的，但是你可以将一些特化声明为`delete`.这也是很重要的.
eg6:
``` c++
class Single
{
public:
	template <typename T>
	void process (T) {}
private:
	template <>
	void process (char); //error: explicit specialization in non-namespace scope 'class Single'
};
```
eg7:
``` c++
class Single
{
public:
	template <typename T>
	void process (T) {}
private:
};
//只能在类外声明特化
template<>
void Single::process<char> (char) = delete;
```
