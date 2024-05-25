#!/bin/bash

pid=$(pgrep -f "python3 main.py")

gcore -o memdump.core $pid >/dev/null 2>&1
echo $(strings memdump.core.$pid | grep "Client connected from")
echo $(strings memdump.core.$pid | grep "Received message:")
echo $(strings memdump.core.$pid | grep "Server Response:")