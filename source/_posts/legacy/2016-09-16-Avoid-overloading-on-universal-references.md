---
title: Avoid overloading on universal references
date: 2016-09-16 20:45:48
tags: ["c++11", "universal reference", "overload"]
categories:
- 读Effective Modern C++后有感
---
避免重载参数是通用引用的函数

<!-- more -->

<i style="color:red">
注:后面的代码中有很多type_trait我随意地添加了`_t`或者`_v`的后缀,后来我发现有些即便是C++14都没有进入标准,需要等到C++17.对这种代码,你可以参照下面的例子做个简单的映射:`std::is_same_v<T1, T2>` == `std::is_same<T1, T2>::value`, `std::decay_t<T>` == `std::decat<T>::type`. 我懒得再去查这些简化都是什么时候加入标准的了.其中的原理请参阅[Prefer alias declarations to typedefs](https://lizeyan.github.io/2016/08/09/Prefer-alias-declarations-to-typedefs/).
</i>



想象你需要这么一段代码:接受一个参数,记录当前时间,然后将参数添加到一个全局的数据结构中.我们可以简单地写成这样:
``` c++
std::set<std::string> names;
void logAdd (const std::string& name)
{
    auto now = std::chrono::system_clock::now ();
    log (now, "logAdd");
    names.emplace (name);
}
```
这段代码是合理的,但是效率不够高.我们考虑下面的调用语句
``` c++
std::string petName ("Cat");
logAdd (petName);
logAdd (std::string ("Dog"));
logAdd ("Turtle");
```
在第一次调用中,我们不得不进行一次复制.因为传入`logAdd`是一个左值,我们将其加入`names`时必然需要复制.
在第二次调用中,传入`logAdd`是一个右值,但是`name`又是一个左值.此时将`name`加入`names`仍然发生复制,但是这个复制是不必要的.
在第三次调用中,不仅发生了复制,而且还有一个临时的`std::string`对象的构造和析构过程.而这些都是不必要的,我们可以直接将这个常量字符串转发给`std::set::emplace`.

因此我们将代码改成下面这样:
``` c++
template <class T>
void logAdd (T&& name)
{
    auto now = std::chrono::system_clock::now ();
    log (now, "logAdd");
    names.emplace (std::forward<T> (name));
}
```
这段代码将效率提高到了极限.不过我们并不仅仅到此为止.我们再考虑无法直接访问`name`的情况.
``` c++
std::string idx2name (int idx);
void logAdd (int idx)
{
    auto now = std::chrono::system_clock::now ();
    log (now, "logAdd");
    names.emplace (idx2name (idx));
}
```
这个函数和之前的同时存在的.此时我们通过下面的代码调用它会发生什么呢?
``` c++
logAdd (22);
```
`22`的类型会被解析成`short`.根据重载规则,编译器会优先选择类型最匹配的函数.一个模板会比`int`更靠近`short`.因此`22`会被当成传给`name`而不是`idx`.这时候就发生了错误,因为`std::set::emplace`不能接受`short`,同时这也和我们的本意不符.

像通用引用这种写法是很贪婪的,它和几乎所有类型都能完美匹配.这就是为什么我们不希望在使用通用引用的同时重载,因为这真的很容易出错.

我们再看一个例子:
``` c++
class Person
{
public:
    template <class T>
    explict Person (T&& n): name (std::forward (n)) {}
    explict Person (idx) : name (idx2name (idx)) {}
private:
    std::string name;
}
```
这个例子依然会出错.不过它的情况会更加严重.我们回忆一下,之前提到过[编译器会生成一些特殊成员函数](https://lizeyan.github.io/2016/08/16/The-rules-of-generating-special-member-functions/).在这里,尽管有一个模板构造函数,编译器仍会自动生成移动构造函数和拷贝构造函数.
上面的代码其实等效于:
``` c++
class Person
{
public:
    template <class T>
    explict Person (T&& n): name (std::forward (n)) {}
    explict Person (idx) : name (idx2name (idx)) {}
    Person (const Person&) = default;
    Person (Person&&) = default;
private:
    std::string name;
}
```
我们看看下面的调用会发生什么:
``` c++
Person p ("Nancy");
auto cloneOfP (p);
```
这里第一行没问题.第二行我们是想调用拷贝构造函数,但实际上编译器会选择完美转发构造函数.因为`std::string`不能从`Person`初始化,因此会编译错误.
为什么呢?我们传入的是一个非`const`的`Person`左值,而调用拷贝构造函数需要一个`const`值.因此此时特化模板才是最接近`p`的类型的函数.
如果我们这样写就可以调用到拷贝构造函数了:
``` c++
const Person p ("Nancy");
auto cloneOfP (p);
```

当有继承的时候,这件事就更加复杂了:
``` c++
class SpecialPerson: public Person
{
public:
    explicit SpecialPerson (const SpecialPerson& rhs): Person (rhs) {}
    explicit SpecialPerson (SpecialPerson&& rhs): Person (std::move(rhs)) {}
}
```
上面的两个函数中,被调用其实都是`Person`的完美转发构造函数,因为`rhs`都是`SpecialPerson`类型.

相信看到这里,你应该可以理解为什么不应该重载完美转发函数了吧.如果你确实需要在完美转发的同时特化一些类型的处理应该怎么办呢?

- 不使用重载

    在这种情况,你可以不使用重载而是使用不同名字的函数.不过,在上面的第二个例子中,这样做就不可以了,因为构造函数的函数名是语法规定好的.而且,谁愿意抛弃重载呢?

- 使用`const T&`

    回归C++98的传值方式,不再使用通用引用.虽然之前我们已经介绍过了这种方式比起通用引用性能低,但是,有些时候,在性能和开发复杂度之间做一点取舍也是应该的.

- 按值传递参数

    这个时候你需要明白参数必然会发生一次拷贝.不过我们之后会看到(不是这一篇文章),这种方式的性能也是可取的.
    ``` c++
    class Person
    {
    public:
        explict Person (std::string n) : name (std::move (n)) {}
        explict Person (int idx): name (idx2name (idx)) {}
    private:
        std::string name;
    }
    ```
    这时所有的整型类型的参数都会使用`int`重载.值得注意的是`NULL`也是会使用这个重载的(参阅[Comparasion nullptr with NULL](https://lizeyan.github.io/2016/08/09/Comparasion-nullptr-with-NULL/)).

- 使用标签分发(tag dispatch)

   不论是传递左值引用,还是传值,都不支持完美转发.有的时候我们需要的就是完美转发,而这时你也不想抛弃重载,那该怎么办呢?
   其实也不复杂.通用引用的问题在于几乎能够完美匹配所有类型,那么我们就给需要完美转发的函数增加一个不是通用引用的参数.我们还使用上面的例子.这里,真正完成完美转发工作的函数我们将其命名为`logAddImpl`,而`logAdd`依然是只接受通用引用.
   ``` c++
   std::set<std::string> names;
   template <class T>
   void logAdd (T&& name)
   {
       logAddImpl (std::forward<T> (name), std::is_integral<T> ());
   } 
   ```
   这个实现基本没问题.只是,你是否记得,在[c++类型推导](https://lizeyan.github.io/2016/07/24/c-%E7%B1%BB%E5%9E%8B%E6%8E%A8%E5%AF%BC/)中,我们曾经学习过,这里如果传入了一个左值引用,`T`会被推导为左值引用.也就是说,传入一个`int&`的时候,`T`也是`int&`,这时`std::is_integral<T>()`就是`false`了.
   解决这个问题我们需要`std::remove_reference`:
   ``` c++
   std::set<std::string> names;
   template <class T>
   void logAdd (T&& name)
   {
       logAddImpl (std::forward<T> (name), std::is_integral<std::remove_reference_t<T> > ());
   } 
   ```
   我们接下来看看`logAddImpl`的实现.我们需要注意的是`std::is_integral`是`constexpr`函数(参阅[Use constexpr whenever possible](https://lizeyan.github.io/2016/08/12/Use-constexpr-whenever-possible/)),我们必须充分利用这一点:
   ``` c++
   template <class T>
   void logAddImpl (T&& name, std::false_type)
   {
       auto now = std::chrono::system_clock::now ();
       log (now, "logAdd");
       names.emplace (std::forward<T> (name));
   }
   void logAddImpl (int idx, std::true_type)
   {
       logAdd (idx2name (idx));
   }
   ```
   我们需要知道,`true`和`false`都是运行时的值(`value`),而这里我们需要一个类型(`type`)来区分两个函数.后一个标签参数不需要名字,因为它们完全没有在代码中用到,只是让编译器去区分选择那个函数而已.我们甚至希望编译器在生成的目标代码中优化掉这个参数,减少掉运行时传递参数的开销.这种技巧是C++模板元编程的常见技巧,在STL,boost等库中你可以看到很多这种代码.
   

- 受限模板

    标签分发的一个关键点在于使用一个接受通用引用,不重载的接口函数.然后从接口函数向其他实现类进行分发.大多数时候创建一个接口函数是很简单的,但是前面介绍的第二个例子是个例外.当你试图对构造函数使用标签分发的时候,你会发现即便你只显式写了一个构造函数,有的调用还是会被编译器生成的构造函数处理而不是被分发.
    事实上,关键的问题不是编译器生成的特殊函数会绕过标签分发.关键之处在于他们是有时绕过分发,有时又不绕过.比如,只有当你试图拷贝一个非`const`的左值的时候才会调用通用引用构造函数.拷贝一个`const`的左值还是会调用拷贝构造函数的.
    像这样的情况,通用引用几乎匹配所有的情况,但是又不能真的匹配所有的情况来形成一个统一的接口函数,标签分发是不适用的.
    这里,你需要的是`std::enable_if`.一般情况下,一个模板总是被`enable`的,现在,我们希望模板在某些情况下被禁止特化.
    ``` c++
    class Person
    {
    public:
        template <class T, typename = typename std::enable_if<condition>::type>
        explicit Person (T&&);
    };
    ```
    ``` c++
    class Person
    {
    public:
        template <class T, typename = std::enable_if_t<condition>>
        explicit Person (T&&);
    };
    ```
    这里我只是简单地写出了使用`std::enable_if`的格式,其他未列出的部分和之前的例子相同.后面的是C++14的写法.我们接下来主要关注`condition`部分的语句.
    这里,我们想要让`T`不是`Person`的时候调用通用引用构造函数.也就是,
    ``` c++
    !std::is_same<Person, T>::value
    ```
    但是这有问题.正如之前提到过的,一个左值引用传给通用引用,`T`会被推导成左值引用.在这里,我们希望忽略:
    - 引用. 无论传入的是`Person`, `Person&`还是`Person&&`,我们都希望把他交给别的构造函数去处理.
    - `const`和`volatile`. 无论一个`Person`用什么修饰,通用引用构造函数都不接受.

    因此我们需要`std::remove_cv_t<std::remove_reference_t<T> >`.或者`std::decay<T>`.不过`std::decay`有点副作用,就是它会把数组和函数转化为指针.不过在这里没什么影响,我们可以使用.
    总的来说,完整的声明要写成这样:
    ``` c++
    template <typename T, typename = std::enable_if_t<!std::is_same_v<Person, std::decay_t<T> > >
    explicit Person (T&& n);
    ```
    把这种方式放在最后是有原因的.如果你能够用前面的方式解决问题,那么你就用前面的方式.不过如果你习惯了这种美丽的写法,倒也没有那么糟糕.
    成功了,是么?不是.
    之前我们还介绍了关于继承时发生的错误:
    ``` c++
    class SpecialPerson: public Person
    {
    public:
        explicit SpecialPerson (const SpecialPerson& rhs): Person (rhs) {}
        explicit SpecialPerson (SpecialPerson&& rhs): Person (std::move(rhs)) {}
    }
    ```
    在`SpecialPerson`调用`Person`的构造函数的时候,我们本意明显是要拷贝和移动的.但是要知道,现在我们传递的参数是`SpecialPerson`,那么这个调用会绑定到通用引用构造函数去!

    因此我们需要使用`std::is_base_of`来判断参数是不是`Person`的子类.
    ``` c++
    std::is_base_of_v<T1, T2>
    ```
    如果`T2`是`T1`的子类,或者`T1`和`T2`相同且不是基本类型,那么会返回`true`.
    所以我们需要进一步把代码改进成这样:
    ``` c++
    template <typename T, typename = std::enable_if_t<!std::is_base_of_v<Person, std::decay_t<T> > >
    explicit Person (T&& n);
    ```

    现在,我们完美地解决了通用引用构造函数和其他构造函数冲突的问题.不过还记得么,我们的本意还想要区分参数是不是`integral`类型然后做转发的.现在,我们还需要在`condition`中加上判断是不是`integral`的语句:
    ``` c++
    class Person
    {
    public:
        template <typename T, typename = std::enable_if_t<!std::is_base_of_v<Person, std::decay_t<T> > && !std::is_integral_v<std::remove_reference_t<T> > > >
        explicit Person (T&& n): name (std::forward<T> (n)) {}
        explicit Person (int idx): name (idx2name (idx)) {}
    private:
        std::string name;
    }
    ```
    这个办法可以完美地解决通用引用和重载的矛盾,而且效率很高.真是美丽的代码.


- 取舍

    前三种方法:抛弃重载,使用`const T&`, 按值传递为每个函数指定了参数类型.而后两种方法:标签分发和受限模板都依然使用了完美转发.
    使用通用引用更加高校的,因为它避免了创建临时对象.但是通用引用也有其缺点,首先就是有的类型不能被完美转发.这个问题我们之后详细讨论.
    另一个问题就是使用完美转发可能会生成难以理解的编译错误.比如下面的调用:
    ``` c++
    Person (u"Cat");
    ```
    `u`前缀的作用是表明使用宽字符.但是,`std::string`和`int`都不能接受宽字符串.所以这个调用会发生编译错误.问题就出在这个编译错误上,很多编译器都会生成大段大段难以理解的错误信息.比如我使用`clang++-3.8`,生成了70行.如果在一个复杂的工程中,你的参数可能经过几次转发,那么错误信息简直要多到上天了...(原书观点,我觉得现在的编译器做得已经越来越好了,尤其是clang)
    一个弥补的办法是使用`std::static_assert`:
    ``` c++
    ``` c++
    class Person
    {
    public:
        template <typename T, typename = std::enable_if_t<!std::is_base_of_v<Person, std::decay_t<T> > && !std::is_integral_v<std::remove_reference_t<T> > > >
        explicit Person (T&& n): name (std::forward<T> (n))
        {
            std::static_assert (std::is_constructible_v<std::string, T>, "Parameter n can't be used to construct a std::string");
        }
        explicit Person (int idx): name (idx2name (idx)) {}
    private:
        std::string name;
    }
    ```
    如此,你可以在一大段错误信息中较容易找见一点有用的东西.

