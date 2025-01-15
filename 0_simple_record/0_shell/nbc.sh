#! /bin/bash

ip=192.168.0.151

#curl -o output_file.ts "http://hdhomerun_ip_address:5004/auto/vX.Y/?duration=Z"
# test favorite channels

dir=/home/tony/play
show=nbc
chan=46.1

curl -o $dir/$show.ts $ip:5004/auto/v$chan?duration=14400 &
