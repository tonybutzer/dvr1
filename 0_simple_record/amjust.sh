#! /bin/bash

#curl -o output_file.ts "http://hdhomerun_ip_address:5004/auto/vX.Y/?duration=Z"
# test favorite channels

dir=/home/tony/tv/video

curl -o $dir/american_justice.ts 192.168.0.93:5004/auto/v14.4?duration=14400 &
