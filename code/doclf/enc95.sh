#!/bin/bash
# usage: enc95.sh <in> <out>  -> two-pass x264 sized for <= ~95 MB (GitHub limit 100 MB), AAC 128k
set -e; IN=$1; OUT=$2; T=$(mktemp -d)
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $IN)
VB=$(python3 -c "print(int(94e6*8/$DUR - 128000))")
cd $T
ffmpeg -y -loglevel error -i $IN -c:v libx264 -preset medium -b:v $VB -pass 1 -an -f null /dev/null
ffmpeg -y -loglevel error -i $IN -c:v libx264 -preset medium -b:v $VB -pass 2 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart $OUT
echo "ENC OK $OUT $(stat -c%s $OUT) bytes, video $VB bps"
