#! /bin/bash

#curl -o output_file.ts "http://hdhomerun_ip_address:5004/auto/vX.Y/?duration=Z"
# test favorite channels

dir=/home/tony/tv/video

#curl -o $dir/ion.ts 192.168.0.93:5004/auto/v7.7?duration=30 &
echo curl -o $dir/ion.ts 192.168.0.93:5004/auto/v13.4?duration=14400 | at 1:03
