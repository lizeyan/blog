---
title: refence qualifiers
date: 2016-08-11 17:20:23
tags: ["c++", "c++11", "reference", "qualifier"]
categories:
- 读Effective Modern C++后有感
---

标记成员函数为`&`或者`&&`.

<!-- more -->
`&`或者`&&` 是针对成员函数的标记符，和`const`一样.
``` c++
class Object
{
public:
	void work () &;
	void work () &&;
	void work ();// error: 有了带引用标记之后的就不能有不带引用标记的了！
}
```
他的作用是对函数所在的对象(`*this`)做限制，`&`意为对象必须是左值,`&&`意为对象必须是右值.
eg:
``` c++
class Object
{
public:
	void work () & {std::cout << "lvalue" << std::endl;}
	void work () && {std::cout << "rvalue" << std::endl;}
};
Object makeObject () {return Object ();}
int main ()
{
	Object o;
	o.work (); // stdout: lvalue
	makeObject().work ();// stdout: rvalue
}
```
这个标记的作用可以通过下面的例子略知一二
eg:
``` c++
class Data
{
public:
	Data (const Data&) {std::cout << "copy" << std::endl;}
	Data (const Data&&) {std::cout << "move" << std::endl;}
	Data () {}
};
class Object
{
public:
	Data& getData () {return data;}
private:
	Data data;
};
Object makeObject () {return Object ();}
int main ()
{
	Object o;
	auto a = o.getData ();
	auto b = makeObject ().getData ();
}
/*
* stdout: copy copy
*/
```
这段代码是正确的，但是效率可以优化。问题在于`makeObject ()`返回的对象是右值,那么`getData()`完全可以返回一个右值从而减少一次拷贝.
eg:
``` c++
class Data
{
public:
	Data (const Data&) {std::cout << "copy" << std::endl;}
	Data (const Data&&) {std::cout << "move" << std::endl;}
	Data () {}
};
class Object
{
public:
	Data& getData () & {return data;}
	Data&& getData () && {return std::move(data);}
private:
	Data data;
};
Object makeObject () {return Object ();}
int main ()
{
	Object o;
	auto a = o.getData ();
	auto b = makeObject ().getData ();
}
/*
* stdout: copy move
*/
```
众所周知，`move`比`copy`不知道快到哪里去了，尤其是对象很大的情况下（比如大小为1000000的`std::vector<std::string>`);

总而言之，`&`或者`&&`就是让你可以针对左右值分别作不同的处理。
