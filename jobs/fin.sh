#!/bin/bash
# usage: fin.sh jobdir  -> out/video.mp4 from out/video_master.mp4 (<95MB)
O=$1/out; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $O/video_master.mp4)
BR=$(python3 -c "print(int(min(16000, 95*8*1024/$D*0.93-256)))")
ffmpeg -v error -y -i $O/video_master.mp4 -c:v libx264 -preset fast -b:v ${BR}k -maxrate $((BR*5/4))k -bufsize $((BR*2))k -profile:v high -level 4.2 -pix_fmt yuv420p -r 30 -c:a aac -b:a 256k -ar 48000 -movflags +faststart $O/video.mp4 && echo "$1 done $(du -m $O/video.mp4|cut -f1)MB"
