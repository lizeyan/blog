---
title: 'QML example: clocks'
date: 2016-09-05 23:10:42
tags: ["QML"]
categories:
- QML
---
通过Qt Example中的Clocks学习QML

<!-- more -->

QML时Qt的一种新的图形界面开发框架.它使用一种类似JSON的简单的标记式语法定义界面,内嵌javascript实现逻辑运算,甚至可以和C++交互.QML开发的界面相比Qt Widgets那一套,增加了对GPU硬件加速的支持,从而更加适合实现复杂的动画效果.QML还更容易适配不同的平台,甚至移动端和桌面端也可以同时支持.

Qt为QML准备了一系列标准库,整个框架称为Qt Quick.现在要通过Qt Quick Example中的Clocks学习QML.这个示例Qt自带,如果没有安装上可以在Qt官方文档上看到讲解和代码.我使用的是Qt5.7,Qt Creator4.1.

1. `main.cpp`
``` c++
DECLARATIVE_EXAMPLE_MAIN(demos/clocks/clocks)
```
整个main.cpp的核心只有一行,这个宏定义其实就是一个Qt Quick工程的标准main函数实现:
``` c++
#define DECLARATIVE_EXAMPLE_MAIN(NAME) int main(int argc, char* argv[]) \
{\
    QGuiApplication app(argc,argv);\
    app.setOrganizationName("QtProject");\
    app.setOrganizationDomain("qt-project.org");\
    app.setApplicationName(QFileInfo(app.applicationFilePath()).baseName());\
    QQuickView view;\
    if (qgetenv("QT_QUICK_CORE_PROFILE").toInt()) {\
        QSurfaceFormat f = view.format();\
        f.setProfile(QSurfaceFormat::CoreProfile);\
        f.setVersion(4, 4);\
        view.setFormat(f);\
    }\
    view.connect(view.engine(), &QQmlEngine::quit, &app, &QCoreApplication::quit);\
    new QQmlFileSelector(view.engine(), &view);\
    view.setSource(QUrl("qrc:///" #NAME ".qml")); \
    if (view.status() == QQuickView::Error)\
        return -1;\
    view.setResizeMode(QQuickView::SizeRootObjectToView);\
    if (QGuiApplication::platformName() == QLatin1String("qnx") || \
          QGuiApplication::platformName() == QLatin1String("eglfs")) {\
        view.showFullScreen();\
    } else {\
        view.show();\
    }\
    return app.exec();\
}
```
在Qt Creator里右键选择`Follow the symbol under cursor`就可以看到这个宏定义.
可以看到它通过一个`QQuickView`渲染了一个`.qml`文件,这个文件就是QML的主视窗的定义.

2. `clocks.qml`
前两行是`import`语句.`import`可以用来引入QML模块,JavaScript资源或者组件文件夹,基本的语法是:
```
import <ModuleIdentifier> <Version.Number> [as <Qualifier>]
import "<JavaScriptFile>" as <Identifier>
import "<DirectoryPath>" [as <Qualifier>]
```
然后这个文件定义了一个`Rectangle`对象,这就是我们要展示的主窗体.一个QML文件中只能定义一个对象,每个对象有一个对象类型和一对花括号组成.花括号中间是对象的属性和子对象的定义.
``` QML
Rectangle
{
    ......
}
```
属性的
 - 声明方式为`[default] property <propertyType> <propertyName>`
 - 声明与初始化:`[default] property <propertyType> <propertyName>: <value>`
 - 初始化: `<propertyName> : <value>`
 - 引用创建: `[default] property alias <name>: <alias reference>`

属性中值得特殊注意的是id属性,id是QML语法提供给每个对象的属性,不能被重写或重定义.对象的id在对象创建之后就无法修改.我们可以通过一个对象的id来引用这个对象,但是我们不能通过引用一般属性的方法来引用id属性.([QML
 id attribute](http://doc.qt.io/qt-5/qtqml-syntax-objectattributes.html#the-id-attribute))
```
root.width // fine
root.id // error
```
之后定义的`width`,`height`,`color`都很好理解.之后又定义了3个子对象,但是并没有指定他们的属性名是什么,这是怎么回事?
QML有一种机制叫做[`default property`](http://doc.qt.io/qt-5/qtqml-syntax-objectattributes.html#default-properties),所有没有声明属性名的对象定义都被认为是属于这个默认属性.`Rectangle`继承自`Item`,而`Item`的默认属性是`data`,同时如果子对象也是`Item`的子类,子对象还会被加入`Children`列表.

ListView是一个列表,通过`delegate`属性指定了显示的格式,这里在`Clock.qml`详细定义了样式.`model`中制定了列表项的数据.

Image还有特殊的一个定义:
```
Behavior on opacity { NumberAnimation { duration: 500 } }
```
这是定义了一个属性修改器.QML中每个属性可以有一个修改器,通过`<ModifierType> on <propertyName>`的语法定义.这里是规定了一个动画,表示箭头的透明度变化是500ms的渐变.

3. `Clock.qml`
这个文件定义了每个钟表.
......
钟表的指针使用静态图片,然后定义了图片的`transform`属性,使图片发生旋转.同时,旋转的角度是和时间绑定的,这样就实现了指针转动的效果.时间的获取是通过一个定时器`Timer`,每隔100ms一个js函数被调用.


