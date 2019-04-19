---
title: Declare overriding functions override
date: 2016-08-11 16:31:44
tags: ["c++", "c++11", "override"]
categories:
- 读Effective Modern C++后有感
---
将所有重写的函数声明为`override`。

<!-- more -->

在面向对象程序中，重写(override)是很重要的概念。
``` c++
class Base
{
public:
	virtual void work () 
	{
		std::cout << "Base" << std::endl;
	}
}
class Derived: public Base
{
public:
	virtual void work () //override
	{
		std::cout << "Derived" << std::endl;
	}
}
std::unique_ptr<Base> ptr = std::make_unique<Derived> ();
ptr->work (); // stdout: Derived
```
重写的要求:
- 基类中的对应函数必须声明为`virtual`
- 子类和基类中的对应函数函数名必须相同。
- 子类和基类中的对应函数参数列表必须相同。
- `const`, `&`, `&&`等标记符必须相同。
- 返回值和异常标记必须兼容（可以不一样）

c++11中提供的`override`关键字就是让你在你说想要重写的函数后面标记成`override`.
eg:
``` c++
class Base
{
public:
	virtual void work () ;
}
class Derived: public Base
{
public:
	virtual void work () override;
}
```

这个语法的最大特点在于它的所有功能都是在于在编译器让编译器帮助你检查错误，而在运行时并没有特别的效果。
事情的根源在于重写的时候很容易犯错：
``` c++
class Base
{
public:
	virtual void work1 () const ;
	virtual int work2 () ; 
	virtual void work3 () &;
	void work4 () ;
	virtual void work5 (int);
}
class Derived: public Base
{
public:
	virtual void work1 () ;
	virtual void work2 () ; //error
	virtual void work3 ();
	void work4 () ;
	virtual void work5 ();
}
```
上面的函数全都重写失败，但是只有一个函数编译器会报错，其他的都是合法的。
你可能说这个情况下编译器是有警告的，不得不说有的编译器比如clang++（安利）是会提出警告，但是更为广泛使用的g++却并没有任何警告（打开-Wall）。
依赖编译器的警告来发现你的错误是很不靠谱的，override的作用就是强制让编译器检查你想要重写的函数有没有真的重写。
对于每一个复杂系统，这非常有用，因为每个人都很难了解整个系统，而只能看到一部分。你必须明确地表达你的代码的意图。`override`关键字能让你避免很多毫无意义然而非常费时的Debug工作.
当一个工程中每个该使用`override`的地方都正确使用了的时候，如果你想修改你的函数声明，那么你可以通过编译器的提示很容易看到你修改之后带来的工作量。如果没有使用`override`关键字，那么这个系统说不定就废了......

另一个关于`override`关键字的有趣之处在于他只在函数声明的结尾才会被编译器识别，在其他地方不起作用。你还是可以使用`override`作为标识符。这很明显是为了兼容不计其数的老代码（历史的包袱.....)。