#! /bin/bash

#curl -o output_file.ts "http://hdhomerun_ip_address:5004/auto/vX.Y/?duration=Z"
# test favorite channels

dir=/home/tony/tv/video

curl -o $dir/cbs.ts 192.168.0.93:5004/auto/v11.1?duration=120 &
curl -o $dir/abc.ts 192.168.0.93:5004/auto/v13.1?duration=120 &
curl -o $dir/nbc.ts 192.168.0.93:5004/auto/v46.1?duration=120 &
curl -o $dir/fox.ts 192.168.0.93:5004/auto/v46.2?duration=120 &
curl -o $dir/mytv.ts 192.168.0.93:5004/auto/v11.2?duration=120 &
