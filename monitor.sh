#!/bin/bash
file=/var/log/web_watch.log
res=0
if [ ! -f $file ];then
    res=0
elif [ ! -s $file ];then
    res=0
else
    dir=`cat /var/log/web_watch.log | awk -F "[-]" '{print $2}'`
    for i in $dir
    do
        users=`ls -ld $i|awk '{print $3}'`
        if [ $users != tan ];then
            res=1
            break
        else
            res=0
        fi
    done
fi
echo $res
