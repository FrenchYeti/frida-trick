# frida-trick
My own collection of Frida script and tricks (Java / Native / TEE)

## 1. Scripts summary

### 1.a file_access.js ( do file descriptor lookup)
File : [https://raw.githubusercontent.com/FrenchYeti/frida-trick/master/scripts/file_access.js](https://raw.githubusercontent.com/FrenchYeti/frida-trick/master/scripts/file_access.js)
Observe file system accesses by hooking some java.io.File* classes and methods, libc open/read functions and try to resolve association between file descriptor and path. Optionally, it can dumps the data. The first block contains the configuration.
```
var CONFIG = {
    // if TRUE enable data dump 
    printEnable: true,
    // if TRUE enable libc.so open/read/write hook
    printLibc: false,
    // if TRUE print the stack trace for each hook
    printStackTrace: false,
    // to filter the file path whose data want to be dumped in ASCII 
    dump_ascii_If_Path_contains: [".log", ".xml", ".prop"],
    // to filter the file path whose data want to be NOT dumped in hexdump (useful for big chunk and excessive reads) 
    dump_hex_If_Path_NOT_contains: [".png", "/proc/self/task", "/system/lib", "base.apk", "cacert"],
    // to filter the file path whose data want to be NOT dumped fron libc read/write (useful for big chunk and excessive reads) 
    dump_raw_If_Path_NOT_contains: [".png", "/proc/self/task", "/system/lib", "base.apk", "cacert"]
}
```

## 2. Tricks

### 2.a Generic tricks
Attach to a running process by name.
```
frida -U -p $(frida-ps -U | grep <appname> | tail -n 1 | cut -b1-5) -l <your_scripts>
```


### 2.b Java tricks
Print the stack trace if called from a Java Hook (see *scripts/file_access.js* script for example)
```
var JavaThread = Java.use("java.lang.Thread");
function printStackTrace(){
    var th = Java.cast( JavaThread.currentThread(), JavaThread);
    var stack = th.getStackTrace(), e=null;

    for(var i=0; i<stack.length; i++){
        console.log("\t"+stack[i].getClassName()+"."+stack[i].getMethodName()+"("+stack[i].getFileName()+")");
    }
}
```


### 2.c TEE tricks

To observe shared buffer, set the folder *scripts/qsee* as working directory and run frida-trace like below.   
```
cd ./scripts/qsee
frida-trace -U -p $(frida-ps -U | grep system_server | cut -b1-5) -I "libQSEEComAPI.so"
```



