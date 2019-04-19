---
title: 'Overview about rvalue references, move semantics and perfect forward'
date: 2016-09-12 23:23:28
tags: ["c++11", "rvalue references", "perfect forward", "move"]
categories:
- 读Effective Modern C++后有感
---
概述关于右值引用(rvalue reference), 移动语义(move semantics), 完美转发(perfect forward)的内容.
<!-- more -->
1. 引言
  第一次了解移动和完美转发的时候,你会发现他们是非常的直接而且必要的:
  - 移动

    让编译器可以把费事的拷贝操作变成开销很小的移动操作.如果你有一个对象,需要移动到另一个对象,但是类中的数据都是不变的且源对象将不会再使用,那么为什么不直接让目标使用源的子数据的内存而要拷贝一份呢?移动语义就是提供了这种操作的语法.就像拷贝构造函数和拷贝赋值操作符让你能够拷贝对象一样,移动构造函数和移动赋值操作符让你能够移动一个对象.利用移动机制你还可以创造只能移动不能拷贝的类,比如`std::unique_ptr`.
  - 完美转发

    允许你在函数模板中,接受不确定的参数,然后将它们转发给其他函数.完美转发保证在转发的过程中传递的参数的类型和传入时候是完全相同的.

  - 右值引用

    右值引用将上面两个看起来很不同的东西联系在一起.其实右值引用就是实现移动和完美转发的底层机制.

  但是,如果你有更深入的了解,你就会发现你对他们的第一印象只是真正世界的冰山一角.他们的真实面目和表面看起来的有一些细微但关键的不同.比如说,`std::move`永远不会移动任何东西;完美转发并不能保证总是完美的;移动操作并不总是比拷贝开销更小;即使比拷贝开销小,也不总是像你想象的开销那么小;在可以使用移动的场合,并不总是要移动;然后,`type&&`代表的并不总是右值引用.

  当你有了更深入的了解之后,你才能真正理解C++11的这一方面的新语法的意义所在.你将会理解所有的不符合第一直觉的现象的根源.这些语法将重新变得简洁而自然

  介绍之前有必要强调一点:
  ``` c++
  void f (Object&& w);
  ```
  在这个函数中,`w`永远都是一个左值,只是说它的类型是到`Object`的一个右值引用而已.如果你不理解这一点,请学习一下什么是左值/右值.

