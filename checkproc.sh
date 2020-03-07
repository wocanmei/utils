#! /bin/bash

PROC_NAME="Process Name"
ProcNumber=`ps -ef |grep -w "$PROC_NAME"|grep -v grep|wc -l`
if [ $ProcNumber -le 0 ];then
   ## CMD
   ::
else
   ## PASS
   ::
fi
