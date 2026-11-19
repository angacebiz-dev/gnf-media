#!/bin/bash
# usage (from gnf root): jlf/finish.sh <dir> <out_name> [seed]
# concat render chunks -> piano bed ~20 dB under the voice (hits on section starts) -> -15 LUFS -> 1080p H.264 + AAC, faststart
set -e; cd /home/claude/gnf; D=$1; OUT=$2; SEED=${3:-3}
ls $D/chunk_*.mp4 | sort -V | sed "s|^|file '$PWD/|;s|$|'|" > $D/chunks.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $D/chunks.txt -c copy $D/video.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $D/video.mp4)
HITS=$(python3 -c "
import json; b=json.load(open('$D/beats.json')); print(','.join(str(x['t']) for i,x in enumerate(b) if i and x['sec']!=b[i-1]['sec']))")
python3 somber.py $D/music.wav $DUR "$HITS" $SEED
ffmpeg -y -loglevel error -i $D/voice.wav -ar 48000 $D/voice48.wav
ffmpeg -y -loglevel error -i $D/video.mp4 -i $D/voice48.wav -i $D/music.wav \
  -filter_complex "[2:a]volume=-20dB[m];[1:a]apad[v];[v][m]amix=inputs=2:duration=shortest:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a pcm_s16le -t $DUR $D/mix.mkv
I=$(ffmpeg -i $D/mix.mkv -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -n 1 | awk '{print $2}')
G=$(python3 -c "print(round(-15.0 - ($I), 2))")
mkdir -p out
ffmpeg -y -loglevel error -i $D/mix.mkv -c:v libx264 -preset veryfast -crf 24 -maxrate 7M -bufsize 14M -pix_fmt yuv420p \
  -af "volume=${G}dB,alimiter=limit=0.89:level=false" -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/$OUT
echo "FINISH OK out/$OUT $(stat -c%s out/$OUT) bytes, mix was $I LUFS, gain $G dB"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height -of compact out/$OUT