2.  理解`std::forward`和`std::move`
  在了解`std::move`和`std::forward`做什么之前,有必要强调以下他们不做什么:
    - `std::move`从不移动任何东西
    - `std::forward`从不转发任何东西
    事实上,在运行时,这两个函数并不发生任何作用.他们不会生成哪怕一点运行时代码.

    `std::move`和`std::forward`仅仅是执行类型转换的函数而已.`std::move`无条件地将参数转换为右值引用,而`std::forward`仅当满足一定条件的时候将参数转换为右值引用.
    我们来看一下一段`std::move`在C++11中的实现,以进一步了解:
    ``` c++
    template <typename T>
    typename remove_reference<T>::type&& move (T&& param)
    {
      using ReturnType = typename remove_reference<T>::type&&;
      return static_cast<ReturnType> (param);
    }
    ```
    可以看到,核心内容仅仅是一个将参数转换为右值引用的类型转换.返回值类型中的`&&`是为了说明要返回一个右值引用.但是为什么不写`T&&`呢?因为根据某些规则(以后再学习),当`T`是一个左值引用的时候,`T&&`代表的还是左值引用.因此我们需要先借用`remove_reference`,使得`&&`总是施加到一个非引用对象上.
    使用C++14,我们可以让`std::move`的代码更简洁:
    ``` c++
    template <typename T>
    decltype(auto) move (T&& param)
    {
      using ReturnType = remove_reference_t<T>&&;
      return static_cast<ReturnType> (param);
    }
    ```
    因为`std::move`仅仅只是一个转换到右值引用的转换器,所以也有人建议将它更名为`rvalue_cast`之类更准确的名字.不过最终标准就是这样了.当然了,右值引用是可以移动的,所以对一个对象使用`std::move`就是在告诉编译器这个对象可以移动.因此这个名字也有其准确性:就是要让这个对象移动.

    不过事实上,右值引用并不总是可以移动.比如下面的例子:
    ``` c++
    class Annotation
    {
    public:
      explicit Annotation (const std::string text)
      : value (std::move(text))     { }
    private:
      std::string value;
    };
    ```
    这段代码可以正常编译运行,运行结果也会正确,但是它并不会按照想象中的方式运行.`text`实际上会被拷贝到`value`而不是移动.这主要是因为`text`是`const`的,在经过`std::move`,`const`也依然会保留.
    当编译器选择`value`使用那个构造函数的时候,有两个选择:
    - `string (string&& rhs)`
    - `string (const string& rhs)`
    我们可以看到移动构造函数只接受非`const`的参数,所以`std::move(text)`不能作为它的参数.但是一个右值引用能够转换为左值引用,所以这里会调用拷贝构造函数.一般来说,移动一个对象可能会破坏源对象,所以我们不能移动一个常量.
    这告诉我们一个道理,不要把你想要移动的对象声明为`const`.如果你这样做,你的移动操作将变为拷贝.同时这也提醒我们,`std::move`真的不移动任何东西,他只是让一个对象可以被移动而已.

    `std::forward`和`std::move`很像很像,只不过它是有条件的类型转换而已.我们可以看一段`std::forward`典型应用场景:
    ``` c++
    template <typename T>
    void logAndProcess (T&& param)
    {
      auto now = std::chrono::system_clock::now ();
      makeLogEntry ("Calling process", now);
      process (std::forward<T> (param));
    }
    Widget w;
    logAndProcess (w);
    logAndProcess (std::move (w));
    ```
    如果`param`是通过一个左值初始化的,那么`std::forward`就什么都不做;如果是通过右值初始化的,那么就将`param`转换为右值引用.
    你可能会问`std::forward`怎么会知道`param`这样一个左值是通过左值还是右值初始化的.请注意`std::forward`还需要传入模板参数,它就是通过这个模板参数确定的(参见[c++类型推导](https://lizeyan.github.io/2016/07/24/c-%E7%B1%BB%E5%9E%8B%E6%8E%A8%E5%AF%BC/)).这也是`std::forward`和`std::move`的很大一个不同.

    有人会说既然如此,那么`std::move`完全可以用`std::forward`代替,比如下面两段代码是等价的:
    ``` c++
    std::vector<int> x (10000, 1000);
    auto x1 = std::move (x);
    ```
    ``` c++
    std::vector<int> x (10000, 1000);
    auto x1 = std::forward<std::vector<int>> (x);
    ```
    `std::move`的好处在于只需要一个参数,同时可以是代码的意义更明确.

3.  区分通用引用和右值引用
  当我们想声明类型`T`的一个右值引用的时候,我们会写`T&&`.那么你可能会想`T&&`就都是代表右值引用的意思.不过其实没有这么简单:
  ``` c++
  void f (Wdiget&& param) // rvalue reference
  Widget&& var1 = Widget (); // rvalue reference
  auto&& var2 = var1; // not rvalue reference
  template<typename T>
  void f (std::vector<T>&& param); // rvalue reference
  template <typename T>
  void f (T&& param);// not rvalue reference
  ```
  实际上,`T&&`有两个含义.一种就是右值引用,只能绑定到一个右值上,绑定的对象被认为是可以移动的.而另一种含义是通用引用.通用引用可以绑定左值或者右值.他还可以绑定到`const`或者非`const`, `volatile`或者非`volatile`的对象.通用引用可以绑定到任何对象.
  通用引用在两种情况下出现,一种就是函数模板:
  ``` c++
  template <typename T>
  void f (T&& param);```
  而第二种就是使用`auto`的声明:
  ``` c++
  auto&& var2 = var1;
  ```
  这两种情况的共同点就是存在类型推导.在不存在类型推导的地方看到`&&`,就可以确定它一定是右值引用.
  因为通用引用也是引用,所以他必须被初始化.用来初始化它的值决定了通用引用将表现为左值引用还是右值引用.初始化值为右值,通用引用就相当于右值引用.初始化值为左值,通用引用就相当于左值引用.
  对于上面例子中的函数模板,初始化的值就是传入函数的参数:
  ``` c++
  Widget w;
  f (w);
  f (std::move (w));
  ```
  类型推导是通用引用出现的必要条件,但是不是充分条件.通用引用必须简单地表达为`T&&`的形式.`T`是被推导的类型.我们再看一下下面的例子:
  ``` c++
  template <typename T>
  void f (std::vector<T>&& param);
  ```
  根据上面的规则,这里`param`就是一个右值引用.因为被推导出的是`T`而不是`std::vector<T>`.
  而且即便是`const`这样的修饰符也不可以:
  ``` c++
  template <typename T>
  void f (const T&& param); //param is rvalue reference
  ```
  那么是不是说你看见每一个模板中的`T&&`就可以认为它是一个右值引用了呢?不是的.因为不是每一个`T&&`中的`T`都需要推导.
  ``` c++
  template <class T>
  class vector
  {
  public:
    void push_back (T&& x);// x is rvalue reference
  };
  ```
  为什么`x`不是通用引用?因为在这里`push_back`永远依赖一个具体的`vector`对象,而类型推导在对象初始化的时候就完成了.在`push_back`中不需要推导`T`的类型.
  我们再看一下和`push_back`相似的`emplace_back`,这里就出现了通用引用:
  ``` c++
  template <class T>
  class vector
  {
  public:
    template <class... Args>
    void emplace_back (Args&&... args);// args is universal reference
  };
  ```
  在这里,`Args`的类型是必须在调用函数时推导的,所以`args`就是通用引用.

4.  对右值引用使用`std::move`,对通用引用使用`std::forward`
    右值引用只会绑定那些可以移动的对象.因此如果一个函数的参数是右值引用,那么它就很可能是要被移动.所以说,如果你传递一个对象到一个函数中,并且希望这个函数利用这个对象的可移动性,那么`std::move`就是正确的选择.
    ``` c++
    class Object
    {
    public:
      Widget (Widget&& rhs): name (std::move(rhs.name)) {}
    private:
      std::string name;
    };
    ```
    而通用引用只是可能会绑定那些可以移动的对象,因此我们只能在通用引用以右值初始化的时候将他们作为右值引用使用.`std::forward`就是用来完成这种工作的.
    ``` c++
    class Object{
    public:
      template <typename T>
      void setName (T&& name)
      {
        this.name = std::forwatd<T> (name);
      }
    private:
      std::string name;
    };
    ```
    总之,当把一个右值引用传递给一个函数时,应当通过`std::move`无条件将其转换为右值.而通用引用应该有条件地转换为右值.
    ``` c++
    class Object{
    public:
      template <typename T>
      void setName (T&& name_)
      {
        this.name = std::move<> (name_);
      }
    private:
      std::string name;
    };
    ```
    在这里,如果传入`setName`是一个左值,那么我们希望的是拷贝而不是移动.你可能会说这个函数就不应该使用通用引用:

    ``` c++
    class Object
    {
      public:
        void setName (const std::string& newName)
        {
          name = newName;
        }
        void setName (std::string&& newName)
        {
          name = std::move (newName);
        }
      private:
        std::string name;
    }
    ```
    这样可以工作,但是比起使用`std::forward`还是有一些退步.首先,这个方式需要写更多的源代码.其次,这种方式更加低效.比如说,考虑这种情况:
    ``` c++
    w.setName ("const string)
    ```
    对于使用模板和`std::forward`的版本,这个常亮字符串会被直接传入`setName`,然后直接用常亮字符串对`name`进行复制,不产生任何中间临时变量.但是对于重载的版本,就会增加一个临时的`std::string`变量的构造和析构的过程.
    但是,代码的复杂和运行效率降低并不是使用重载代替通用引用的最大缺点.最大的缺点是缺乏扩展性.上面的例子仅仅是一个参数而已.如果一个函数有`n`个参数,那我们岂不是需要`2^n`个重载函数么?进一步,我们还有[可变参数](http://zh.cppreference.com/w/cpp/language/parameter_pack),那就需要无数个重载函数了......对于这种情况,使用通用引用是唯一的解决方案.在这样使用模板表示参数类型的函数中,想别的函数传递参数应当使用`std::forward`.
    但也不一定如此.有的时候你可能会想要多次传递参数,这个时候只有最后一次传递可以使用`std::forward`.这样做是为了避免在还需要使用参数的时候就将其移动走.
    ``` c++
    template <class T>
    void setSignText (T&& text)
    {
      sign.setText (text);
      signHistory.add (std::forward<T> (text));
    }
    ```

    对`std::move`也有类似的考虑,有的时候你可能会需要[`std::move_if_noexcept`](http://en.cppreference.com/w/cpp/utility/move_if_noexcept).可以参考[Declare functions noexcept if it won't emit exceptions](https://lizeyan.github.io/2016/08/12/Declare-functions-noexcept-if-it-won-t-emit-exceptions/).

    有很多时候函数的返回值是按值传递的.如果此时返回值和一个右值引用或者通用引用绑定,那么应该使用`std::move`或者`std::forward`.比较下面的代码:
    ``` c++
    Matrix operator (Matrix&& lhs, const Matrix& rhs)
    {
      lhs += rhs;
      return std::move (lhs);
    }
    ```
    ``` c++
    Matrix operator (Matrix&& lhs, const Matrix& rhs)
    {
      lhs += rhs;
      return lhs;
    }
    ```
    第一个函数移动了`lhs`,第二个则需要将其拷贝到返回值.如果`Matrix`有移动构造函数而且效率很高,那么前者就有更高的效率.
    而如果`Matrix`不支持移动,这样做也没什么错.因为一个右值引用使是可以转化为一个`const`的左值引用的,此时前者中`Matrix`会正常拷贝.如果日后`Matrix`实现了移动构造,那么这段代码自然就会变成移动.而不是拷贝,不需要修改.
    上面说了,这样做的前提是返回值和一个右值引用或者通用引用绑定.有人可能想要忽视这一点,做一些自以为聪明的扩展:
    ``` c++
    Widget makeWidget ()
    {
      Widget w;
      return std::move (w);
    }
    ```
    这样做是有问题的.因为C++标准委员会早在移动语义出现之前就考虑到了返回一个局部变量的情况.C++标准通过将局部变量直接分配到返回值所在地址来避免拷贝.这是C++标准中少见的允许程序运行结果发生变化的优化规则,被称为[Return Value Optimization](https://en.wikipedia.org/wiki/Return_value_optimization#Compiler_support).这个优化需要满足两个条件:
    - 局部变量的类型和返回值相同
    - 直接返回该局部变量
    
    为什么说这样优化程序可能运行结果发生变化呢?因为拷贝构造函数可能是有副作用的,比如更改一个全局变量的值.
    
    上面的例子完全符合执行这个所谓RVO的优化的所有条件.但是如果你使用了`std::move`,`move`就会同时正常发挥作用(这里我假设`Widget`有移动函数).这个时候,局部变量`w`被移动到了返回值的位置.为什么这个时候RVO规则不发生作用了呢?因为上面的第二条规则并不满足.在这是,被返回的不是该局部变量,而是一个到该局变量的引用.
    
    在这里,程序员试图优化代码,结果反而让代码更慢了.(所以说提高姿势水平很重要)
  
    你可能会想,有的时候实现RVO是很复杂的.是的.比如说一个函数内部有很复杂的控制流,对于编译器来说,很难确定要返回的到底是什么.
    
    尽管如此,在这个时候在返回语句`std::move`也不是一个好主意.因为标准规定,在RVO的条件被满足的时候,要么像上面那样,直接在返回值的位置分配局部变量,要么就将这个局部变量在返回时看成是右值.这是为了编译器的实现考虑.将一个变量看成右值,其实就是隐式地加上了`std::move`而已,所以你不需要自己再写一次.
