---
title: Comparasion nullptr with NULL
date: 2016-08-09 17:04:29
tags: ["c++11", "c++", "pointer", "nullptr"]
categories:
- 读Effective Modern C++后有感
---
`nullptr`比`NULL`好在哪里?

<!-- more -->
首先要明白指针和整数类型之间是可以任意转换的.`0`是一个`int`,不是空指针.但是在任何一个需要指针的地方,`0`又可以被隐式类型转换为空指针.`NULL`因此可以是指针之外的其他类型的数据。
eg1:
``` c++
f (int);
f (void*);
f (0);
f (NULL);//大多数编译器会报错，这里无法区分NULL表示的是int还是一个指针。
```
上面的例子也告诉我们一个道理，任何时候都不要重载整数类型和指针分别作为参数的函数。尽管现在有了`nullptr`，但是`NULL`并没有被禁止。
通过之前的[blog][deduce]里面介绍的方法，可以看到在g++中`NULL`的类型.
eg2:
``` c++
#include <cstddef>
template <typename T>
class TD; // type display
template <typename T>
void f (T* x)
{
	TD <decltype(T())> td;
}
int main ()
{
	f (NULL);
}
/* errors:
test.cpp: In function 'int main()':
test.cpp:12:9: error: no matching function for call to 'f(NULL)'
  f (NULL);
         ^
test.cpp:5:6: note: candidate: template<class T> void f(T*)
 void f (T* x)
      ^
test.cpp:5:6: note:   template argument deduction/substitution failed:
test.cpp:12:9: note:   mismatched types 'T*' and 'int'
  f (NULL);
*/
```
但是`nullptr`是不会被转换成整数类型的。准确地说`nullptr`的类型是`nullptr_t`（虽然说`nullptr_t`的定义是`nullptr`的类型）
这也带来`nullptr`的另一个好处，在模板中`NULL`会被解析为`int`，而`nullptr`会被解析为`nullptr_t`.

对于eg2中的例子`nullptr`其实也是不能编译通过的，但是我们可以对`nullptr_t`做模板特化。
eg3:
``` c++
#include <cstddef>
template <typename T>
class TD; // type display
template <typename T>
void f (T* x)
{
	TD <decltype(T())> td;
}
void f (std::nullptr_t)
{
	TD <decltype(nullptr))> td;
}
int main ()
{
	f (nullptr);
}
```

[deduce]: https://lizeyan.github.io/2016/07/24/c-%E7%B1%BB%E5%9E%8B%E6%8E%A8%E5%AF%BC/ "deduce"