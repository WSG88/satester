#Android 逆向分析步骤

##基础
1.android系统基本介绍

2.apk隐藏图标和自启动原理

3.apk常用分析工具

4.smali汇编

5.dex格式

6.ndk中调用java代码，java调用c,c++

7.java层反编译动态调试

8.ida讲解，以及识别ndk函数,动态调试so

9.xpose注入，动态hook，dalvik注入原理讲解


##so层知识点：

1、arm汇编与so文件格式

2、so多种native hook源码分析与设计

3、so文件源码解析加载装载原理和修复

4、反调试方法总结

5、进程注入技术


##root方面：(可以普及)

1、常见内核漏洞类型

2、内核缓解措施

3、缓解措施的绕过技巧

4、Root提权中常用技巧

5、root检测


##协议分析：

抓包，解密（常见加解密方法），smali动态调试（idea，或者android studio），ddms栈回溯，

apktool的使用，jeb的使用，分析流程，hook结合，最终解密数据包。完成协议分析。 