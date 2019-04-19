---
title: Declare functions noexcept if it won't emit exceptions
date: 2016-08-12 19:45:19
tags: ["c++", "c++11", "noexcept"]
categories:
- 读Effective Modern C++后有感
---

安利关键字`noexcept`

<!-- more -->
先说一说c++里的throw specifier。
c++03里有关于函数异常标识符`throw`，它的作用在于表示一个函数抛是否抛出异常异常以及抛出异常的类型。但是这个特性很快就差不多成为了c++的一个黑点，原因在于他不像Java的异常处理机制那样是强制的。
eg1:
``` c++
int f () throw (int, double)
{
	throw std::exception ();
}
```
这种代码很明显有问题，但是编译器不会报错也不会提出警告。c++对此的处理方式是在运行时发现这种情况调用std::unexcepted()，如果你没有设置过std::unexcepted()的目标函数(通过std::set_unexcepted)，那么默认调用的是std::terminate。在很多环境下（比如windows+mingw），调用std::terminate之后程序会正常退出，你没有办法直接查看栈来马上定位抛出异常的位置。尽管在有的环境比如linux+gcc5.x下可以，但这不是c++标准规定的。
同时，c++对老代码（都是泪...）的兼容和模板让throw specifier非常难确定。所有函数如果不使用throw specifier，那么就相当于可以抛出任何类型的异常。如果你的代码使用了第三方库甚至STL库，C语言的库，那么你就很难确认这些调用会产生什么。模板也是同理。结合上面所说，使用throw specifier会让你的程序很容易被终止，而且还没有办法定位终止的位置。
eg2: from [Should I use an exception specifier in C++? - StackOverflow](http://stackoverflow.com/a/88905)
``` c++
template<class T>
void f( T k )
{
     T x( k );
     x.x();
}
//=============================
int lib_f();
void g() throw( k_too_small_exception )
{ 
   int k = lib_f();
   if( k < 0 ) throw k_too_small_exception();
}
```
上面例子中的`f`和`g`两个函数,你根本就不知道throw specifier应该写什么,写了就是坑。


然后，在c++11中引入了新的关键字`noexcept`，它只表明这个函数是否会抛出异常，而不要求明确异常的类型。
这个关键字仍然有着上面所说throw specifier的全部缺点，但是为什么又说可是试着用用呢？
- 首先上面提到的缺点比较容易克服。
	一方面时是否抛出异常这个问题比起抛出什么异常来说更容易回答。
	另一方面，`noexcept`不仅是一个specifier，还是一个操作符，他可以得到一个函数是否是noexcept的（返回bool）。上面的eg2就可以做一些修改。
	eg3:
	``` c++
	template<class T>
	void f( T k ) noexcept (noexcept (T (k)) && noexcept(T().x()))
	{
	     T x( k );
	     x.x();
	}
	//=============================
	int lib_f();
	void g() noexcept (false)
	{ 
	   int k = lib_f();
	   if( k < 0 ) throw k_too_small_exception();
	}
	```
- 其次，就是`noexcept`确实能够带来性能上的提升,比较实惠。
	一方面是使用`noexcept`的地方，编译器不需要让当前scope中的局部变量保持*unwindable*状态，因此可以优化出更好的代码。（更加细节的东西暂时忽略一下:D，反正就是性能有提升......）
	另一方面，有`noexcept`可以更放心地使用move。
	eg4:
	``` c++
	class Object
	{
	public:
		Object () {}
		Object (const Object&) {std::cout << "copy" << std::endl;}
		Object (const Object&&) {std::cout << "move" << std::endl;}
	};
	class Object2
	{
	public:
		Object2 () {}
		Object2 (const Object2&) {std::cout << "copy" << std::endl;}
		Object2 (const Object2&&) noexcept {std::cout << "move" << std::endl;}
	};
	int main ()
	{
		std::vector<Object> v;
		for (int i = 0; i < 2; ++i)
			v.emplace_back ();
		std::vector<Object2> v2;
		for (int i = 0; i < 2; ++i)
			v2.emplace_back ();
	}
	/*
	* stdout: copy move
	*/
	```
	可以看到，如果你的移动构造函数是`noexcept`的，那么STL中就会自动`move`而不是`copy`。否则就会保守地使用`copy`。显而易见`move`会大大提高效率。
	那么为什么STL要设计成这样呢？
	我们考虑一个`vector`在插入新元素的情况。我们都知道，如果向量在插入元素时空间不够，应该另行申请一个更大的新空间，然后把原来的数据挪过去。使用`copy`的好处是如果挪了一半之后有一个元素失败了，抛出了个异常，那么这个向量原来的数据是不受影响的。而如果这时使用`move`，那么移动一个元素失败会摧毁整个`vector`，这是不能接受的。所以STL只有在确认移动构造函数是`noexcept`的情况下才会放心地调用它。
	事实上我们自己写的库也要考虑这一点，不能盲目自信地`move`。

总之，因为`noexcept`的缺陷相对不是很大，反而能带来明显的性能提升，所以我们应该在每一个*确认可以使用*的地方使用`noexcept`。
