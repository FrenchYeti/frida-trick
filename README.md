# frida-trick
My own collection of Frida script and tricks

## Scripts summary

### file_access.js
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

## Shell tricks

Attach to a running process by name.
```
frida -U -p $(frida-ps -U | grep <appname> | tail -n 1 | cut -b1-5) -l <your_scripts>
```

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
