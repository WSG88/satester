总结来源网络

一. 内存

1. 内存泄漏

说到内存方面，最经典的内存问题当数内存泄漏。百度上对内存泄漏的定义是这样的：内存泄漏（Memory Leak）是指程序中己动态分配的堆内存由于某种原因程序未释放或无法释放，造成系统内存的浪费，导致程序运行速度减慢甚至系统崩溃等严重后果。通俗点讲，在大部分应用中，会有一类功能是需要加载附加资源的，比如显示从网络下载的文本或图片。这类功能往往需要在内存中存放要使用的资源对象，退出该功能后，就需要将这些资源对象清空。如果忘了清理，或者是代码原因造成的清理无效，就会形成内存泄漏。
2. 垃圾回收

说到了内存泄漏，又不得不提到垃圾回收（Garbage Collector，简称 GC），内存中的垃圾，主要指的是内存中已无效但又无法自动释放的空间，除非是重启系统不然永远也不会还给操作系统。这样以来，时间久了当程序运行的时候就会产生很多垃圾，一方面浪费了不少内存空间，另一方面如果同一个内存地址被删除两次的话，程序就会不稳定，甚至奔溃。

在 Java 程序运行过程中，一个垃圾回收器会不定时地被唤起检查是否有不再被使用的对象，并释放它们占用的内存空间。但垃圾回收器的回收是随机的，可能在程序的运行的过程中，一次也没有启动，也可能启动很多次，它并不会因为程序一产生垃圾，就马上被唤起而自动回收垃圾。所以垃圾回收也并不能完全避免内存泄漏的问题。

另一方面，垃圾回收也会给系统资源带来额外的负担和时空开销。它被启动的几率越小，带来的负担的几率就越小。
3. 内存指标

内存指标有 VSS、RSS、PSS、USS，他们的含义分别是：

VSS：Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）

RSS：Resident Set Size 实际使用物理内存（包含共享库占用的内存）

PSS：Proportional Set Size 实际使用的物理内存（按比例分配共享库占用的内存）

USS：Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）

一般来说内存占用大小有如下规律：VSS >= RSS >= PSS >= USS，一般测试中关注的比较多的是 PSS 这个指标。
4. 监控与分析工具

以下是几种常见的内存分析工具，具体使用方法这里就不详述了。
4.1 Memory Monitor

该工具位于 Android Monitor 下面，Android Monitor 是 Android Studio 自带的一个强大的性能分析工具，里面一共包含 5 个模块：Logcat、Memory、CPU、Network 及 GPU。

Memory Monitor 可以实时查看 App 的内存分配情况，判断 App 是否由于 GC 操作造成卡顿以及判断 App 的 Crash 是否是因为超出了内存。
4.2 Heap Viewer

该内存检测工具位于 DDMS 下面，在 Android Studio 里面可以通过 Tools-Android-Android Device Monitor 打开，Heap Viewer 可以实时查看 App 分配的内存大小和空闲内存大小，并且发现 Memory Leaks。

4.3 MAT

MAT（Memory Analyzer Tool），是一个被老生常谈的 Android 内存分析工具，它可以清楚的获知整体内存使用情况。虽然是 Eclipse 的工具，但也可以单独运行，不需要安装 Eclipse。

二. CPU

1. 时间片

时间片即 CPU 分配给各个程序的时间，每个线程被分配一个时间段，称作它的时间片，即该进程允许运行的时间，使各个程序从表面上看是同时进行的。
2. Jiffies

2.1 Jiffies的概念

要讲 Jiffies 需要先提到这两个概念：HZ 和 Tick

    HZ：Linux 核心每隔固定周期会发出 timer interrupt (IRQ 0)，HZ 是用来定义每一秒有几次 timer interrupts。例如 HZ 为 1000，就代表每秒有 1000 次 timer interrupts。

    Tick：HZ 的倒数，Tick = 1/HZ，即 timer interrupt 每发生一次中断的时间。如 HZ 为 250 时，tick 为 4 毫秒（millisecond）。

而 Jiffies 为 Linux 核心变量，是一个 unsigned long 类型的变量，被用来记录系统自开机以来，已经过了多少 tick。每发生一次 timer interrupt，Jiffies 变数会被加 1。
2.2 查看 Jiffies 的方法

Linux 下使用命令cat /proc/stat，查看具体整机的 Jiffies，如图：

Linux 下使用命令cat /proc/<进程id>/stat，查看具体某个进程的 Jiffies：

3. CPU 使用率

在 Linux 系统下，CPU 利用率分为用户态、系统态和空闲态，他们分别代表的含义为：用户态表示 CPU 处于用户态执行的时间，系统态表示系统内核执行的时间，空闲态表示空闲系统进程执行的时间。

