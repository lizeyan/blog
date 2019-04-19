---
title: Prefer scoped enums to unscoped enums
date: 2016-08-10 11:05:50
tags: ["c++", "c++11", "enum"]
categories:
- 读Effective Modern C++后有感
---

新的scoped enum写法。

<!-- more -->

unscoped enum中定义的枚举变量会处于enum所在的命名空间内。
eg1:
``` c++
enum Color {white, red, black};
auto white = false; // error
```
但是scoped enum中的变量会处于这个enum class建立的命名空间中。
eg2:
``` c++
enum class Color {while, red, black};
auto white = false;// fine
auto c = white;// error
auto c1 = Color::white;// fine
```

另一个问题在于unscoped enum是支持向任何整数类型的隐式类型转换的。但是scoped enum就必须使用强制类型转换。这可能让你的代码更加安全。
eg3:
``` c++
enum Color {red, white, black};
std::vector<std::size_t> vt {red, white, black}; // fine
```
eg4:
``` c++
enum class Color {red, white, black};
std::vector<std::size_t> vt {Color::red, Color::white, Color::black};// error
```
eg4中出错的原因正在于Color中的枚举变量不能被隐式类型转换为其他任何类型。
我们必须使用显式类型转换,这确保了你知道你的代码在做什么。
eg5:
``` c++
enum class Color {red, white, black};
std::vector<std::size_t> vt {static_cast<std::size_t>(Color::red), static_cast<std::size_t>(Color::red), static_cast<std::size_t>(Color::red)};// fine
```

scoped enum的第三个优势在于可以直接使用前置声明。在c++98中，只能定义enum而不能声明。
eg6:
``` c++
enum Color; // error
enum class Color; //fine
```
使用前置类型声明有什么好处呢？在一个工程中你可能需要到处使用你的某个enum，那么在c++98中你只能把它写在一个头文件里然后每个地方都包含一次。但是一旦你修改了这个enum，你就不得不重新编译整个工程。如果使用前置声明，那么就只需要重新编译修改过的文件，然后再重新连接即可。
为什么c++98禁止声明enum呢？因为enum其实是有底层类型的，比如int，char之类的。再c++98中，enum使用哪个类型作为底层类型是由编译器确定的，编译器会自动选择占用空间最小、速度最快的底层类型，因此他必须看到你的定义之后才能分配空间。但是再c++11中，所有的scoped enum的底层类型默认均为int，如果你要使用别的你需要手动声明。
eg7:
``` c++
enum class Color; // underlying type is int
enum class Status: char; //underlying type is char
```
底层类型的声明在声明时和定义时都可以指定，但是必须一致。
eg8:
``` c++
enum class Color: int;
enum class Color:int {red, white, black};//fine
enum class Status: std::uint32_t;
enum class Status: long long {win, lose};//error
```
同时，在c++11中如果unscoped enum也显式声明了底层类型的话也是可以只声明不定义的。
eg9:
``` c++
enum Color: int;
```

以上是scoped enum的三点优点，但是他还有一个缺点：在需要类型转换的时候比较麻烦。
eg10:
``` c++11
using UserInfo = std::tuple<std::string, std::string, std::size_t>;
enum class UserInfoFields {name, email, age};
UserInfo userInfo;
auto age = std::get<static_cast<int>(UserInfoFields::age)>(userInfo);
```
对比使用unscoped enum：
``` c++11
using UserInfo = std::tuple<std::string, std::string, std::size_t>;
enum UserInfoFields {Name, Email, Age};
UserInfo userInfo;
auto age = std::get<Age>(userInfo);
```
明显更加简洁明了。
在c++11和c++14的标准库中提供了给出enum的底层类型的方法，因此eg9可以稍微简化一点。
eg11:
``` c++11
template <typename T>
using UT = typename std::underlying_type<T>::type;
template <typename T>
constexpr UT<T> TU (T t)
{
	return static_cast<UT<T> > (t);
}
int main ()
{
	using UserInfo = std::tuple<std::string, std::string, std::size_t>;
	enum class UserInfoFields {name, email, age};
	UserInfo userInfo;
	auto age = std::get<TU(UserInfoFields::age) >(userInfo);
}
```
尽管还是比unscoped enum麻烦一点，但是为了更好的安全性多打一点代码还是值得的（原作者观点）。