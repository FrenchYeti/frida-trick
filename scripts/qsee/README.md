## setup

When the function QSEECom_send_cmd() is called, the buffer is saved to a file in the folder "*/data/local/tmp/tee_buffers*".
You should configure properly the rights in order to be able to write in this folder from the hooked process.

It can be done with this "one-shoot-style" command :
```
adb shell su -c "mkdir /data/local/tmp/tee_buffers; chmod 777 /data/local/tmp/tee_buffers; setenforce 0"
```

## run

When setup is ok, you can run the following command from the location of this README.md file
```
frida-trace -U -p $(frida-ps -U | grep <process_name> | cut -b1-5) -I "libQSEEComAPI.so"
```


