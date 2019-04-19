---
title: lambda in java
date: 2016-07-28 13:29:48
tags: ["java", "lambda"]
---
介绍Java中的lambda函数。

<!-- more -->
Eg:
lambda函数的基本语法为:
``` java
(ParamType param) -> ReturnType {Function Body;};
```
返回值为void时不写ReturnType。
于是你可以这样很简单地新建一个线程:
``` java
Thread thread = new Thread ( () -> 
{
    func ();
});
```
在Java中，可以将lamda表达式转换为任何只有一个方法的接口的实现。
lamda中*不需要*显式地capture变量，可以访问lamda表达式定义所在位置的作用域中的所有变量。但是Java限制这些被capture的变量是final或者effectively final的，即这些变量在声明之后不能修改。这是为了避免发生一些多线程情境下发生的bug。:)
Java提供了一些接口用来表示lambda函数的类型，如下所示：
一个函数定义如下：
``` java        
public static <X, Y> void processElements(
    Iterable<X> source,
    Predicate<X> tester,
    Function <X, Y> mapper,
    Consumer<Y> block) {
    for (X p : source) {
        if (tester.test(p)) {
            Y data = mapper.apply(p);
            block.accept(data);
        }
    }
}
```

如此调用这个函数:
``` java      
processElements(
    roster,
    p -> p.getGender() == Person.Sex.MALE
        && p.getAge() >= 18
        && p.getAge() <= 25,
    p -> p.getEmailAddress(),
    email -> System.out.println(email)
);
```
        
Iterable<T> 是一个表示可以使用迭代器迭代的接口。

lamda表达式常用的标准的函数对象接口包括：

接口|说明|解释
---|---|---
Consumer<T>| accept(T t)| 
BiConsumer<T,U>| accept(T t, U u)|    
Function<T,R>|   apply(T t)-> R|  
BiFunction<T,U,R>| apply(T t, U u)-> R| 
BinaryOperator<T>| apply(T t, T u)-> T| 
Predicate<T>|    test(T t)-> boolean| 
BiPredicate<T,U>|    test(T t, U u)-> boolean|    
BooleanSupplier| getAsBoolean() -> boolean|   从local variable中capture变量
Supplier<T>| get()->T|    

