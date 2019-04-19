---
title: 'Distinguish between {} and () when initializing'
date: 2016-07-28 16:10:01
tags: ["c++", "c++11", "initialize", "brace", "parenthese"]
categories:
- 读Effective Modern C++后有感
---

介绍c++中通过`()`和`{}`初始化对象的不同。需要这两种方式各有利弊，视情况选择。

<!-- more -->
在c++,初始化一个变量有四种方式:
``` c++
int a1 (1);
int a2 = 2;
int a3 {3};
int a4 = {4};//
```
当然，初始化像`int`这样的内建类型的时候实际上没有任何区别，我们真正需要关注的是初始化一个对象的时候发生了什么。同时，第四种方式中的赋值号在绝大多数的处理中都被忽略，它和第三种方式直接使用大括号是完全一样的，因此我将不再讨论它。
在介绍{}之前，先说明一下`=`，初始化语句中的`=`不表示赋值，而表示拷贝构造。
eg:
``` c++
Object o1 (); // default constructor
Object o2 = o1; // copy constructor
o1 = o2; // operator =
```

- brace for uniform initailization

设计`{}`初始化的一个目的是实现一致的初始化。
我们可以使用`{}`去直接初始化一个类(`class`, `struct`)的内容:
``` c++
struct Object
{
    int a;
    double b;
};
Object o (1, 2.0);
```
不需要构造函数，我们可以直接按照`struct`中的成员变量的生命顺序去初始化一个对象。当然这种时候初始化的对象需要满足一定条件:
- 初始化一个数组
- 初始化满足下列条件的类(`class`, `struct`):
    - 没有`private`或者`protected`的成员变量
    - 没有自定义的构造函数,包括从基类继承的
    - 没有`virtual`,`private`或者`protected`的基类 (virtual继承的内容我之后大概会学习一下，flag)
    - 没有`virtual`成员函数，即虚函数
这种类叫做聚合（[aggregate](http://en.cppreference.com/w/cpp/language/aggregate_initialization)）

这种类有的时候会很方便，比如`std::array`就是这样设计的。
同时有的库实现了和这种规则风格一致的{}初始化接口:
``` c++
std::vector<int> v{2, 3};//表示v的元素是2，3而不是v有2个元素，每个都被初始化为3
```

在c++11之后，我们可以在类的声明中对成员变量进行初始化，就像在Java中那样，这能避免很多漏洞。但是在这个时候，不能使用`()`,只能使用`{}`和`=`:
``` c++
class Widget
{
private:
    int x {0}; //ok
    int y = 0; //ok
    int z (0); //error
};
```

在一些禁止进行拷贝的类中，比如`std::actomic`(表示需要学习一下)和`std::unique_ptr'，使用=初始化又是被禁止的:
``` c++
std::unique_ptr<Object> o1 (new Object()); //ok
std::unique_ptr<Object> o2 = o1; // error
std::unique_ptr<Object> o3 {new Object()}; //ok
```

在c++中有一条规则，*most vexing parse*,他的意思是任何能被看成声明都被看成是声明而不是定义。
比如下面的代码，就会被看成函数声明而不是对象定义:
``` c++
Object o ();//声明了一个函数
```
然而使用{}就不存在这种问题:
``` c++
Object o {};
```

- narrowing convertion among built-in types
使用`{}`时禁止了内建类型的implicit narrowing convertion，即导致精度损失的隐式类型转换。
对于`()`和`=`不禁止implicit narrowing convertion的原因是避免无数的老代码不兼容。然而对于新的工程，使用`{}`来避免implicit narrowing convertion应该是正确的选择。

- which function will be called?
当我们定义了以`std::initialize_list`为参数的构造函数的时候，会优先调用这些函数。如果我们没有定义这些函数或者他们都无法匹配类型的时候，才会去试图调用普通的构造函数，这时`{}`中的参数会和`()`一样地处理。
这其中有一些陷阱:
eg1:
``` c++
class Object
{
public:
    Object (int a, bool b);
    Object (int a, double b);
};
Object o1 (1, true);// first
Object o2 {1, true};// first
Object o3 (1, 2.0);// second
Object o4 {1, 2.0};// second
```
eg1看起来很正常，但是当我们定义一个新的函数之后就会出现问题。
eg2:
``` c++
class Object
{
public:
    Object (int a, bool b);
    Object (int a, double b);
    Object (std::initializer_list<double> il);
};
Object o1 (1, true);// first
Object o2 {1, true};// third, int和bool被强制转换为double
Object o3 (1, 2.0);// second
Object o4 {1, 2.0};// third, int被强制转换为double
```
甚至在拷贝和移动的时候也会出现问题。
eg3:
``` c++
class Object
{
public:
    Object (int a, bool b);
    Object (int a, double b);
    Object (std::initializer_list<double> il);
    operator float () const;//类型转换函数，长见识了......
};
Object o5 (o4);//copy constructor
Object o6 {o4};//o4先被转换为float，在被转换为double
Object o7 (std::move (o4));// move constructor
Object o8 {std::move (o4)};//同o6
```
只有在使用`std::initializer_list`的构造函数实在是没有办法适用的时候才会使用普通的函数。
eg4:
``` c++
class Object
{
public:
    Object (int a, bool b);
    Object (int a, double b);
    Object (std::initializer_list<std::string> il);
};
Object o1 (1, true);// first
Object o2 {1, true};// first
Object o3 (1, 2.0);// second
Object o4 {1, 2.0};// second
```
另一个陷阱在于空的`{}`。直接使用`{}`会调用空参数构造函数而不是认为它是空的`std::initializer_list`。
eg5:
``` c++
class Object
{
public:
    Object ();
    Object (std::initializer_list<std::string> il);
};
Object o1 ();//first
Object o2 {};//first
Object o3 ({});//second
Object o4 {{}};//second
```
因为这种种问题，我们说{}和()其实是不分优劣的。

## 总结
{}:
通用性
安全性，禁止narrowing conversion
规避most vexing parse
():
和无数的老代码保持一致
避免使用`auto`+`{}`出现的错误（见[Let's talk about the c++ auto](https://lizeyan.github.io/2016/07/24/Let-s-talk-about-the-c-auto/)）
避免初始化对象是调用函数和预期不一致出现的错误。

在一个工程中坚持一种风格，在必要的时候使用另一个。或者像`std::vector`这样使用`()`和`{}`有不同的语义。

