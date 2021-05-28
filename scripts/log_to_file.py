# 

import frida
import sys
import os 
import json
from optparse import OptionParser


CONFIG = {
    "dir": os.getcwd()+"/tmp/"
}

# hook message must contains at least "myVarName" (the name of target file) and "myVarValue" (the value)

def storeLog(meta,data):
    print("Processing hook log ...")
        
    path = CONFIG['dir']+"/"
    if meta.has_key('size') is False:
        fd = open(path+("{0}.bin".format(meta["myVarName"])), "w+")
        fd.write(meta['myVarValue'])
        fd.close()
        print("[*] Hook logs stored")
    elif data is not None:
        fd = open(path+("{0}_{1}.bin".format(meta["myVarName"],meta["size"])), "w+b")
        fd.write(data)
        fd.close()
        print("[*] Hook logs stored")
    else:
        print(data)
        

def on_message(message, data):
    try:
        if (message is not None) and (message["payload"] is not None):
            if message["payload"].has_key('cmd'):
                storeLog(message["payload"], data)
    except Exception as e:
        print("Exception catched")
        print(e)


if __name__ == '__main__':
    try:
        parser = OptionParser(usage="usage: %prog [options] <process_to_hook>",version="%prog 1.0")
        parser.add_option("-A", "--attach", action="store_true", default=False,help="Attach to a running process")
        parser.add_option("-S", "--spawn", action="store_true", default=False,help="Spawn a new process and attach")
        parser.add_option("-P", "--pid", action="store_true", default=False,help="Attach to a pid process")
        parser.add_option("-o", "--output", action="store_true", default=False,help="Output folder")

        (options, args) = parser.parse_args()
        if (options.spawn):
            print ("[+] Spawning "+ str(args[0]))
            pid = frida.get_usb_device().spawn([args[0]])
            session = frida.get_usb_device().attach(pid) 
        elif (options.attach):
            print ("[+] Attaching to process"+str(args[0]))
            session = frida.get_usb_device().attach(str(args[0]))
        elif (options.pid):
            print ("[+] Attaching to PID "+str(args[0]))
            session = frida.get_usb_device().attach(int(args[0]))
        elif (options.output):
            if os.path.isdir(args[0]) == false:
                os.mkdir(args[0])
                CONFIG.dir = args[0]
                
        else:
            print ("Error")
            print ("[!] Option not selected. View --help option.")
            sys.exit(0)

        hook = open(os.getcwd()+"/hook.js", "r")
        script = session.create_script(hook.read())
        script.on('message', on_message)
        script.load()
        sys.stdin.read()

    except KeyboardInterrupt:
        sys.exit(0)
