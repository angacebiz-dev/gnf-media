#!/bin/bash
# render -> mix -> encode each toon Short in turn (2 parallel halves per Short)
cd /home/claude/gnf/s6

for S in $@; do
  if true; then
    N=$(python3 -c "
import sys; sys.argv=['engine5.py','$S']; import engine5 as E; print(int(E.END*E.FPS))" 2>/dev/null | tail -1)
    H=$((N/2))
    python3 engine5.py $S --range 0 $((N/3)) > /tmp/r_${S}_a.log 2>&1 &
    python3 engine5.py $S --range $((N/3+1)) $((2*N/3)) > /tmp/r_${S}_b.log 2>&1 &
    python3 engine5.py $S --range $((2*N/3+1)) 99999 > /tmp/r_${S}_0.log 2>&1 &

    wait
  fi
  python3 mix5.py $S > /tmp/mix_${S}.log 2>&1
  ffmpeg -y -loglevel error -framerate 24 -i $S/fr/f_%05d.png -i $S/mix.wav -c:v libx264 -crf 19 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart /home/claude/gnf/s6/gnf_hd_${S}.mp4
  echo "DONE $S $(date +%T) $(ls $S/fr | wc -l) frames" >> /tmp/renderall.log
done
