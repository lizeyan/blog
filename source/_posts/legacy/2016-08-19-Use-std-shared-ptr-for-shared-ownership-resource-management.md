---
title: 'Use std::shared_ptr for shared-ownership resource management'
date: 2016-08-19 21:05:26
tags: ["c++", "c++11", "shared_ptr"]
categories:
- 读Effective Modern C++后有感
---
使用`std::shared_tr`管理共享控制权的资源.

<!-- more -->

`std::shared_tr`是一种类似垃圾回收机制的智能指针,它统计有多少个指针指向了所管理的对象,如果没有指针指向资源,那么资源就会自动释放.

`std::shared_tr`使用引用计数存储指向资源的指针个数.从原生指针构造时,引用计数增加;复制时,目标指向资源的引用计数减少,源指向的资源引用计数增加;移动时,引用计数不变.

由此我们可以得到`std::shared_tr`的一些性质:
- `std::shared_tr`比原生指针尺寸大.因为我们需要空间存储资源对应的计数的位置.
- 引用计数的空间是动态分配的.因为引用计数是和被管理的资源绑定的,但是资源本身不知道引用计数的存在,所以我们需要动态分配空间管理引用计数.
- 引用计数的增减都是原子操作.显然,必须保证线程安全,因此引用计数的增减应当为原子操作.

和`std::unique_ptr`一样,`std::shared_ptr`使用`delete`作为默认的析构器,同时支持自定义的析构器.但是不同之处在于对`std::shared_ptr`而言,析构器的类型不是模板参数.这种设计更加灵活,因为指向同样类型的智能指针可以使用不同的析构器.
eg1:
``` c++
void f (std::shared_ptr<Object>& sp);
auto loggingDel = [] (Object* pw)
{
    makeLogEntry (pw);
    delete pw;
};
std::unique_ptr<Object, decltype(loggingDel)> upw (new Object, loggingDel);
std::shared_ptr<Object> spw (new Object, loggingDel);
std::shared_ptr<Object> spw2 (new Object);
f (spw);
f (spw2);
```
另一个不同在于指定析构器并不改变`std::shared_ptr`的大小,因为析构器回合引用计数一起存放在一块动态分配的空间中.
在一般的实现方法中,`std::shared_ptr`包含两个原生指针,一个指向资源本身,另一个指向资源对应的控制块(Control Block).控制块中有引用计数,弱引用计数,析构器,构造器之类的数据.

一个指针指针构造时是没有办法知道是否有其他智能指针指向资源的,那么什么时候应当创建新的控制块呢?c++11标准是这样做的:
- 当使用`std::make_shared`构造时,创建控制块
- 从原生指针构造时,创建控制块
- 从独占式指针:`std::unique_ptr`,`std::auto_ptr`构造时,创建控制块

因此,如果多次从同一个原生指针差创建`std::shared_ptr`,就会产生错误.因为会有多个控制块被创建,同一个资源就会被析构多次.
因此,使用一个原生指针构造`std::shared_ptr`是不好的工程实践,使用`std::make_shared`或者直接使用`new`都是更好的方案.

尤其值得关注的是`this`:
eg2:
``` c++
class Object
{
public:
    void process ();
    static std::vector<std::shared_ptr<Object> > processed;
};
void Object::process ()
{
    //
    processed.emplace_back (this);
}
```
如果其他地方已经定义了指向该对象的智能指针,那么就会析构多次,导致错误.
STL提供了一种写法可以部分地解决这个问题:
eg3:
``` c++
class Object: public std::enalbe_shared_from_this<Object>
{
public:
    void process ();
    static std::vector<std::shared_ptr<Object> > processed;
};
void Object::process ()
{
    processed.emplace_back (shared_from_this());
}
```
`shared_from_this`会从所有的控制块中寻找当前对象关联的控制块,然后返回一个`std::shared_ptr`,如果没有已创建的控制块,将会抛出一个异常.

使用独占性的智能指针可以创建`std::shared_ptr`,但是反过来是不可以的.`std::shared_ptr`还不支持数组.