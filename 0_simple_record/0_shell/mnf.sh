#! /bin/bash

#curl -o output_file.ts "http://hdhomerun_ip_address:5004/auto/vX.Y/?duration=Z"
# test favorite channels

dir=/home/tony/tv/video
chan=13.1

#curl -o $dir/ion.ts 192.168.0.93:5004/auto/v7.7?duration=30 &
#echo curl -o $dir/mnf1.ts 192.168.0.93:5004/auto/v$chan?duration=3600 | at 19:10
echo curl -o $dir/mnf2.ts 192.168.0.93:5004/auto/v$chan?duration=3600 | at 20:10
echo curl -o $dir/mnf3.ts 192.168.0.93:5004/auto/v$chan?duration=3600 | at 21:10
echo curl -o $dir/mnf4.ts 192.168.0.93:5004/auto/v$chan?duration=3600 | at 22:10
