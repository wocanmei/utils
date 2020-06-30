#!/bin/bash

function get_timestap(){
    current=`date "+%Y-%m-%d %H:%M:%S"`
    timeStamp=`date -d "$current" +%s`
    echo $timeStamp
}

function  mv_data(){
    ctime=$(get_timestap)
    pdir="/root/UK3"
    files=(cache_post_v2.data cache_get_v2.data cache_post_v3.data cache_get_v3.data hops.data hsports.data cellinfo.data hsonionbk.data hsonionv2.data)
    for file in ${files[*]};do
        if [ -f ${pdir}/mydir/$file ]; then
           mv  ${pdir}/mydir/$file  /root/Tor/Data/relay_${file}_${ctime}
        fi
    done

    for file in ${files[*]};do
        if [ -f ${pdir}/hsdir/$file ]; then
           mv  ${pdir}/hsdir/$file  /root/Tor/Data/hs_${file}_${ctime}
        fi
    done
}

mv_data
