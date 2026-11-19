#!/bin/bash
# usage: post_lf.sh <dir> <YYYY-MM-DD> <slug>  -> copies out/<slug>.mp4 + <dir>/thumb_A/B/C.jpg into gnf-media lf/ + thumbs/, commits, pushes, checks raw URLs
set -e; D=$1; DATE=$2; SLUG=$3; R=/home/claude/gnf-media; G=/home/claude/gnf
cd $R && git pull -q origin main
cp $G/out/${DATE}_${SLUG}.mp4 lf/${DATE}_${SLUG}.mp4
for k in A B C; do cp $G/$D/thumb_$k.jpg thumbs/${DATE}_${SLUG}_$k.jpg; done
git add lf/${DATE}_${SLUG}.mp4 thumbs/${DATE}_${SLUG}_*.jpg
git -c user.name="Captain Spike (Claude)" -c user.email=noreply@anthropic.com commit -qm "Long-form ${DATE} ${SLUG}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Fm4WVGoJqSfmpxc71YawHW"
git -c push.negotiate=true push -q origin main
for p in lf/${DATE}_${SLUG}.mp4 thumbs/${DATE}_${SLUG}_A.jpg; do
  L=$(stat -c %s $p); C=$(curl -sSI https://raw.githubusercontent.com/angacebiz-dev/gnf-media/main/$p | grep -i '^content-length' | tail -1 | awk '{print $2}' | tr -d '\r')
  echo "$p local=$L remote=$C $([ "$L" = "$C" ] && echo OK || echo MISMATCH)"
done
