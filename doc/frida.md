pip install frida

frida_server的下载地址：https://github.com/frida/frida/releases

adb push frida-server /data/local/tmp/
adb shell
su
cd /data/local/tmp/
chmod 777 frida-server
./frida-server

adb forward tcp:27042 tcp:27042
adb forward tcp:27043 tcp:27043

frida-ps -R
PID Name


得到android手机当前最前端Activity所在的进程

    import frida
    rdev = frida.get_remote_device()
    front_app = rdev.get_frontmost_application()
    print front_app
    
    
枚举android手机所有的进程

    import frida
    rdev = frida.get_remote_device()
    processes = rdev.enumerate_processes()
    for process in processes:
        print process
        
        
枚举某个进程加载的所有模块以及模块中的导出函数


    import frida 
    rdev = frida.get_remote_device() 
    session = rdev.attach("com.tencent.mm") 
    #如果存在两个一样的进程名可以采用rdev.attach(pid)的方式 
    modules = session.enumerate_modules() 
    for module in modules: 
      print module 
      export_funcs = module.enumerate_exports() 
      print "\tfunc_name\tRVA" 
      for export_func in export_funcs: 
        print "\t%s\t%s"%(export_func.name,hex(export_func.relative_address))


hook android的native函数

    import frida
    import sys
    rdev = frida.get_remote_device()
    session = rdev.attach("com.tencent.mm")
    scr = """
    Interceptor.attach(Module.findExportByName("libc.so" , "open"), {
        onEnter: function(args) {
            send("open("+Memory.readCString(args[0])+","+args[1]+")");
        },
        onLeave:function(retval){
        
        }
    });
    """
    script = session.create_script(scr)
    def on_message(message ,data):
        print message
    script.on("message" , on_message)
    script.load()
    sys.stdin.read()

hook android的java层函数

如下代码为hook微信（测试版本为6.3.13，不同版本由于混淆名字的随机生成的原因或者代码改动导致类名不一样）
com.tencent.mm.sdk.platformtools.ay类的随机数生成函数，让微信猜拳随机（type=2），而摇色子总是为6点（type=5）

    import frida
    import sys
    rdev = frida.get_remote_device()
    session = rdev.attach("com.tencent.mm")
    
    scr = """
    Java.perform(function () {
    var ay = Java.use("com.tencent.mm.sdk.platformtools.ay");
    ay.pu.implementation = function(){
        var type = arguments[0];
        send("type="+type);
        if (type == 2)
        {
        return this.pu(type);
        }
        else
        {
        return 5;
        }
    };
    
    });
    """
    
    script = session.create_script(scr)
    def on_message(message ,data):
        print message
    script.on("message" , on_message)
    script.load()
    sys.stdin.read()

通过frida向android进程注入dex

    import frida, sys, optparse, re
    def on_message(message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)
    
    jscode = """
    Java.perform(function () {
        var currentApplication = Java.use("android.app.ActivityThread").currentApplication();
        var context = currentApplication.getApplicationContext();
        var pkgName = context.getPackageName();
        var dexPath = "%s";
        var entryClass = "%s";
        Java.openClassFile(dexPath).load();
        console.log("inject " + dexPath +" to " + pkgName + " successfully!")
        Java.use(entryClass).%s("%s");
        console.log("call entry successfully!")
    });
    """
    
    def checkRequiredArguments(opts, parser):
        missing_options = []
        for option in parser.option_list:
            if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) == None:
                missing_options.extend(option._long_opts)
        if len(missing_options) > 0:
            parser.error('Missing REQUIRED parameters: ' + str(missing_options))
    
    if __name__ == "__main__":
        usage = "usage: python %prog [options] arg\n\n" \
                "example: python %prog -p com.android.launcher " \
                "-f /data/local/tmp/test.apk " \
                "-e com.parker.test.DexMain/main " \
                "\"hello fridex!\""
        parser = optparse.OptionParser(usage)
        parser.add_option("-p", "--package", dest="pkg", type="string",
                          help="[REQUIRED]package name of the app to be injected.")
        parser.add_option("-f", "--file", dest="dexPath", type="string",
                          help="[REQUIRED]path of the dex")
        parser.add_option("-e", "--entry", dest="entry", type="string",
                          help="[REQUIRED]the entry function Name.")
    
        (options, args) = parser.parse_args()
        checkRequiredArguments(options, parser)
        if len(args) == 0:
            arg = ""
        else:
            arg = args[0]
    
        pkgName = options.pkg
        dexPath = options.dexPath
        entry = options.entry.split("/")
        if len(entry) > 1:
            entryClass = entry[0]
            entryFunction = entry[1]
        else:
            entryClass = entry[0]
            entryFunction = "main"
    
        process = frida.get_usb_device(1).attach(pkgName)
        jscode = jscode%(dexPath, entryClass, entryFunction, arg)
        script = process.create_script(jscode)
        script.on('message', on_message)
        print('[*] Running fridex')
        script.load()
        sys.stdin.read()

通过注入抛出异常代码实现跟踪程序调用栈
    重打包写入异常代码进行栈跟踪
    
    
    
https://mp.weixin.qq.com/s/mvTxwQdX9n9e_m-Kar7OyQ

