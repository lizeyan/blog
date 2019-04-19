---
title: How to simulate keyword friend like in c++ in JAVA
date: 2016-07-26 10:59:54
tags: ["Java", "friend", "c++"]
---
如何在Java中模仿c++的关键字friend的功能呢？

<!-- more -->

有的时候我们想要一个类的某些方法是私有的，但是同时又能够被特定的类访问，比如下面这样
eg:
``` c++
class Data
{
public:
    int get ();//访问
private:
    friend class Control;//只允许Control访问修改接口
    void set (int d);//修改
    int data;
}
```
数据类提供了访问和修改的接口，但是我并不想让每个类都能够修改数据。在c++里通过友元类可以轻易实现，但是在JAVA中要怎么做呢？
我们可以通过一个机智的方法来模拟友元:
``` java
public class Data
{
    public int get ();//访问
    public void set (Control.SecurityKey sk, int d) {set (d)}//公开的修改接口必须传入安全密匙，注意处理null
    private void set (int d);//私有的修改接口
    private int data;
}
public class Control
{
    public static class SecurityKey {private Security () {}}//定义公共的安全密匙类，所有类都可以访问，但是因为构造函数是私有的，所以只有Control可以新建安全密匙。
    private SecurityKey sk = new SecurityKey ();//私有的安全密匙
    public Control ()
    {
        Data d = new Data ();
        d.set (sk);//通过安全密匙顺利修改
    }
}
```
其他的类因为没有办法新建`SecurityKey`，也不能访问到`Control`私有的`SecurityKey`成员变量，就保证了它们不能修改数据。
唯一的问题是null也可以视为`SecurityKey`，所以在修改接口中视情况自行处理一下传入了null的情况吧。
eg:
``` java
public void set (Control.SecurityKey sk, int d)
{
    if (securityNeed == true && sk == null)
        throw new Exception ("balabala");
    //do something
}
public void lock ()
{
    securityNeed = true;
}
```

[Reversi](https://github.com/lizeyan/Reversi)是一个更实际的例子。
这是一个对战黑白棋程序。`Composition`存储的是棋局的数据，`Reversi`是控制游戏流程的控制器，`Player`是玩家或者AI进行决策的类。
当我们构造一个新的`Player`时，我们有必要将`Composition`传入从而让玩家和AI得到棋局的信息。但是`Player`是绝对不能自由修改真正的棋局的，他们只能向控制器报告自己的决策结果然后由控制器执行落子。（否则AI的实现岂不是有可能直接铺满整个棋盘？毕竟`Player`的具体实现者很可能不是开发游戏的人员，他们没有义务维护游戏的规则。）
当然，我们可以每回合传入一个真正棋局的拷贝保证`Player`中只能访问而不能修改，但这样比起安全密匙的方法大大浪费了时间和空间。我们只要让`Composition`的所有涉及修改的方法都需要`Reversi`私有的安全密匙作为参数即可保证`Player`无法修改了，附加的时间空间消耗是很小的。