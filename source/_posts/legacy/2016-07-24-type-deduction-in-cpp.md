---
title: c++类型推导
date: 2016-07-24 14:50:52
tags: ["c++", "c++11", "c++14", "template", "auto", "decltype", "type deducing"]
categories:
- 读Effective Modern C++后有感
---
本文介绍在c++11及c++14中template，auto和decltype的类型推导规则。

<!-- more -->
1.  template 的类型推导。
    我们主要解决的问题是，当有一个模板函数定义如下时：
    ``` c++
    template <typename T>
    void func (ParamType param);
    ```
    若我们调用
    ``` c++
    func (expr);
    ```
    那么ParamType和T的类型如何产生。
    1. ParamType是引用(reference)和指针(pointer)
        - 如果expr本身是引用，那么就忽略这个引用
        - 如果expr本身是指针，那么就忽略这个指针
        - 如果ParamType中还有const，那么忽略expr中的const
        - expr类型的剩余部分去匹配T

        eg1:
        ``` c++
        template <typename T>
        void f (T& x);

        int x = 27;
        const int cx = x;
        const int& rx = x;
        f (x); // T: int
        f (cx); // T: const int
        f (rx); // T: const int
        ```
        eg2:
        ``` c++
        template <typename T>
        void f (T& x);

        int x = 27;
        const int cx = x;
        const int& rx = x;
        f (x); // T: int
        f (cx); // T: const int
        f (rx); // T: const int
        ```
        eg3:
        ``` c++
        template <typename T>
        void f (T* x);

        int x = 27;
        const int* px = &x;
        f (x); // T: int
        f (px); // T: const int
        ```
        eg4:
        ``` c++
        template <typename T>
        void f (T* const x);//注意这个const的位置

        int x = 27;
        const int* px = &x;
        f (x); // T: int
        f (px); // T: const int
        ```
    2. ParamType是通用引用(universal reference)
        通用引用的设计是为了处理右值引用的问题。这是唯一区分左值右值的规则。
        - 如果expr是左值，那么T将被推断为左值引用。这是模板类型推断中唯一一处可以推断出类型为引用的规则。同时尽管ParamType声明为右值引用(&&), 类型推断会将其推断为左值引用(&);
        - 如果expr是右值，那么和case1没有什么不同。

        eg1:
        ``` c++
        template <typename T>
        void f (T&& param);

        int x = 27;
        const int cx = x;
        const int& rx = x;
        f (x); // T: int&
        f (cx); // T: const int&
        f (rx); // T: const int&
        f (27); // T: int
        ```
    3. ParamType是其他一般类型
        这个时候是按值传参的。
        - 忽略expr的引用，const，volatile等修饰符

        eg1:
        ``` c++
        template <typename T>
        void f (T param);

        int x = 27;
        const int cx = x;
        const int& rx = x;
        const char* const str = "hello world";
        f (x); // T: int
        f (cx); // T: int
        f (rx); // T: int
        f (27); // T: int
        f (str); // T: const char*
        ```

    4. 如果参数是数组和函数
        - 如果参数是按值或者指针传递的，那么expr会被视为指针或者函数指针再按照前面的规则进行匹配
        - 如果参数是按引用传递，那么将保存数组的长度信息
        eg1:
        ``` c++
        template <typename T>
        void f (T x);
        void g () {}

        int arr[3];
        f (arr);// T:int*
        f (g);// T: void (*) ()
        ```
        eg2:
        ``` c++
        template <typename T>
        void f (T& x);
        void g () {}

        int arr[3];
        f (arr);// T:int[3]
        f (g);// T: void ()
        ```
        eg3:
        ``` c++
        template <typename T>
        void f (T&& x);
        void g () {}

        int arr[3];
        f (arr);// T:int (&) [3]
        f (g);// T: void (&) ()
        f ((int[]){1, 2, 3}); // T: int [3]
        ```
        可以看出，此时最大的区别就是保留了数组长度的信息。
        根据这个规则，-Effective Modern c++-中给出了一个返回任意数组长度的方法：
        ```
        template <typename T, std::size_t N>
        constexpr std::size_t arraySize (T (&)[N]) noexcept 
        {
            return N;
        }
        ```
        真神奇！！！

2. auto的类型推断
    auto的类型推断大体上和模板类型推断是一样的，把auto看成上面的T即可。
    eg1:
    ``` c++
    void g () {}
    auto x = 27; // int
    const auto cx = x; // const int
    const auto& rx = x; // const int&
    auto&& ux1 = x; // int&
    auto&& ux2 = cx; // const int&
    auto&& ux3 = 27; // int&&
    const char name[] = "Zeyan Li";
    auto arr1 = name; // const char*
    auto& arr2 = name; // const char (&) [9];
    auto f = g; // void (*) ()
    auto& f = g; // void (&) ()
    ```
    唯一的不同在于聚合构造，auto会假设聚合构造为std::initializer_list,但是模板推导不会。
    eg2:
    auto x = {1, 2, 3}; //std::initializer_list<int>;
    f ({1, 2, 3}); //couldn't deduce template parameter 'T', f is defined as above

    同时需要注意的是，当我们直接把auto作为函数的返回值或者参数的时候，含义是用模板推断来决定返回值或参数的类型而不是用auto的推断。

3. decltype是做什么的
    这是一个操作符，返回一个表达式或者变量的-真实-类型。
    eg:
    ``` c++
    template <typename T>
    class TD; // type display
    auto il = {1, 2, 3};
    TD<decltype(il)> id;// std::initializer_list<int>
    TD<decltype(27)> id2;// int
    ```
    上面的TD是用来让编译器通过编译错误的方式显示类型的技巧。

    decltype(auto)是用来解决auto推断时忽略一些修饰符的问题，这是c++14的语法。
    eg:
    ```
    int x = 27;
    const int& rx = x;
    auto cx = rx; // int
    decltype(auto) dcx = rx; // const int&
    ```

    对于任何的左值表达式，decltype都返回左值引用。
    eg:
    ``` c++
    int x = 27;
    TD<decltype(x)> id;// int
    TD<decltype((x))> id2;// int&
    ```

4. 如何判断一个变量或者表达式的类型。
    上面给出的TD是一种通过编译错误得到类型的手段
    eg:
    ``` c++
    template <typename T>
    class TD; // type display
    TD<decltype(27)> id2;
    // aggregate 'TD<int> id' has incomplete type and cannot be defined
    ```

    通过[std::type_info](http://en.cppreference.com/w/cpp/types/type_info)可以在运行时得到类型信息。
    eg:
    ``` c++
    std::string x;
    std::cout << typeid (x).name () << std::endl;
    ```
    各种编译器的输出不一样。对于大部分编译器，包括g++和clang++，输出的都是编译器内部的类型而不是可读的类型。比如上面的例子在g++5.3.0编译后的输出为NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE，WTF:)



