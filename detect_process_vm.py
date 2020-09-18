import os,time

proc_name='ftp.proxy -D 7021 172.16.200.1'
proc_id=None

def get_proc_id(pname):
    if(proc_id!=None):
        return proc_id   
    res = os.popen("ps -axu | grep -v grep | grep '{}'| awk '{}'".format(pname,'{print $2}')).read().strip()
    return res
    # res = os.popen('ps -e -o "pid,comm,args,pcpu,rsz,vsz,stime,user,uid"').read().strip()
    # print(res)

def get_rsz_vsz(pid):
    if pid == None or pid == '':
        return None,None
    res = os.popen(" ps -e -o 'pid,rsz,vsz' |grep -v grep |grep {}".format(pid)).read().strip()
    idd,rsz,vsz=(' '.join(res.split())).split(' ')
    return rsz,vsz

def main():
    ts=time.time()
    pid=get_proc_id(proc_name)
    if(pid==''):
        print('未找到进程：{}'.format(proc_name))
    else:
        rsz,vsz = get_rsz_vsz(pid)
        print('{},{},{},{},{}'.format(ts,proc_name,pid,rsz,vsz))    

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)

