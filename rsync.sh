#!/bin/bash
remote_host='172.16.30.1'
remote_port='22'
remote_user='bf'
remote_passwd=''  # here is ceritifaicate

remote_dir='/home/bf/Data/'
local_dir='/home/Data/'


clean_local()
{
    if [ -f ${local_dir}.lock ]; then
        exit 1
    fi
    mkdir -p ${local_dir}.tmp
}

sync_lock()
{
    ssh -p ${remote_port} ${remote_user}@${remote_host} ": > ${remote_dir}.lock"
}

sync_data()
{
    rsync -e "ssh -p ${remote_port}" -az ${remote_user}@${remote_host}:${remote_dir} ${local_dir}.tmp/
    #scp  -r -P ${remote_port} ${remote_user}@${remote_host}:${remote_dir}* ${local_dir}.tmp/
}

sync_ack() 
{
    if [ $? -ne 0 ]; then
	:
	##echo 'failed'
    else
        ##echo 'success'
	mv ${local_dir}.tmp/* ${local_dir}
        ssh -p ${remote_port} ${remote_user}@${remote_host} "rm -rf ${remote_dir}* && rm -rf ${remote_dir}.lock"
    fi
}

clean_local
sync_lock
sync_data
sync_ack