而一个 App 的 CPU 使用率 = CPU 执行非系统空闲进程时间 / CPU 总的执行时间，也可以表示为 App 用户态 Jiffies + App 系统态 Jiffies / 手机总 Jiffies。
4. CPU 过高会带来的影响

可能会使整个手机无法响应，整体性能降低，引起 ANR，导致手机更耗电，降低用户体验等。
三. 流量

1. 定义

我们的手机通过运营商的网络访问 Internet，运营商替我们的手机转发数据报文，数据报文的总大小（字节数）即流量，数据报文是包含手机上下行的报文。
2. 常用流量测试方法

2.1 抓包测试法

主要是利用工具 Tcpdump 抓包，导出 pcap 文件，再在 wireshark 中打开进行分析。
2.2 统计测试法

2.2.1 读取 linux 流量统计文件

利用 Android 自身提供的 TCP 收发长度的统计功能，获取 App 的 tcp_snd 和 tcp_rcv 的值，测试一段时间后再分别统计一次，用 tcp_snd

两者的差值得到发送流量，用 tcp_rcv 两者的差值得到接受流量。
2.2.2 利用 Android 流量统计 API

    TrafficStats

Android 2.2 版本开始加入 android.net.TrafficStats 类来实现对流量统计的操作。

部分方法如下：

static long getMobileRxBytes() //获取通过移动数据网络收到的字节总数 
static long getMobileTxBytes() //通过移动数据网发送的总字节数 
static long getTotalRxBytes() //获取设备总的接收字节数 
static long getTotalTxBytes() //获取设备总的发送字节数 
static long getUidRxBytes(int uid) //获取指定uid的接收字节数 
static long getUidTxBytes(int uid) //获取指定uid的发送字节数 

    NetworkStatsManager

Android 6.0 版本开始，为了打破了原本 TrafficStats 类的查询限制，官方又提供了 NetworkStatsManager 类，可以获取更精准的网络历史数据，也不再是设备重启以来的数据。部分方法如下：

 NetworkStats.Bucket querySummaryForDevice(int networkType, String subscriberId, long startTime, long endTime) // 查询指定网络类型在某时间间隔内的总的流量统计信息
 NetworkStats queryDetailsForUid(int networkType, String subscriberId, long startTime, long endTime, int uid) // 查询某uid在指定网络类型和时间间隔内的流量统计信息
 NetworkStats queryDetails(int networkType, String subscriberId, long startTime, long endTime) // 查询指定网络类型在某时间间隔内的详细的流量统计信息（包括每个uid）

四. 电量

1.耗电场景

    定位，尤其是调用 GPS 定位。

    网络传输，尤其是非 Wifi 环境。

    屏幕亮度

    CPU 频率

    内存调度频度

    wake_locker 时间和次数

    其他传感器

2.测试方法

2.1 通过系统文件获取电量记录

使用命令 adb shell dumpsys batterystats> batterystats.txt 可以打印出详细的耗电相关信息并保存统计的电量信息到 batterystats.txt 这个文件里。

2.2 通过导入 batterystats.txt 到 Google 开源工具 battery historian 进行分析

因为这个工具是 Go 语言开发，所以需要预装Go语言开发环境，当然如果你不想配置Go语言环境，官方还提供了一种更方便的方案，通过安装 docker 环境来使用这个工具。具体这个工具的配置安装和具体使用方法以及参数的代表含义，我会单独再写一篇文章记录，先抛砖引玉放一张这个工具的运行截图。

3.优化方法

3.1 CPU 时间片

当应用退到后台运行时，尽量减少应用的主动运行，当检测到 CPU 时间片消耗异常时，深入线程进行分析。
3.2 wake lock

前台运行时不要注册 wake lock。

后台运行时，在保证业务需要的前提下，应尽量减少注册 wake lock。

降低对系统的唤醒频率， 使用 partial wake lock 代替 wake lock。
3.3 传感器

合理设置 GPS 的使用时长和使用频率。
3.4 云省电策略

考虑到用户使用场景的多样性，导致很难定位用户异常耗电的根源，所以为了更深一层弄清楚这些问题，可以考虑定期上报灰度用户手机电量数据的方式来分析问题。
五. 启动时间

可使用命令 adb shell am start -W packagename/activity 查看 App 启动耗时，查看了一下我们自己的 App Android 版本的启动耗时如下：

注释：

WaitTime：总的耗时，包括前一个应用 Activity pause 的时间和新应用启动的时间

ThisTime：一连串启动 Activity 的最后一个 Activity 的启动耗时

TotalTime：新应用启动的耗时，包括新进程的启动和 Activity 的启动，但不包括前一个应用 Activity pause 的耗时