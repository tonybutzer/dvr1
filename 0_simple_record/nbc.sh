#! /bin/bash

#curl -o output_file.ts "http://hdhomerun_ip_address:5004/auto/vX.Y/?duration=Z"
# test favorite channels

dir=/home/tony/tv/video
show=nbc
chan=46.1

curl -o $dir/$show.ts 192.168.0.93:5004/auto/v$chan?duration=14400 &
