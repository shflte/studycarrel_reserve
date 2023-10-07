#!/bin/bash

BOT_PROCESS="bot.py"

if pgrep -f "$BOT_PROCESS" >/dev/null; then
    echo "bot.py running"
else
    echo "bot.py not running, restarting..."
  
    cd /home/shflte/studycarrel_reserve
  
    nohup python3 bot.py >/dev/null 2>&1 &
  
    echo "bot.py restarted"
fi
