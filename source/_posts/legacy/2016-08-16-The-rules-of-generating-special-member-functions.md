---
title: The rules of generating special member functions
date: 2016-08-16 13:14:08
tags: ["c++", "c++11", "spetial memeber functions"]
categories:
- 读Effective Modern C++后有感
---
介绍关于编译器自动生成特殊成员函数的规则。

<!-- more -->

在C++98中，会被编译器自动生成的特殊成员函数包括默认构造函数，析构函数，拷贝构造函数，拷贝赋值运算符四种。
这些函数只有在被掉用到而你又没有显式地声明它们的时候才会被编译器自动生成。其中默认构造函数更是只有没有任何构造函数的声明时才会被自动生成。
这些函数都是被隐式生成的，生成的函数都是`public`,`inline`的。除了在基类的析构函数是`virtual`的情况下会生成`virtaul`的析构函数之外,生成的其他函数都是`non-virtual`的。

在C++11中，会被隐式生成的函数还要加上移动构造函数和移动赋值运算符。
总结一下，以上提到的所有函数的函数原型如下:
``` c++
class Object
{
public:
	Object ();
	~ Object ();
	Object (const Object&); // T&, const T&, volatile T&, const volatile T&
	Object& operator= (const Object&); // T&, const T&, volatile T&, const volatile T&
	Object (const Object&&); // T&&, const T&&, volatile T&&, const volatile T&&
	Object& operator= (const Object&&); // T&&, const T&&, volatile T&&, const volatile T&&
};
```
移动构造函数，移动赋值和拷贝构造，拷贝赋值是很相似的。它们会尝试移动每一个非静态成员变量以及基类（`memberwise move`）。之所以说移动是因为不能保证每个成员或者基类都是可以移动的，<b style="color:red">*如果不能移动的话就会进行拷贝(这也是c++11对待所有移动操作的方式，不能移动就拷贝)*</b>。这又是为了兼容旧的代码而作的妥协。
然而这两类函数生成的方式又有些不一样。
拷贝构造函数和拷贝赋值操作符是独立的，声明一个并不会阻止编译器生成另一个。但是移动构造函数和移动赋值操作符是不独立的，声明一个会阻止另一个被生成。C++如此做的逻辑是这样的:既然你显式声明了某一个，比如说移动构造函数，说明用默认的方式移动是有问题的，那么用默认的移动方式赋值应当也会发生同样地问题。
同时，如果你显式声明了拷贝构造函数或者拷贝赋值运算符，那么两个移动函数都不会被生成。C++的逻辑是相似的：既然逐个拷贝是有问题的，那么逐个移动很可能也有问题。反之同理，声明任何移动操作也会阻止编译器生成拷贝操作。(禁止拷贝操作的方法是使用`delete`关键字，参见[delete](https://lizeyan.github.io/2016/08/11/Prefer-deleted-functions-to-private-undefiened-ones/))

你可能听说过*Rule of Three*.意思是如果你显式定义拷贝构造函数，拷贝赋值操作或者析构函数，那么你最好显式定义全部三个。其中的道理很明显，用户显式定义它们往往是因为这个类自己进行内存管理，在拷贝构造中完成的内存管理在其他拷贝操作中理当同样完成，析构时理当释放掉被管理的资源。按照这个规则，c++就应当在用户显式定义析构函数的时候禁止自动生成拷贝操作（反之同理）,用户显式定义任何拷贝操作的时候也应该禁止自动生成析构函数。但是C++98形成的时代这条规则未能形成共识，在C++11中，为了保持兼容性，就沿用了C++98的规则。
不过考虑到*Rule of Three*，C++11引入了一条新规则，任何显式定义了析构函数的类都不会自动生成移动操作。也就是说，移动操作仅仅在满足下面所有条件的情况下才会被生成:
- 没有任何显式定义的移动
- 没有任何显式定义的拷贝
- 没有显式定义的析构函数

事情变得复杂起来，尤其是考虑到<b style="color:red">c++11对待所有移动操作的方式:不能移动就自动转而使用拷贝</b>，依赖编译器自动生成这些特殊函数是很危险的事情。为此c++11引入了新关键字`default`（hhhhh,越来越复杂）
``` c++
class Object
{
public:
	Object () = default;
	virtual ~ Object () = default;
	Object (const Object&) = default; 
	Object& operator= (const Object&) = default;
	Object (Object&&) = default; 
	Object& operator= (Object&&) = default;
};
```
不过不得不说这个关键字提供了一些方便。比如说你要写一个基类，你需要它的析构函数是`virtual`的，同时自动生成的默认析构函数就足够了。这时你必须显式声明这个函数是`virtual`的，但是使用`default`就又可以直接让编译器生成具体实现。这时你还想要它支持移动操作，但是自动生成被禁止同时默认的移动方式是正确的，那么就有需要使用`default`。显式定义之后拷贝会被禁止，那么你又需要显式声明拷贝操作。
这个关键字还能避免一些bug。有的时候你依赖编译器自动生成这些特殊函数，但是在你调试的过程中可能不小心显式定义了某个函数。尽管函数体可能仅仅加了一些调试语句，但是编译器同样会改变自动生成的策略。很可能你的这个工程中的所有`move`不知不觉就都以`copy`执行了，这是比较难发现的bug。

<div style="color:red">
下面对上面提到的规则做一个总结:
- Default Constructor
	仅仅在没有自定义的构造函数时自动生成。
- Destructor
	没有自定义析构函数时生成。默认为`noexcept`。当且仅当基类的析构函数为`virtual`时声明为`virtual`。
- Copy Constructor
	实现方式为逐个拷贝非静态成员和基类。仅仅在没有自定义的拷贝构造函数时生成。如果有自定义的移动函数则`delete`。
- Copy Assignment Operator
	实现方式为逐个拷贝非静态成员和基类。仅仅在没有自定义的拷贝赋值运算符时生成。如果有自定义的移动函数则`delete`。
- Move Constructor and Move Assignment Operator
	实现方式为逐个尝试移动非静态成员和基类（不能移动则拷贝）。仅仅在没有自定义的拷贝函数，移动函数，析构函数时自动生成。

</div>
最后注意一下下面的情况
``` c++
class Object
{
public:
 	template <typename T>
 	Object (const T&);
};
```
尽管模板可以特化出拷贝构造函数，编译器仍然会直接自动生成拷贝构造函数。其他的特殊成员函数也是同理。