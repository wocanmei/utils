#!/bin/bash

data_ip='198.181.40.229'
data_type='itor'

files=(
	/root/Tor/mydir/cache_get_v2.data
        /root/Tor/mydir/cache_get_v3.data
        /root/Tor/mydir/cache_post_v2.data
        /root/Tor/mydir/cache_post_v3.data
        /root/Tor/mydir/hops.data
      )



function mv_files(){
    for file in ${files[*]};
    do
        fname=${file##*/}
        current=`date "+%Y-%m-%d %H:%M:%S"`
        timeStamp=`date -d "$current" +%s`
        newfname="${data_ip}_${data_type}_${timeStamp}_$fname"
        mv $file /root/Data/$newfname
    done
}

mv_files
