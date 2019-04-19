---
title: 'Some chaos about incomplete types and std::unique_ptr'
date: 2016-09-11 22:24:58
tags: ["c++", "c++11", "std::unique_ptr", "incomplete"]
categories:
- 读Effective Modern C++后有感
---
对`std::unique_ptr`和`incomplete type`一起使用时发生的问题的讨论.
<!-- more -->
假想这样一段代码:
``` c++
#include <memory>
class Widget
{
public:
  Widget ();
  // ~Widget ();
private:
  struct Impl;
  std::unique_ptr<Impl> pImpl;
};
```
其中`Impl`保存了`Widget`的数据变量.一个示例的定义:
``` c++
struct Widget::Impl
{
  std::string name;
  std::vector<int> x;
};
```
这是一个被称为*pimpl idiom*的设计模式,具体思想就是将类的成员变量存在一个实现类中,然后在原来的类中只保存实现类的指针.因为包含`Widget.h`的源文件很多,这样做的话`Impl`有所改动将不需要包含`Widget.h`的源文件重新编译.
现在给出`Widget.cpp`的一个实现:
``` c++
#include "widget.h"
#include <string>
struct Widget::Impl
{
  std::string name;
};
Widget::Widget (): pImpl (std::make_unique<Impl> ())
{

}
```
我们没有定义析构函数,因为没有任何需要特化的,编译器自动生成即可.
但如果我们在一个函数中使用`Widget`,就会发现问题:
``` c++
#include "widget.h"
int main(int argc, char* argv[])
{
  Widget w;
  return 0;
}
```
这个工程会编译错误,具体的错误信息与编译器有关,但总的来说核心在于不能对一个`incomplete type`使用`sizeof`操作符.问题在哪呢?

关键问题就是编译器自动生成的析构函数.在大多数现代编译器里,生成的析构函数并不仅仅是调用`delete`而已.一个编译器添加的典型的操作就是使用`std::static_assert`对指针进行检查,但是这个过程是不支持`incomplete type`的.所以解决问题的关键就是保证编译器生成析构函数时`Impl`已经有了定义.
我们可以这样:
``` c++
#include <memory>
class Widget
{
public:
  Widget ();
  ~Widget ();
private:
  struct Impl;
  std::unique_ptr<Impl> pImpl;
};
//=============================
#include "widget.h"
#include <string>
struct Widget::Impl
{
  std::string name;
};
Widget::Widget (): pImpl (std::make_unique<Impl> ())
{

}
Widget::~Widget() = default;
```
这样编译器在看到`default`的时候,`Impl`就已经定义了.不过这个方法引入了新问题,那就是显式声明析构函数的类编译器就不会自动生成移动函数,因此我们需要自定义移动函数.移动函数使用默认函数的时候会遇到和析构函数一样的问题.因为编译器会在移动函数中生成这样的代码:当移动时发生异常,将析构`pImpl`然后重新分配空间.但是析构又需要他的定义,这样我们就又需要在源文件中定义移动函数.
``` c++
#include "widget.h"
#include <string>
struct Widget::Impl
{
  std::string name;
};
Widget::Widget (): pImpl (std::make_unique<Impl> ())
{

}
Widget::~Widget() = default;
Widget::Widget(Widget&&) = default;
Widget& operator= (Widget&&) = default;
```

设计模式*pimpl idiom*并不改变原始类的含义,但是现在这个类已经不可复制了
- 一方面是有`std::uniqeu`作为成员变量的类都不可自动生成拷贝函数
- 另一方面是自动生成的拷贝函数也不可能可用,因为这里的指针不能直接拷贝指针
我们需要自己实现拷贝函数
``` c++
Widget::Widget (const Widget& r): pImpl (nullptr)
{
  if (r.pImpl)
    pImpl = std::make_unique<Impl> (* r.pImpl);
}
Widget& Widget::operator= (const Widget& r)
{
  if (!r.pImpl)
    pImpl.reset ();
  else if (!pImpl)
    pImpl = std::make_unique<Imple> (* r.pImpl);
  else
    * pImpl = * r.pImpl;
}
```

最后说明一点,那就是对于`std::shared_ptr`来说,上面提到的所有麻烦的事情都不存在,第一份示例代码就可以正确运行.但是这里我们的所有关系还是更符合`std::unique_ptr`的独占关系,所以我们不推荐为了省事使用`std::shared_ptr`,这让你的代码逻辑混乱.
为什么会这样呢?因为对于`std::unique_ptr`而言,删除器(`deleter`)是智能指针对象的一部分.这可以让编译器生成更好的代码.但是对于`std::shared_ptr`而言,删除器只是存储在控制块中的一个参数.
