#!/bin/bash
remote_host='213.219.36.190'
remote_port='8022'
remote_user='root'
remote_passwd=''  # here is ceritifaicate

remote_dir='/root/Data/'
local_dir='/root/Data/'


clean_local()
{
    if [ -f ${local_dir}.lock ]; then
        exit 1
    fi
    mkdir -p ${local_dir}.tmp
    rm -rf ${local_dir}.tmp/.*
}

sync_lock()
{
    ssh -p ${remote_port} ${remote_user}@${remote_host} ": > ${remote_dir}.lock"
}

sync_data()
{
    rsync -e "ssh -p ${remote_port}" -az --exclude={.tmp,.lock}  ${remote_user}@${remote_host}:${remote_dir} ${local_dir}.tmp/
    #scp  -r -P ${remote_port} ${remote_user}@${remote_host}:${remote_dir} ${local_dir}.tmp
}

sync_ack()
{
    if [ $? -ne 0 ]; then
        :
        ##echo 'failed'
    else
        ##echo 'success'
        if [ ! -f ${local_dir}.lock ]; then
            mv ${local_dir}.tmp/* ${local_dir}
            ssh -p ${remote_port} ${remote_user}@${remote_host} "rm -rf ${remote_dir}* && rm -rf ${remote_dir}.lock"
        fi
        #ssh -p ${remote_port} ${remote_user}@${remote_host} "rm -rf ${remote_dir}* && rm -rf ${remote_dir}.lock"
    fi
}

clean_local
sync_lock
sync_data
sync_ack
