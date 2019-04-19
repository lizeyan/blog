---
title: 'Use std::weak_ptr for std::shared_ptr-like pointers than can dangle'
date: 2016-09-11 13:43:52
tags: ["c++", "c++11", "weak_ptr"]
categories:
- 读Effective Modern C++后有感
---
针对那些类似`std::shared_ptr`但是没有所有权,可能为悬挂指针的指针使用`std::weak_ptr`.

<!-- more -->

`std::weak_ptr`是一个类似`std::shared_ptr`的智能指针,但是它没有对对象的所有权.也就是说`std::weak_ptr`不影响资源的引用计数(RC).
`std::weak_ptr`不是一个独立的智能指针,事实上它只是`std::shared_ptr`的一个补充.比如说,`std::weak_ptr`只能使用`std::shared_ptr`和`std::weak_ptr`构造,而不能直接使用原生指针.
eg:
``` c++
auto spw = std::make_shared<Object> ();
std::weak_ptr wpw (spw);
spw = nullptr; // then wpw is dangle
```

`std::weak_ptrs`的`expired()`方法可以探测是否悬空.如果一个弱指针不是悬空的,然后再访问它所指向的对象.但这又一些问题,一方面是`std::weak_ptr`没有提供访问指向的资源的接口(因为本意就是不让这么做),另一方面这不是线程安全的.比如说说你在判断`expired`之后最后一个指向资源的`std::shared_ptr`析构了,那么你下面的访问就会出错.所以正确的访问`std::weak_ptr`的资源的方法是先准换为`std::shared_ptr`.
eg:
``` c++
std::shared_ptr<Object> spw1 = wpw.lock ();
```
如果wpw是悬挂的,那么`lock`返回的是空的智能指针.其实`lock`就相当于`expired()?shared_ptr<T> (): shared_ptr<T> (*this)`.
`std::shared_ptr`的构造函数可以以`std::weak_ptr`为参数,如果这个弱指针是悬空的,那么会抛出异常`std::bad_weak_ptr`

然而你可能会想,这样的一个东西有什么用处呢?接下来举三个例子来说明.

比如有这样一个函数:
``` c++
std::unique_ptr<Object> load (ObjectId id);
```
假设`load`操作是很费时的,因为可能有访问I/O设备的操作,那么我们需要一个缓存机制:
``` c++
std::shared_ptr<Object> loadQuick (ObjectId id)
{
    static std::unordered_map<ObjectId, std::weak_ptr<Object> > cache;
    auto sp = cache[id].lock ();
    if (!sp)
    {
        sp = load (id);
        cache[id] = sp;
    }
    return sp;
}
```
因为这时缓存需要保存一份指向资源的指针,因为不能再使用`std::unique_ptr`作为返回值.为什么缓存中不使用`std::shared_ptr`呢?因为我们要让用户控制资源的生命期,而不是缓存函数.


第二个例子是观察者模式(Observer Pattern).观察者模式中,主体(subject)是状态可能发生变化的对象,如果主体的状态发生变化,应当通知观察者.显然,主体应当保存观察者的指针,但是主体不应该控制观察者的生命周期.同时,主体还需要知道观察者是否已经被析构了.这时`std::weak_ptr`就是不二选择

第三个例子是循环引用:
``` c++
class A
{
    std::shared_ptr<B> ptr;
};
class B
{
    PointerToA ptr;
};
```
这时`PointerToA`有几种选择:
- 原生指针 这时B.ptr不能判断是否有效.
- `std::shared_ptr` 这时会发生循环引用.析构B之前将需要先析构A,析构A之前又需要先析构B.
- `std::weak_ptr` 上面的两个问题都得到了解决.

不过这种使用`std::weak_ptr`打破循环的做法并不常见.因为在一个设计良好的数据结构中,对象之间的所有的关系是明确的.比如在一棵树中,父节点对子节点拥有所有权,应当使用`std::unique_ptr`.这时在子节点中存储父节点的指针使用原生指针就是安全的.