---
title: Let's talk about the c++ auto
date: 2016-07-24 20:45:36
tags: ["c++", "c++11", "c++14", "auto", "keyword", "modern", "effective"]
categories:
- 读Effective Modern C++后有感
---

介绍关于c++11的新关键字auto。

<!-- more -->

# the wisdom of auto

`auto`表示将类型留给编译器去推断而不是由程序员指定。使用`auto`关键字好处多多。
- 减少代码量，让代码更清晰
eg:
``` c++
std::unordered_map<std::string, std::string> map;
for (std::unordered_map<std::string, std::string>::iterator it = std::begin(map); it != std::end (map); ++it)
{
    //do something
}
for (auto it = std::begin(map); it != std::end (map); ++it)
{
    //do something
}
```
    下面的代码显然更清晰可读。
    同时如果你上面`map`的类型修改为其他，比如改为`std::map`，那么下面的代码使用`auto`关键字就可以不用更改。
    有人可能认为使用auto让人没办法通过看源代码很快知道一个变量的类型。但是我必须指出，现代化的IDE完全可以弥补这一点缺陷，IDE可以通过编译器的API或者其他什么手段分析代码结构，从而随时得到变量类型。写稍大一些的工程就不应该只使用文本编辑器。
- 定义不知道类型的变量
eg:
``` c++
template <typename It>
void travel (It b, It e)
{
    for (; b != e; ++b)
    {
        typename std::iterator_traits<It>::value_type curValue = *b;
        //do something
    }
}
```
    我相信很多人都不熟悉`typename std::iterator_traits<It>::value_type`这个用法，那么此时用`auto`去声明`curValue`无疑是更好的解决方案。
    另一个例子是针对lamda函数的。
eg:
``` c++
auto f = [] (const auto& p, const auto& q) {return p < q;};
```
    这个lambda函数的类型相当复杂（`main()::<lambda(const auto:1&, const auto:2&)>`），大部分人应该都不会去手动指定类型，`auto`就是我们最好的选择。
    上面的这个例子中因为参数的类型也是不确定的，所以连`std::function`也不能用。那么对确定参数类型的lambda函数直接使用`std::function`如何呢？就像下面这样？
``` c++
std::function<bool<(int, int)> f = [] (int a, int b) {return a < b;};
```
    当然，这样是可以通过编译的。但是我们应当认识到，`std::function`的含义是任何可以被当作函数使用的对象，它和lambda的类型并不是真的一样。
eg:
``` c++
std::function<bool(int, int) > g1 = [] (int a, int b) {return a < b;};
// type: std::function<bool(int, int)>
auto g2 = [] (int a, int b) {return a < b;};
// type: main()::<lambda(int, int)>
std::cout << sizeof (g1) << " " << sizeof (g2) << std::endl;
```
    输出结果是16 1，可以看到两种类型的内存占用差别很大。同时，显然地`std::function`的执行效率也可能会略低。

- 避免因平台和版本和知识水平导致的类型错误
    你会如何记录一个`std::vector`的size呢？
``` c++
unsigned size = v.size()
```
    这样做看起来很好，但是`std::vector`的返回值并不总是`unsigned`。按照标准，返回值实际上是`std::vector<T>::size_type`，这个值在32bit平台上是32bit的，在64bit平台上是64bit的。所以上面的代码在64bit平台上就存在bug。
    这种问题对于一个经历过很多坑的资深程序员来说应该可以避免，但是使用auto无疑更加保险。
    下面看range loop的例子
eg:
``` c++
std::unordered_map<std::string, int> map;
for (const std::pair<std::string, int>& p: map)
{
    //do something
}
```
    这段代码看起来很美，也可以正常编译运行。但是它是有问题的，你能看出来么？
    关键在于std::unordered_map的[定义](http://zh.cppreference.com/w/cpp/container/unordered_map)，他的value_type是`std::pair<const Key, T>`。因此上面的例子迭代时得到的是`std::pair<const string, int>`，为了转换为p声明的类型，编译器会增加一段拷贝复制的代码，大大降低了效率。
    使用下面的写法则可以完美掩盖自己的姿势水平23333
``` c++
for (const auto& p: map)
{
    //do something
}
```


# unexpected auto type deducing

接下来讨论auto推导出错误的、和我们的认知不同的类型的情况。在这些情况下，我们必须使用明确的类型声明。
``` c++
std::vector<bool> boolVec ()
{
    std::vector<bool> tmp(10);
    return tmp;
}
auto v = boolVec()[5];
func (v); //potential undefined behavior
```
存在undefind behavior的原因在于`std::vector<bool>`被特化为类似于`std::bitset`的的数据结构而不是通常的`std::vector`，其中每一个`bool`使用一个bit存储而不是一个byte以提高效率。但是有一个问题就是c++是没有办法返回一个bit的，因此`operator[]`返回的实际上是`std::_Bit_reference`，不像通常的`std::vector`那样返回`std::vector::value_type&`。
`std::_Bit_reference`可能不同的平台上实现不同，一种实现是存储一个指向存储bit所在word的指针，再加上指向bit的偏移(offset)。
因为`boolVec()`返回的是一个临时变量，所以它将很快被析构，此时v对应的`std::_Bit_reference`就指向了一个悬挂指针。

事实上auto在所有类似这样的代理类(proxy class)出现的情况下都不太适用。代理类指的是那些被实现为和某些实际类型有相同行为的类。比如上面的`std::_Bit_reference`，比如`std::unique_ptr` `std::shared_ptr`。尤其让人困惑的是像`std::_Bit_reference`这样隐式的代理，他们从来不会在代码中显式出现，他们被设计出来的初衷就是悄悄地完成自己的使命然后消失，我们往往会忽视他们的存在。
然而我们又舍不得放弃auto的各种好处，就像第一节提到的那样。*Effective modern c++*给出的解决方案是熟读你所使用的库的文档(就是要提高你的姿势水平)，或者阅读它的头文件。同时将存在这样的隐式类型转换的地方显式地写出来以提醒后人这里存在的问题，像这样:
``` c++
auto v = static_cast<bool> (boolVec ()[5]); //
```
虽然我不是很懂这里干嘛还写成auto，不过显式地写出来所有的隐式类型转换确实很有必要。:)




