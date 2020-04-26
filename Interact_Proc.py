import subprocess
import threading 
import time
import inspect
import ctypes
import os
import signal

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

class Interact_Proc():
    def __init__(self,command):
        self.process =subprocess.Popen(command,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.mythread=threading.Thread(target=self.read_message,args=())
        self.mythread.start()
        self.result=''

    
    def read_message(self):
        try:
            while True:
                line = self.process.stdout.readline() 
                if not line:  
                    break
                self.result+=line.decode()
        except Exception as e:
            print('read message error'+str(e))


    def send_cmd(self,cmd,timeout=None):
        self.result=''
        cmd+='\n'
        self.process.stdin.write(cmd.encode())
        self.process.stdin.flush()
        if(timeout!=None):
            time.sleep(timeout)
        return self.result
    
    def close(self):
        stop_thread(self.mythread)
        self.process.kill()
        # os.kill(self.process.pid,signal.SIGKILL)

aa=Interact_Proc('bash')
res=aa.send_cmd('ls',0.1)
print(res)

res=aa.send_cmd('echo "helloworld"',0.1)
print(res)

res=aa.send_cmd('cat ./tt.py',0.1)
print(res)
aa.close()

os.kill(os.getpid(),signal.SIGKILL)






