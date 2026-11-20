#!/bin/bash
cd /home/claude/gnf/s6
while pgrep -f "renderall.sh el pr pt" >/dev/null; do sleep 20; done
./renderall.sh dn el
