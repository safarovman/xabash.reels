#!/bin/bash
cd /home/claude/xabash.reels
for j in "$@"; do echo "START $j $(date -u +%H:%M)"; python3 reel/engine.py jobs/$j > /tmp/r_$j.log 2>&1; echo "engine $j exit $? $(date -u +%H:%M)"; done
