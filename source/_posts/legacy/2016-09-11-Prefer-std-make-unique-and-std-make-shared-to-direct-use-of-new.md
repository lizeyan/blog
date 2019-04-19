---
title: 'Prefer std::make_unique and std::make_shared to direct use of new'
date: 2016-09-11 15:06:24
tags: ["c++", "c++11", "unique_ptr", "shared_ptr"]
categories:
- 读Effective Modern C++后有感
---
使用`std::make_unique`和`std::make_shared`而不是原生指针来构造智能指针.

<!-- more -->

`std::make_shared`是C++11提供的创建`std::shared_ptr`的函数.遗憾的是`std::make_unique`属于C++14.不过你可以很容易写一个`make_unique`的简单实现:
``` c++
template <typename T, typename... Ts>
std::unique_ptr<T> make_unique (Ts&&... params)
{
    return std::unique_ptr<T> (new T(std::forward<Ts>(params)...));
}
```
`make_unique`相对简单,只是完美转发参数列表而已.上面的版本不支持数组和自定义删除器,不过无伤大雅.

除了上面提到的两个构造器,STL还有一个`std::allocate_shared`,他的功能和`std::make_shared`相同,只是可以自定义内存分配器.

为什么说要使用他们创建智能指针呢?

- 避免重复的类型说明

    eg:
    ``` c++
    auto sp1 = std::make_shared<Object> ();
    auto sp2 = std::shared_ptr<Object> (new Object ());
    ```
    可以看到不使用`make`函数的版本类型名出现了两次.倒不是说多打一些字的问题,而是前后的类型本来就必然是相同的,出现两次很没有必要,不符合软件设计的哲学.同时对将来可能的修改也不利.
- 避免可能的内存泄露

    智能指针不就是为了防止内存泄露么?使用智能指针为什么会造成内存泄露?问题关键就在于使用`new`新建智能指针的话,在堆上分配内存和建立智能指针实际上是先后的两部操作.
    eg:
    ``` c++
    process (std::shared_ptr<Object> (new Object()), compute ());
    ```
    这句函数调用有三个操作:
    - `new Object`
    - 创建智能指针
    - compute 

    但是三者的顺序是未定义的.假设首先`new Object`, 然后执行`compute`.但是`compute`发生了异常,此时之前创建的对象就没人负责回收了.
    但是使用`make`函数就不会发生问题
    ``` c++
    process (std::make_shared<Object> (), compute ());
    ```
    即使发生异常,已创建的智能指针也可以自动回收,不会发生内存泄露.

- 提高时空效率
    这一条只针对`std::shared_ptr`.
    我们来比较下面两行代码:
    ```
    auto p1 = std::shared_ptr<Object> (new Object ());
    auto p2 = std::make_shared<Object> ();
    ```
    第一行执行了两次内存分配,第一次是分配`Object`的空间,第二次是在`std::shared_ptr`的构造函数中分配控制块的空间.但是使用`make`函数的话,资源和控制块的空间是一起分配的.这样消耗时间更少,生成的代码也更小.

然而`make`函数有一些局限性:
- 不支持自定义的删除器
    自定义`deleter`本来是智能指针的一大功能,但是使用`make`函数的话,暂时没办法制定删除器.
- 不支持使用通用构造{}
    下面的代码会生成什么呢?
    ``` c++
    auto p = std::make_unique<std::vector<int> > (10, 20);
    ```
    是大小为10,每个初始化为20的`vector`,还是值分别为10,20的`vector`?好消息是这个结果是确定的,`make`函数只是用()构造器.因为事实上{}对应的初始化列表无法做到完美转发.如果你一定要使用初始化列表构造,可以使用`auto`帮忙:
    ``` c++
    auto il = {10, 20};
    auto p = std::make_shared<std::vector<int> > (il);
    ```

对于`std::unique_ptr`来说,就是这样了.但是`std::shared_ptr`还有其他问题,这些都是一些边界情况,但是我们还是需要有所了解:
- 一些类可能会有自定义的`new`和`delete`操作符.有的时候这些操作符可能只能处理分配内存大小为对应类的大小的情况,但是对于`std::allocate_shared`而言,我们需要的内存分配器必须能够处理一次性分配对象加控制块大小的情况.所以说,如果使用某些十分特殊的`new`和`delete`操作符或者功能相同的函数,不应该使用`make`函数.
- 另一个就是内存释放的问题.对于直接使用原生创建分配的`std::shared_ptr`,对象占用的内存和控制块的内存不在一起.当所有的`std::shared_ptr`都被释放时,存储对象的内存就会被释放,但是控制块的内存还会被保留.这是为了让`std::weak_ptr`查找是否悬空.

    以前的文章提到过,在控制块(Control Block)中,保存了引用计数(Reference Count),弱引用计数(Weak Count), 分配器,删除器等信息.每个`std::weak_ptr`判断是否悬空时,是在控制块中查找引用计数来判断的(为0则悬空).所以只要还有弱指针存在(弱引用计数不为0),控制块就不能释放.
    使用`make`函数创建的智能指针对象和控制块是一次分配的,因此只要引用计数或者弱引用计数不为零,这个大的内存块就一直不释放.
    
    那么如果现在`std::shared_ptr`管理的是一个很大很大的对象,同时所有的`std::shared_ptr`和`std::weak_ptr`全部释放的时间相差较大,那么这个内存释放时间的差异就可能很关键.

本文前面说过不使用`make`函数导致的无法处理异常造成内存泄露的问题,解决这个问题的关键在于尽量让`new`和智能指针的构造放在一起,同时让他们中间不要插入其他操作.
eg:
``` c++
auto p = std::shared_ptr<Object> (new Object ());
process (p, compute ());
```
这样,即使发生异常,也不会发生内存泄露.
但是此时我们传递了一个左值进函数`process`,那么会导致`std::shared_ptr`的引用计数增加.如果这个复制不是必要的,那么使用`move`更好,因为`move`一个`std::shared_ptr`完全不去修改控制块,效率更高.
``` c++
auto p = std::shared_ptr<Object> (new Object());
process (std::move(p), compute ());
```